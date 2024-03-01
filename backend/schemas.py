from pydantic import BaseModel,Field

class UserBase(BaseModel):
    user_id: str
    username: str = Field(min_length=5,max_length=32) 
    name: str

class GroupsBase(BaseModel):
    groupname : str

class Users_Groups_Mapping_Base(BaseModel):
    group_id : int
    user_ids : list = [str]


class groups(GroupsBase):
    groupname:str
    group_id : int

class users_group_mapping(Users_Groups_Mapping_Base):
    group_id : str
    users : list[Users_Groups_Mapping_Base] = []

class User(UserBase):
    # username : str
    users: list[users_group_mapping] = []

class Transactions(BaseModel):
    group_id : int
    transaction_name : str
    transactions: list[tuple[int, str, str]]