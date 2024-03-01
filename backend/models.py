from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(String(32),primary_key=True,nullable=False)
    username = Column(String,nullable=False)
    name = Column(String,nullable=False)

    groups = relationship("Users_Groups_Mapping",backref="users_mapping")

class Groups(Base):
    __tablename__ = "groups"

    group_id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    groupname = Column(String,nullable=False)

    users = relationship("Users_Groups_Mapping",backref="group_mapping")

class UserTransactions(Base):
    __tablename__ = "user_transactions"

    transaction_id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    payeer = Column(String,nullable=False)
    payee = Column(String,nullable=False)
    amount = Column(Integer, nullable=False)
    transaction_name = Column(String , nullable=False)
    group_id = Column(Integer,ForeignKey("groups.group_id"))

class Users_Groups_Mapping(Base):
    __tablename__ = "users_group_mapping"

    user_id = Column(String,ForeignKey("users.user_id"),nullable=False,primary_key=True)
    group_id = Column(Integer,ForeignKey("groups.group_id"),nullable=False,primary_key=True)