from configargparse import ArgParser

p = ArgParser(
    auto_env_var_prefix='KLAUD_',
    default_config_files=['./settings.ini'],
)
p.add('-c', '--config', is_config_file=True, help='config file path')
p.add('-p', '--port', type=int, default=8000, help='port for serving')
p.add('-H', '--host', type=str, default='0.0.0.0', help='host for serving')

settings = p.parse_args()
