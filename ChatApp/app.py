from flask import Flask, redirect, render_template, request, session, flash
from datetime import timedelta
import hashlib
import uuid
import re

from config import config
from models import models

app = Flask(__name__)
app.config.from_object(config)


@app.route('/signup')
def signup():
    return render_template('registration/signup.html')


@app.route('/signup', methods=['POST'])
def user_signup():
  id = uuid.uuid4()
  name = request.form.get('name')
  email = request.form.get('email')
  password1 = request.form.get('password1')
  password2 = request.form.get('password2')
  lng = request.form.get('language')
  learning_lng = request.form.get('learning_language')
  country = request.form.get('country')
  city = request.form.get('city')

  datetime = datetime.now()
  last_operation_at = datetime.strftime('%Y-%m-%d %H:%M:%S')

  pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

  if(name == "" | email == "" | password1 == "" | password2 == "" | lng == "" | learning_lng == ""):
    flash("必須項目をすべて入力してください")
  elif(password1 != password2):
    flash("同じパスワードを入力してください")
  elif(re.match(pattern,email)):
    flash("正しいパスワードを入力してください")
  else:
    password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
    user = models.getUser(email)

  if user != None:
    flash('既に使用されているアドレスです')
  else:
     models.create_user(id,name,email,password,lng,learning_lng,country,city,last_operation_at)
     UserId = str(id)
     session['id'] = UserId
     return redirect('/')
  return redirect('/signup')


@app.route('/login')
def login():
    return render_template('registration/login.html')


@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if(email == "" & password == ""):
       flash('メールアドレスとパスワードを入力してください')
    elif(email == "" ):
       flash('メールアドレスを入力してください')
    elif(password == ""):
       flash('パスワードを入力してください')
    elif(re.match(pattern,email)):
       flash('正しいメールアドレスを入力してください')
    else:
       user = models.getUser(email)
       if user is None:
          flash('存在しないユーザーです')
       else:
          password = hashlib.sha256(password.encode('utf-8')).hexdigest()
          if(password != user["password"]):
             flash('パスワードが間違っています')
          else:
             session["id"] = user["id"]
             datetime = datetime.now()
             last_operation_at = datetime.strftime('%Y-%m-%d %H:%M:%S')
             models.updateLastOperationAt(user["id"],last_operation_at)
             return redirect('/')
    return redirect('/login')

if __name__ == '__main__': app.run(host="0.0.0.0", debug=False)