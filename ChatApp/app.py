from flask import Flask, redirect, render_template, request, session, flash
from datetime import timedelta
# datetimeモジュールのインポートが必要
import datetime
import hashlib
import uuid
import re

from config import config
from models import models

import translation
from langdetect import detect



app = Flask(__name__)
app.config.from_object(config.Config)
# config.pyのConfigクラス

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

# 変数名がdatetimeだとエラーが起きたのでdtに
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
@app.route('/message/<channel_id>')
def all_message(channel_id):
    #user_id = session["id"]
    user_id = {}
    user_id = {"user_id":"35d485b3-f3e0-4b34-84bd-3460487c711e"}
    if user_id is None:
        return redirect('/login')
    print(user_id)

    # #貰ったcidをpythonの型に直す？ 無くてもいいのか？  
    # print(type(channel_id))   
    # channel_id = channel_id
    print(f"{channel_id} + {type(channel_id)}")
            
    channel_members = models.getChannelMemberId(channel_id)
    print(channel_members)

    if user_id not in channel_members:
        print("このチャンネルに参加していません")
        #flash("このチャンネルに参加していません")
        return redirect('/') 
    
    print("1")        
    messages = models.getMessageAll(channel_id)
    print("2")    
    channel = models.getChannelById(channel_id)
    return render_template('chat.html', messages=messages, channel=channel)


#チャット送信
@app.route('/message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    print(message)
    #sender_id = session["id"]
    sender_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    channel_id = request.form.get('channel_id')
    print(channel_id)
    
    if message is None:
        flash("メッセージが入力されていません")
        return redirect("/message/{channel_id}".format(channel_id = channel_id))
    elif sender_id is None:
        return redirect('/login')
    else:
        source_lang, target_lang = translation.get_language_pair(sender_id, channel_id) 
        print(f"翻訳元言語は{source_lang},翻訳先言語は{target_lang}")

    #入力言語判定
    input_lang = detect(message)
    print(f"入力言語は{input_lang}")
    if input_lang != source_lang:
        #flash("身につけたい言語で入力してみよう")
        print("身につけたい言語で入力してみよう")
        return redirect("/message/{channel_id}".format(channel_id = channel_id))

    translated_message = translation.translation(message, source_lang, target_lang)
    print(translated_message)
    models.createMessage(message, translated_message, sender_id, channel_id)

    return redirect("/message/{channel_id}".format(channel_id = channel_id))



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


#メッセージ削除
#編集機能実装するなら関数として切り離して流用するorこの中でif使って編集もやる
@app.route('/message', methods=['POST'])
def delete_message():
    user_id = session.get("id")
    message_id = request.form.get("message_id")
    
    message_info = models.getMessageById(message_id)
    sender_id = message_info["user_id"]
    channel_id = message_info["channel_id"]

    #フロントからのuserIDと合っているのか確認
    if user_id != sender_id:
        flash("自分の投稿ではありません")
    else:
        new_message = "この投稿は削除されました"
        source_lang, target_lang = translation.get_language_pair(sender_id, channel_id)
        new_translated_message = translation.translation(new_message, source_lang, target_lang)
        models.changeMessage(new_message, new_translated_message, message_id)
        
    #チャンネルIDをフロントに渡してメッセージ一覧ページに飛ばす
    return redirect("/message/{channel_id}".format(channel_id = channel_id))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=False)



