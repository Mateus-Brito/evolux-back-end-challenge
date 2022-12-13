# -*- coding: utf-8 -*-
"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from datetime import timedelta

from environs import Env

env = Env()
env.read_env()

ROWS_PER_PAGE = env.int("ROWS_PER_PAGE", default=10)
FLASK_DEBUG = env.str("FLASK_DEBUG", default=False)
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL", default="sqlite:////tmp/test.db")
SECRET_KEY = env.str("SECRET_KEY")
BCRYPT_LOG_ROUNDS = env.int("BCRYPT_LOG_ROUNDS", default=13)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_ERROR_MESSAGE_KEY = "message"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=10)
SENTRY_DSN_URL = env.str("SENTRY_DSN_URL", default=None)
SAVE_LOG_FILE = False
