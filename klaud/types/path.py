class Path(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not v.startswith('/'):
            v = '/' + v
        while '//' in v:
            v = v.replace('//', '/')
        if any(part.startswith('_') for part in v.split('/') if v):
            raise ValueError('parts starts with underscope is reserved')
        return v
