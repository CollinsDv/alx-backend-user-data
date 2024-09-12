#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds users to database
        """
        user = User(email=email, hashed_password=hashed_password)

        current_sesh = self._session

        try:
            current_sesh.add(user)
            current_sesh.commit()
        except Exception:
            current_sesh.rollback()
            user = None
        finally:
            return user

    def find_user_by(self, **kwargs) -> User:
        """searches users in database
        Args:
            kwargs: set of values to query
        """
        if not kwargs:
            raise InvalidRequestError

        current_sesh = self._session
        try:
            user = current_sesh.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
        except NoResultFound:
            raise NoResultFound

        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """updates users
        Args:
            user_id: id
            kwargs: other items to update with
        """
        current_sesh = self._session

        try:
            user = self.find_user_by(id=user_id)

            for key, value in kwargs.items():
                if not hasattr(user, key):
                    raise ValueError
                setattr(user, key, value)

            current_sesh.commit()
        except Exception as e:
            current_sesh.rollback()
            raise e
