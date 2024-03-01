from sqlalchemy.orm import Session
import models, schemas

def get_user(db: Session, user_id: str):
    user = db.query(models.Users)\
        .filter(models.Users.user_id == user_id).first()
    return user

def create_user(db: Session, user: schemas.UserBase):
    db_user = models.Users(user_id = user.user_id , username = user.username , name = user.name )
    db.add(db_user) 
    db.commit()
    db.refresh(db_user)
    return db_user

def get_group(db: Session,user_id :str):
    db_groups = db.query(models.Groups)\
    .join(models.Users_Groups_Mapping, models.Groups.group_id == models.Users_Groups_Mapping.group_id)\
    .join(models.Users, models.Users.user_id == models.Users_Groups_Mapping.user_id)\
    .filter(models.Users.user_id == user_id)\
    .all()
    return db_groups

def create_group(db: Session, group: schemas.GroupsBase):
    db_group = models.Groups(groupname = group.groupname)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def map_user_group(db: Session, user_group_mapping: schemas.Users_Groups_Mapping_Base):
        
        for user_id in user_group_mapping.user_ids:
            # Check if the user is already mapped to the group
            existing_mapping = db.query(models.Users_Groups_Mapping).filter_by(group_id=user_group_mapping.group_id, user_id=user_id).first()
            
            if existing_mapping:
                continue 

            new_mapping = models.Users_Groups_Mapping(group_id=user_group_mapping.group_id, user_id=user_id)
            db.add(new_mapping)
        
        db.commit()
        
        return {'msg': 'success'}, 200

def add_transaction(db : Session, transactions : schemas.Transactions):
    group_id = transactions.group_id
    transaction_name = transactions.transaction_name
    for transaction in transactions.transactions:
        db_transaction = models.UserTransactions( amount = transaction[0] ,payeer = transaction[1], payee = transaction[2]  , group_id = group_id,transaction_name=transaction_name)
        db.add(db_transaction)
    db.commit()
    return {'msg':'success'},200
    