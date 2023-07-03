from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for, send_file
from database import register_user_to_db, login_user, load_users_from_db, load_user_from_db,save_picture_to_database, show_picture_from_db, save_default_picture_to_database, edit_user_info, create_recipe, get_user_id
from werkzeug.utils import secure_filename
from base64 import b64encode
import os, io



app=Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']


@app.route("/")
def home():
  users = load_users_from_db()
  return render_template('home.html', users=users)


##############################################################
############### LOGIN / REGISTRATION / SESSION ###############
##############################################################

@app.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
        try:
          data = request.form
          username = login_user(data)[0]['username']
          if username:
              session['logged_in'] = True
              session['username'] = username
              return redirect(url_for('user_profile', username=username))
        except TypeError:
          flash('Invalid email or password')

  return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    data = request.form
    pw = data['password']
    cpw = data['confirmed_password']
    if pw == cpw:
      register_user_to_db(data)
      temp_pic = process_picture_default_picture()
      save_default_picture_to_database(temp_pic, data)
      flash('You have successfully created your account! Please log in', 'success')
      return redirect('/login')
    else:
      flash('Passwords do not match!', 'error')
  return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully signed out')
    return redirect('/')

######################   END    ##############################
############### LOGIN / REGISTRATION / SESSION ###############
##############################################################

##############################################################
#####################   PROFILE   ############################
##############################################################

@app.route('/profile/<username>')
def user_profile(username):
    user = load_user_from_db(username)
    image = show_picture_from_db(username)
    try:
      image_data = b64encode(image.profile_picture).decode("utf-8")
      return render_template('user_profile.html', user=user, image_data=image_data, image=image)
    except TypeError:
      return render_template('error.html')
      

@app.route('/profile/<username>/edit_profile', methods=['GET', 'POST'])
def edit_user_profile_picture(username):
    user = load_user_from_db(username)
    return render_template('edit_profile_picture.html', user=user)

@app.route('/profile/<username>/edit_profile_picture', methods=['GET', 'POST'])
def edit_profile_picture(username):
  if request.method == 'POST':
    picture = request.files['picture']
    save_picture_to_database(picture, username)
    return redirect(f'/profile/{username}')
  return render_template('edit_profile.html')

@app.route('/profile/<username>/edit_profile_info', methods=['GET', 'POST'])
def edit_profile_info(username):
  user = load_user_from_db(username)
  image = show_picture_from_db(username)
  try:
    image_data = b64encode(image.profile_picture).decode("utf-8")
    return render_template('edit_profile_info.html', user=user, image_data=image_data, image=image)
  except TypeError:
    return render_template('error.html')
  return render_template('edit_profile_info.html')

@app.route('/profile/<username>/edit_profile_info_sent', methods=['GET', 'POST'])
def edit_profile_info_sent(username):
  if request.method == 'POST':
    data = request.form
    edit_user_info(data, username)
    return redirect(f'/profile/{username}')
  return render_template('error.html')

######################   END    ##############################
#####################   PROFILE   ############################
##############################################################









@app.route('/explore')
def explore():
  return render_template('explore.html')


@app.route('/recipe/create',  methods=['GET', 'POST'])
def recipe_create():
  if request.method == 'POST':
    username = session['username']
    data = request.form
    user_id = get_user_id(username)
    create_recipe(data, user_id[0]['id'])
  return render_template('create_recipe.html')





















def process_picture_default_picture():
  image_path = 'static/default_profile_picture.jpg'
  with open(image_path, 'rb') as file:
    image_data = file.read()
    blob = io.BytesIO(image_data)
  return blob

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)

