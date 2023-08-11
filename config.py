"""
Module to handle application configuration settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings():
    """
        Class to define application settings.
    """
    
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    
    DB_USER: str = os.getenv('DB_USER')
    DB_NAME: str = os.getenv('DB_NAME')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = os.getenv('DB_PORT')
    DB_URL: str = os.getenv('DB_URL')
        

settings = Settings()
