from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

def register_user_to_db(data):
  with engine.connect() as conn:
    conn.execute(text("INSERT INTO users (email_address, username, password) VALUES (:email_address, :username, :password)").
                 params(
                   email_address = data['email_address'], 
                   username = data['username'],     
                   password = data['password']))


def login_user(data):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM users WHERE email_address = :email_address AND password = :password").
                 params(
                   email_address = data['email_address'],     
                   password = data['password']))
    user = []
    for row in result.all():
      user.append(row._asdict())
    if len(user) == 0:
      return None
    else:
      return user

def load_users_from_db():
  with engine.connect() as conn:
    result = conn.execute(
      text("select * from users"))
    user = []
    for row in result.all():
      user.append(row._asdict())
    if len(user) == 0:
      return None
    else:
      return user


def load_user_from_db(username):
    with engine.connect() as conn:
      result = conn.execute(
        text("select * from users WHERE username = :username")
        .params(username=username))
      user = []
      for row in result.all():
        user.append(row._asdict())
      if len(user) == 0:
        return None
      else:
        return user


def save_picture_to_database(picture, username):
  picture_data = picture.read()
  with engine.connect() as conn:
    conn.execute(text("UPDATE users SET profile_picture = :profile_picture WHERE username = :username").
                 params(
                   profile_picture = picture_data,
                    username = username))


def save_default_picture_to_database(picture, data):
  picture_data = picture.read()
  with engine.connect() as conn:
    conn.execute(text("UPDATE users SET profile_picture = :profile_picture WHERE username = :username").
                 params(
                   profile_picture = picture_data,
                    username = data['username']))


def show_picture_from_db(username):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT profile_picture FROM users WHERE username = :username")
                         .params(
                           username = username
                         ))
    row = result.fetchone()
    image_data = row
    if image_data:
      return image_data
    else:
      return None


def edit_user_info(data, username):
  with engine.connect() as conn:
    conn.execute(text("UPDATE users SET Firstname = :firstname, Lastname = :lastname,  country = :country, about = :about, cheftype = :level WHERE username =:username").
                 params(
                   firstname = data['firstname'], 
                   lastname = data['lastname'],     
                   country = data['country'],
                   about = data['about'],
                   level = data['level'],
                   username = username))