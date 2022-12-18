import os


class Config:
    # localhost 'postgresql://postgres:postgres@127.0.0.1:5432/flask-delivery'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')\
                              or 'postgresql://shanin-ivan:JE5VjFRNwy2i@ep-damp-hall-087772.eu-central-1.aws.neon.tech/neondb'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-difficult-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # TRAP_HTTP_EXCEPTIONS = True
