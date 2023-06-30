import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # should use ENV variable
    SECRET_KEY = "2cp88k5a4zeyif5f"
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Auth-Token"
    # should use ENV variable
    SECURITY_PASSWORD_SALT = "0hbcndakxfkou6ut"
    SECURITY_PASSWORD_HASH = "sha256_crypt"
    SECURITY_LOGIN_URL = "/api/login"
    SECURITY_LOGOUT_URL = "/api/logout"
    SECURITY_USERNAME_ENABLE = True
    SECURITY_USERNAME_REQUIRED = True
    SECURITY_TRACKABLE = True


class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        SQLITE_DB_DIR, "database.sqlite3"
    )
    DEBUG = True


class ProductionDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        SQLITE_DB_DIR, "database.sqlite3"
    )
    DEBUG = False
