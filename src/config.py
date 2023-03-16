from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_SERVER = os.environ.get('POSTGRES_SERVER')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
DB_HOST = os.environ.get('DB_HOST')

SMTP_USER = str(os.environ.get("SMTP_USER"))
SMTP_PASSWORD = str(os.environ.get("SMTP_PASSWORD"))

SECRET_AUTH = os.environ.get("SECRET_AUTH")