class DevelopmentConfig:
    DEBUG = True
    SECRET_KEY = "sample1203"
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
