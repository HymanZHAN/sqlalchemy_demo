from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()
db_uri = "sqlite:///db.sqlite"

engine = create_engine(db_uri, pool_pre_ping=True,)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

engine_test = create_engine(db_uri, pool_pre_ping=True,)
session_test = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine_test))
