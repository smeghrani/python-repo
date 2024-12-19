import os
from configparser import ConfigParser
from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session
from src.config import CONFIG_PATH

def get_db_engine():
    config = ConfigParser()
    config.read(os.path.join(CONFIG_PATH, "config.ini"))
    DBNAME = config["DB"]["DBNAME"]
    DBPATH = config["DB"]["DBPATH"]
    DBPATH = os.path.join(os.getcwd(), DBPATH)
    DBPATH = os.path.join(DBPATH, DBNAME)
    sqlite_url = f"sqlite:///{DBPATH}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, connect_args=connect_args)
    return engine

def get_session():
    engine = get_db_engine()
    with Session(engine) as db:
        yield db

SessionDep = Annotated[Session, Depends(get_session)]