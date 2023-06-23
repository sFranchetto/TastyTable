from flask import Flask, render_template, request, redirect, session, jsonify, flash
from database import register_user_to_db, login_user
import os

app=Flask(__name__)

app.secret_key = os.environ['SECRET_KEY']


@app.route("/")
def home():
  return render_template('home.html')


##############################################################
############### LOGIN / REGISTRATION / SESSION ###############
##############################################################

@app.route("/login", methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
        try:
          data = request.form
          user = login_user(data)[0]['username']
          if user:
              session['logged_in'] = True
              session['username'] = user
              return render_template('dashboard.html')
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
    return redirect('/login')

######################   END    ##############################
############### LOGIN / REGISTRATION / SESSION ###############
##############################################################


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)