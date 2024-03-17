import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv

load_dotenv()

database_username = os.environ['DB_USER']
database_password = os.environ['DB_PASSWORD']
database_ip       = os.environ['DB_IP']
database_name     = os.environ['DB_NAME']
database_port     = os.environ['DB_PORT']

engine = create_engine('mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}'.
    format(database_username, database_password, database_ip, database_port, database_name))

Session = sessionmaker(bind=engine)

Base = declarative_base()