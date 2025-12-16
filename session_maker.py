from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
db_url =  "postgresql://postgres:1234567890@localhost:5432/sarathdb"

engine = create_engine(db_url)
session = sessionmaker(autoflush = False, autocommit = False, bind = engine)

