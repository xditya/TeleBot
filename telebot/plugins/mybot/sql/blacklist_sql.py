# (c) @SpEcHIDe

from sqlalchemy import (
    Column,
    String
)
from . import (
    SESSION,
    BASE
)


class blacklist(BASE):
    __tablename__ = "blacklist"
    chat_id = Column(String(14), primary_key=True)
    # reason = Column(UnicodeText)

    def __init__(self, chat_id):
        self.chat_id = int(chat_id)
        # self.reason = reason

    def __repr__(self):
        return "<BL %s>" % self.chat_id


blacklist.__table__.create(checkfirst=True)


def add_user_to_bl(chat_id: int):
    """Adding the user to the blacklist"""
    __user = blacklist(str(chat_id))
    SESSION.add(__user)
    SESSION.commit()


def check_is_black_list(chat_id):
    """check if blacklisted"""
    try:
        return SESSION.query(blacklist).filter(
            blacklist.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def rem_user_from_bl(chat_id):
    """remove from bl"""
    __user = SESSION.query(blacklist).get(str(chat_id))
    if __user:
        SESSION.delete(__user)
        SESSION.commit()


def all_bl_users():
    """get all bl users"""
    __user = SESSION.query(blacklist).all()
    SESSION.close()
    return __user
