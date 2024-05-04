from flask import Flask, redirect, render_template, request, session, flash
from datetime import timedelta
import datetime
import hashlib
import uuid
import re

from config import config
from models import models

import translation


app = Flask(__name__)
app.config.from_object(config.Config)


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

  dt = datetime.datetime.now()
  last_operation_at = dt.strftime('%Y-%m-%d %H:%M:%S')

  pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

  if(name == "" or email == "" or password1 == "" or password2 == "" or lng == "" or learning_lng == ""):
    flash("必須項目をすべて入力してください")
  elif(password1 != password2):
    flash("同じパスワードを入力してください")
  elif(re.match(pattern,email) is None):
    flash("正しいメールアドレスを入力してください")
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

    if(email == "" and password == ""):
       flash('メールアドレスとパスワードを入力してください')
    elif(email == "" ):
       flash('メールアドレスを入力してください')
    elif(password == ""):
       flash('パスワードを入力してください')
    elif(re.match(pattern,email) is None):
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
             dt = datetime.datetime.now()
             last_operation_at = dt.strftime('%Y-%m-%d %H:%M:%S')
             models.updateLastOperationAt(user["id"],last_operation_at)
             return redirect('/')
    return redirect('/login')


# ハブページ用
@app.route('/')
def home():
    return render_template('home.html')


# チャットページ
@app.route('/message')
def all_message():
    sent_message = models.getMessageAll()
    return render_template('chat.html', sent_message=sent_message)


#チャット送信
@app.route('/message', methods=['POST'])
def send_message():
    #ログイン処理でsessionに入れたidを使う
    #user_id = session.get("id")　
    user_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    if user_id is None:
        return redirect('/login') #リンク先は要調整

    #チャンネルに入るとき？にidをもらう
    #channel_id = request.form.get('channel_id')
    channel_id = 1

    message = request.form.get('message')
    if message is None:
        return redirect('/')

    #学ぶ/教える言語が必ず対になる前提の記述
    language_pair = models.translationLanguage(user_id)

    for lang in language_pair:
        src = lang['learning_language']
        dest = lang['language']

    translated_message = translation.translation(message, src, dest)
    models.createMessage(message, translated_message, user_id, channel_id)
    return redirect('/message')


# チャンネル一覧ページの表示
# 最終的には"/"にする
@app.route("/channel")
def index():
    # user_id = session.get("id")
    user_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    if user_id is None:
        return redirect('/login')
    else:
        channels = models.getChannelAll()
        channels.reverse()
    return render_template('index.html', channels=channels, user_id=user_id)


# チャンネルの追加
# 最終的には"/"にする
@app.route("/channel", methods=["POST"])
def add_channel():
    # sessionからuser_id取得
    # user_id = session.get("user_id")
    user_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    if user_id is None:
        return redirect("/login")
    channel_name = request.form.get("channel_name")
    id = uuid.uuid4()
    models.addChannel(id, channel_name, user_id)
    models.addToUsersChannels(user_id, id)
    return redirect("/channel")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=False)



