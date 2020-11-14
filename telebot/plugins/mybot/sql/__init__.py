#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

""" init SQL """

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from telebot.telebotConfig import DB_URI


def start() -> scoped_session:
    """ returns SQLAlchemy ScopedSession """
    engine = create_engine(DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(
        sessionmaker(
            bind=engine,
            autoflush=False
        )
    )


try:
    BASE = declarative_base()
    SESSION = start()
except BaseException:
    pass
