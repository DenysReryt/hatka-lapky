from models import db, UserModel, AdminModel

def get_all_users():
    query = UserModel.query
    return query.all()

def get_chat_by_user_id(user_id):
    chat = UserModel.query.filter_by(user_id=user_id).first()
    return chat

def create_chat(first_name, username, user_id, last_message):
    chat = UserModel(first_name=first_name, username=username, user_id=user_id, last_message=last_message, messages=last_message + ' | ')
    db.session.add(chat)
    db.session.commit()
    return chat

def update_chat(user_id, last_message):
    chat = UserModel.query.filter_by(user_id=user_id).first()
    if not chat:
        return None
    chat.last_message = last_message
    chat.messages += last_message + ' | '
    chat.active = True
    db.session.commit()
    return chat

def stop_chat(user_id):
    chat = UserModel.query.filter_by(user_id=user_id).first()
    chat.messages += '\n'
    chat.active = False
    db.session.commit()
    return chat

def delete_chat(user_id):
    chat = UserModel.query.filter_by(user_id=user_id).first()
    db.session.delete(chat)
    db.session.commit()

def create_admin(username, password):
    existing_record = db.session.query(AdminModel).first()
    if existing_record is not None:
        return False
    admin = AdminModel(username=username, password=password)
    db.session.add(admin)
    db.session.commit()
    return admin

def get_admin(username):
    admin = AdminModel.query.filter_by(username=username).first()
    return admin

def delete_admin(username):
    admin = AdminModel.query.filter_by(username=username).first()
    db.session.delete(admin)
    db.session.commit()
