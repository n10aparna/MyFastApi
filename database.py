from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dburl = "postgresql://postgres:password@localhost:5432/mydatabase"
engine = create_engine(dburl)
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)