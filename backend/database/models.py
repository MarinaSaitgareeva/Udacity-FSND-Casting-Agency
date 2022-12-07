import os
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Boolean
from flask_migrate import Migrate


# Take environment variables from ".env" (file should be in the root directory of your project) 
load_dotenv()