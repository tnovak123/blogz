import os

class Config(object):
    # Secret Key that prevents cross site code injection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # Posts per page setting
    POSTS_PER_PAGE = 3
    # Debug feature
    DEBUG = True
    # Database interface settings
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


