# (c) @its_xditya
from sqlalchemy import Column, String
from . import BASE, SESSION


class userbase(BASE):
    __tablename__ = "UserBase"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


userbase.__table__.create(checkfirst=True)


def add_to_userbase(chat_id: int):
    __user = userbase(str(chat_id))
    SESSION.add(__user)
    SESSION.commit()


def full_userbase():
    users = SESSION.query(userbase).all()
    SESSION.close()
    return users


def present_in_userbase(chat_id):
    try:
        return SESSION.query(userbase).filter(
            userbase.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()
