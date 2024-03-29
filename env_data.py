from os import getenv
from dotenv import load_dotenv
load_dotenv(".env")

token = getenv("TOKEN")
db_user = getenv("DB_USER")
db_name = getenv("DB_NAME")
db_password = getenv("DB_PASSWORD")
