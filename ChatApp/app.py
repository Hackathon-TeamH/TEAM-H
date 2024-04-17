from flask import Flask, redirect, render_template, request, session, flash
from datetime import timedelta
import hashlib
import uuid
import re

from util.db import DB
from config import config
from models import models

import translation


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
    # TODO:既に登録されているユーザーか判定
    # user = models.getUser(email)

  #if user != None:
  #  flash('既に使用されているアドレスです')
    models.create_user(id,name,email,password,lng,learning_lng,country,city,last_operation_at)
    UserId = str(id)
    session['uid'] = UserId
    return redirect('/')
  return redirect('/signup')


# チャットページ
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/message')
def all_message():
    sent_message = models.getMessageAll()
    return render_template('chat.html', sent_message=sent_message)


#チャット送信
@app.route('/message', methods=['POST'])
def send_messege():
    
    #ログイン処理でsessionに入れたidを使う
    #user_id = session.get("id")　
    user_id = 1
    if user_id is None:
        return redirect('/login') #リンク先は要調整

    #チャンネルに入るとき？にidをもらう
    #channel_id = request.form.get('channel_id')
    channel_id = 1

    message = request.form.get('message')
    if message is None:
        return redirect('/')

    #学ぶ/教える言語が必ず対になる前提の記述
    language_pair = models.translationlanguage(user_id)
    
    for lang in language_pair:
        src = lang['learning_language']
        dest = lang['language']
    
    translated_message = translation.translation(message, src, dest)
    models.createMessage(message, translated_message, user_id, channel_id)
    return redirect('/message')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=False)
 

  
