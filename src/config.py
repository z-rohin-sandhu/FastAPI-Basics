import os
from dotenv import load_dotenv

ROOT_DIR = os.path.join(os.path.dirname(__file__),"../")
DOT_ENV_PATH = os.path.join(os.path.dirname(__file__),"../") + ".env"
load_dotenv(DOT_ENV_PATH)

class Config(object):
    @staticmethod
    def getDBConnectionString():
        config= {}
        config["username"] = os.getenv('DB_USERNAME')
        config["host"] = os.getenv('DB_HOST')
        config["password"] = os.getenv('DB_PASSWORD')
        config["database"] = os.getenv('DATABASE')
        config["port"] = os.getenv('DB_PORT')
        return f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    
    @staticmethod
    def uvicornDict():
        config= {}
        config["host"] = os.getenv('UVICORN_HOST')
        config["port"] = os.getenv('UVICORN_PORT')
        config["reload"] = os.getenv('UVICORN_RELOAD')
        return config
    
    @staticmethod
    def metaDataDict():
        meta_data_dict = {}
        meta_data_dict['TITLE'] = os.getenv('TITLE')
        meta_data_dict['VERSION'] = os.getenv('VERSION')
        meta_data_dict['DESCRIPTION'] = os.getenv('DESCRIPTION')
        meta_data_dict['NAME'] = os.getenv('NAME')
        meta_data_dict['EMAIL'] = os.getenv('EMAIL')
        meta_data_dict['DOCS_URL'] = os.getenv('DOCS_URL')
        meta_data_dict['REDOC_URL'] = os.getenv('REDOC_URL')
        meta_data_dict['OPENAPI_URL'] = os.getenv('OPENAPI_URL')
        return meta_data_dict
    
    @staticmethod
    def jwtCredDict():
        jwt_dict = {}
        jwt_dict['SECURITY_KEY'] = os.getenv('SECURITY_KEY')
        jwt_dict['ALGORITHM'] = os.getenv('ALGORITHM')
        return jwt_dict

    METADATA_DICT = metaDataDict()
    UVICORN_DICT= uvicornDict()
    SQLALCHEMY_DATABASE_URI = getDBConnectionString()
    JWT_DICT = jwtCredDict()