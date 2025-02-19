from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    USER = environ.get("user")
    PASSWORD = environ.get("password")
    HOST = environ.get("host")
    PORT = environ.get("port")
    DBNAME = environ.get("dbname")
    OPEN_AI_KEY = environ.get("openai_key")
