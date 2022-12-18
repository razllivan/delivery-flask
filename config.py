import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')\
                              or 'postgresql://postgres:postgres@127.0.0.1:5432/flask-delivery'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-difficult-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TRAP_HTTP_EXCEPTIONS = True
