from environs import Env

env = Env()
env.read_env()

"""Settings module for test app."""
SQLALCHEMY_DATABASE_URI = env.str(
    "DATABASE_URL", "postgresql://postgres:postgres@db-test:5432/postgres_test"
)
FLASK_DEBUG = True
TESTING = True
SECRET_KEY = "not-so-secret-in-tests"
BCRYPT_LOG_ROUNDS = (
    4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_ERROR_MESSAGE_KEY = "message"
ROWS_PER_PAGE = 10
SENTRY_DSN_URL = None
SAVE_LOG_FILE = False
