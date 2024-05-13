from flask import Flask, redirect, render_template, request, session, flash, jsonify
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
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
app.config.from_object(config.Config)# config.pyのConfigクラス

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
  dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
        models.create_user(id,name,email,password,lng,learning_lng,country,city,dt,dt,is_active = True)
        UserId = str(id)
        session['id'] = UserId
        return redirect('/')
  return redirect('/')


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
             session['id'] = user["id"]
             last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
             models.updateLastOperationAt(user["id"],last_operation_at)
             return redirect('/')
    return redirect('/')


# メッセージ一覧
@app.route("/message")
def all_message():
    user_id = session.get("id")
    #user_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    channel_id = request.args.get("channel_id")
    
    if user_id is None:
        return redirect('/login')
    elif channel_id is None:
        return render_template('initial.html')
    else:
        session["channel_id"] = channel_id
          
    channel_members = models.getChannelMemberId(channel_id)

    #チャンネル内にいるのにチャンネルが削除された場合
    if not channel_members:
        print("チャンネルが見つかりません")
        return redirect('/')
    elif user_id not in channel_members:
        print("このチャンネルに参加していません")
        #flash("このチャンネルに参加していません")
        #return redirect('/') 
    
    messages = models.getMessageAll(channel_id)    
    channels = models.getChannelById(channel_id)
    
    return render_template('message.html', messages=messages, channel_id=channel_id, user_id=user_id, channels=channels)


#チャット送信
@app.route('/message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    sender_id = session.get("id")
    #sender_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    channel_id = session.get("channel_id")
    print(channel_id, message)
    
    if sender_id is None:
        return redirect('/login')
    elif channel_id is None:
        flash("チャンネルが選択されていません")
        return redirect(f"/message?channel_id={channel_id}") #todo:HTML修正
    elif message == "":
        flash("メッセージが入力されていません")
        return redirect(f"/message?channel_id={channel_id}")
    else:
        source_lang, target_lang = translation.get_language_pair(sender_id, channel_id)
        print(f"翻訳元言語は{source_lang},翻訳先言語は{target_lang}")

    #入力言語判定
    input_lang = detect(message)
    print(f"入力言語は{input_lang}")
    if input_lang != source_lang:
        flash("身につけたい言語で入力してみよう")
        return redirect(f"/message?channel_id={channel_id}")

    translated_message = translation.translation(message, source_lang, target_lang)
    models.createMessage(message, translated_message, sender_id, channel_id)
    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(sender_id,last_operation_at)
    return redirect("/message?channel_id={channel_id}".format(channel_id = channel_id))



# チャンネル一覧ページの表示
@app.route("/")
def index():
    user_id = session.get("id")
    #user_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    if user_id is None:
        return redirect('/login')
    else:
        channels = models.getChannelByUserId(user_id)
        if channels:
            channels.reverse()

    channel_id = session.get("channel_id")

    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    return render_template('chat.html', channels=channels, channel_id=channel_id)


# チャンネルの追加
# 最終的には"/"にする
@app.route("/channel", methods=["POST"])
def add_channel():
    # sessionからuser_id取得
    user_id = session.get("id")
    #user_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    if user_id is None:
        return redirect("/login")
    channel_name = request.form.get("channel_name")
    id = uuid.uuid4()
    models.addChannel(id, channel_name, user_id)
    models.addToUsersChannels(user_id, id)
    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    return redirect("/")


#メッセージ削除
#編集機能実装するなら関数として切り離して流用するorこの中でif使って編集もやる予定
@app.route('/delete/<message_id>')
def delete_message(message_id):
    user_id = session.get("id")
    #user_id = "35d485b3-f3e0-4b34-84bd-3460487c711e"
    if user_id is None:
        return redirect('/login')

    message_info = models.getMessageById(message_id)
    sender_id = message_info["user_id"]
    channel_id = message_info["channel_id"]

    new_message = "This message has been deleted"
    source_lang, target_lang = translation.get_language_pair(sender_id, channel_id)
    new_message = translation.translation(new_message, "en", source_lang)
    new_translated_message = translation.translation(new_message, "en", target_lang)
    models.changeMessage(new_message, new_translated_message, message_id)

    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    #チャンネルIDをフロントに渡してメッセージ一覧ページに飛ばす
    return redirect(f"/message?channel_id={channel_id}")

@app.route('/logout', methods=["POST"])
def logout():
    user_id = session.get("id")
    if user_id:
        models.changeInactive(user_id)
    session.clear()
    return redirect('/login') #TODO: ログアウトページがあれば/logoutになる


@app.route('/list-user', methods=["GET"])
def get_list_user():
    user_id = session.get("id")
    learning_lang = models.getLearningLanguage(user_id)
    users = models.getOtherLanguageUserList(learning_lang)
    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    return jsonify(users)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(id="check_status", func= models.updateStatus, trigger='interval', hours=1) #一時間に一回ユーザーの操作を確認する
    scheduler.start()
    app.run(host="0.0.0.0", port=5002, debug=True)





