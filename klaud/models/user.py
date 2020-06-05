from typing import Optional

from pydantic import BaseModel, Field

from klaud.database import db


class User(BaseModel):
    username: str = Field(..., example='jonh_doe')
    is_master: bool = Field(False, example=False)


class UserInDB(User):
    uid: str = Field(..., example='some_uid')
    hashed: str = Field(..., example='abacaba')

    @classmethod
    async def find_by_username(cls, username: str) -> Optional['UserInDB']:
        result = await db()['users'].find_one({'username': username})
        if not result:
            return None
        return cls(
            uid=str(result['_id']),
            username=username,
            hashed=result['hashed'],
            is_master=result['is_master']
        )

    async def insert(self):
        await db()['users'].find_one_and_replace(
            {'username': self.username},
            {
                'username': self.username,
                'hashed': self.hashed,
                'is_master': self.is_master
            },
            upsert=True
        )
