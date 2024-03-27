from app.config.databaseConnection import get_database_connection_string

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

dbConnectionString = get_database_connection_string()
engine = create_engine(dbConnectionString)

Session = sessionmaker(bind=engine)