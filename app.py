from flask import Flask, render_template, request, redirect, session, jsonify, flash, url_for
from database import register_user_to_db, login_user, load_users_from_db, load_user_from_db
import os

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
      return redirect('/login')
    else:
      flash('Passwords do not match!')
  return render_template('register.html')

@app.route("/dashboard")
def dashboard():
  try:
    if session['username'] != None:
      return render_template('dashboard.html')
  except:
    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully signed out')
    return redirect('/')

######################   END    ##############################
############### LOGIN / REGISTRATION / SESSION ###############
##############################################################

@app.route('/profile/<username>')
def user_profile(username):
    user = load_user_from_db(username)
    return render_template('user_profile.html', user=user)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)