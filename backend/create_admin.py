#!/usr/bin/env python3
import os
from getpass import getpass
from app.db import SessionLocal, engine, Base
from app import crud, models

Base.metadata.create_all(bind=engine)
db = SessionLocal()
username = input('admin username: ').strip()
email = input('admin email (optional): ').strip() or None
password = getpass('admin password: ')
res = crud.create_user(db, {'username': username, 'email': email, 'password': password, 'is_admin': True})
if isinstance(res, dict) and res.get('error'):
    print('Error:', res)
else:
    print('Admin user created:', res.username)
db.close()
