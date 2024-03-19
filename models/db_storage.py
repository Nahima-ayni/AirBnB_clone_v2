#!/usr/bin/python3
"""New engine DBStorage"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """Handles interactions with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the DBStorage class"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine(
                "mysql+mysqldb://{}:{}@{}/{}".format(
                    user, password, host, database), pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

        from models.base_model import Base
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        """Query all objects from the database session"""
        from models import base_model

        result = {}
        if cls is not None:
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                result[key] = obj
        else:
            for cls in Base.__subclasses__():
                query_result = self.__session.query(cls).all()
                for obj in query_result:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    result[key] = obj

        return result

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all tables and creates a new session"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
                sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()
