import secrets

from configargparse import ArgParser

p = ArgParser(
    auto_env_var_prefix='KLAUD_',
    default_config_files=['./settings.ini'],
)
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-p', '--port', type=int, default=8000, help='port for serving')
p.add('-H', '--host', type=str, default='0.0.0.0', help='host for serving')
p.add('--hot-reload', action='store_true', help='enable hot reload')

p.add('--db-host', type=str, default='localhost', help='mongo server host')
p.add('--db-port', type=int, default=27017, help='mongo server port')
p.add('--db-user', type=str, default='user', help='mongo server user')
p.add('--db-password', type=str, default='hackme', help='mongo server password')
p.add('--db-name', type=str, default='klaud', help='mongo database name')

p.add('-S', '--secret', type=str, default=secrets.token_hex(64), help='secret token')
p.add('--access-token-life', type=int, default=15, help='access token life duration (in minutes)')
p.add('--master-name', type=str, default='master', help='master username')
p.add('--master-password', type=str, default='master', help='master password')

settings = p.parse_known_args()[0]
