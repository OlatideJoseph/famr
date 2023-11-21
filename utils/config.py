class Config:
    SECRET_KEY =  "8b9562889f24968e91ebdb6c2af18ba8cada1b34cfcccb1c64b5db118bf67143"
    SQLALCHEMY_DATABASE_URI = "sqlite:///sqlite.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SESSION_CO0KIE_DOMAIN = False

class DevelopmentConfig(Config):
    pass

class ProductionConfig(Config):
    SESSION_CO0KIE_DOMAIN = False
    SERVER_NAME = "olatidejosepha.pythonanywhere.com"