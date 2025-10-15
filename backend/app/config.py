import os
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://gigi:gigi_pass@db:5432/gigi_yogurt')
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '60'))
