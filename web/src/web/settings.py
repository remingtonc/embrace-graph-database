from starlette.config import Config
from starlette.datastructures import Secret

config = Config()

DEBUG = config('DEBUG', cast=bool, default=False)
ARANGODB_HOST = config('ARANGODB_HOST', cast=str, default='graphdb')
ARANGODB_DATABASE = config('ARANGODB_DATABASE', cast=str, default='embrace')
ARANGODB_USERNAME = config('ARANGODB_USERNAME', cast=str, default='root')
ARANGODB_PASSWORD = config('ARANGODB_PASSWORD', cast=Secret)
