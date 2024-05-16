from flask import Flask, redirect, render_template, request, session, flash, jsonify, url_for
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from config import config
import datetime
import hashlib
import uuid
import re

from models import models
import channels
import reload
import renderProfile

import translation
from langdetect import detect


app = Flask(__name__)
app.config.from_object(config.Config)


#サインアップ画面へ遷移
@app.route('/signup')
def signup():
    return render_template('registration/signup.html')


#サインアップ処理
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

    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if(name == "" or email == "" or password1 == "" or password2 == "" or lng == None or learning_lng == None):
        flash("必須項目をすべて入力してください")
        return redirect("/signup")
    elif(password1 != password2):
        flash("同じパスワードを入力してください")
        return redirect("/signup")
    elif(re.match(pattern,email) is None):
        flash("正しいメールアドレスを入力してください")
        return redirect("/signup")
    elif(lng == learning_lng):
        flash("異なる言語を選んでください")
        return redirect("/signup")
    else:
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        user = models.getUser(email)

    if user:
        flash('既に使用されているアドレスです')
        return redirect("/signup")
    else:
        models.create_user(id,name,email,password,lng,learning_lng,country,city,dt,dt,is_active = True)
        UserId = str(id)
        session['id'] = UserId
        return redirect('/login')


#ログイン画面へ遷移
@app.route('/login')
def login():
    return render_template('registration/login.html')


#ログイン処理
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
          return redirect("/login")
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


#メッセージ送信
@app.route('/message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    sender_id = session.get("id")
    channel_id = session.get("channel_id")
    print(channel_id, message)
    
    if sender_id is None:
        return redirect('/login')
    elif channel_id is None:
        flash(translation.flash_trans(sender_id, "チャンネルが選択されていません"))
        return redirect("/")
    elif message == "":
        flash(translation.flash_trans(sender_id, "メッセージが入力されていません"))
        return redirect("/")
    else:
        source_lang, target_lang = translation.get_language_pair(sender_id, channel_id)


    #入力言語判定
    input_lang = detect(message)
    print(f"入力言語は{input_lang}")
    if input_lang != source_lang:
        flash(translation.flash_trans(sender_id, "学びたい言語で入力しよう"))
        return redirect("/")

    translated_message = translation.translation(message, source_lang, target_lang)
    models.createMessage(message, translated_message, sender_id, channel_id)
    models.updateLastMessageAt(channel_id)
    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(sender_id,last_operation_at)
    return redirect("/")


# チャンネル一覧ページの表示
@app.route("/")
def index():
    user_id = session.get("id")
    if user_id is None:
        return redirect('/login')
    else:
        channels = models.getChannelByUserId(user_id)
    channel_id = session.get("channel_id")
    if channel_id is None:
        messages = None
    else:
        messages = models.getMessageAll(channel_id)    
        channels = models.getChannelByUserId(user_id)
 
    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    return render_template('chat.html', user_id=user_id, channel_id=channel_id, channels=channels, messages=messages)


# チャンネルの追加
@app.route("/channel", methods=["POST"])
def add_channel():
    user_id = session.get("id")
    if user_id is None:
        return redirect("/login")
    channel_name = request.form.get("channel_name")
    id = uuid.uuid4()

    models.addChannel(id, channel_name, user_id)
    models.addToMemberships(user_id, id)
    
    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    return redirect("/")


#メッセージ削除
@app.route("/deletemessage", methods=["POST"])
def delete_message():
    user_id = session.get("id")
    if user_id is None:
        return redirect('/login')
    
    message_id = request.form.get("message_id")
    models.deleteMessage(message_id)

    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)

    return redirect("/")


#ログアウト
@app.route('/logout', methods=["POST"])
def logout():
    user_id = session.get("id")
    if user_id:
        models.changeInactive(user_id)
    session.clear()
    return redirect('/login') #TODO: ログアウトページがあれば/logoutになる


#参加可能チャンネル取得
@app.route('/list-user', methods=["GET"])
def get_list_user():
    user_id = session.get("id")
    learning_lang = models.getLearningLanguage(user_id).get('learning_language')
    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    list_user = channels.renderUsers(learning_lang)
    return list_user


#チャンネル選択時HTMLを書き換える
@app.route('/reload')
def message_reload():
    user_id = session.get("id")
    channel_id = request.args.get("channel_id")
    # todo：エラー対処
    # JSにURLを返して遷移する必要があるが今回はHTMLをテキストで渡すので以下はできない
    if user_id is None:
        redirect_url = url_for(login)
        return jsonify({'redirect_url': redirect_url})
    elif channel_id is None:
        channel_id = session.get("channel_id")
        if channel_id is None:
            redirect_url = url_for(login)
            return jsonify({'redirect_url': redirect_url})
    else:
        session["channel_id"] = channel_id

    new_HTML = reload.make_HTML(user_id, channel_id)
    return new_HTML


#条件の合う相手とのマッチング・チャット作成
@app.route('/matching', methods=["POST"])
def matching():
    user_id = session.get("id")
    if user_id is None:
        return redirect('/login')
    
    channel_id = request.form.get("channel_id")

    models.addToMemberships(user_id, channel_id)

    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    
    session["channel_id"] = channel_id

    return redirect("/")


#チャンネル削除
@app.route('/deletechannel', methods=["POST"])
def delete_channel():
    user_id = session.get("id")
    if user_id is None:
        return redirect('/login')
    
    channel_id = request.form.get("channel_id")
    channel_detail = models.getChannelById(channel_id)

    if user_id != channel_detail["user_id"]:
        flash(translation.flash_trans(user_id, "あなたの作ったチャンネルではありません"))
        return redirect("/")
    else:
        models.deletechannel(channel_id)
        session["channel_id"] = None
        return redirect("/")


@app.route('/profile', methods=["GET"])
def get_profile():
    user_id = session.get("id")
    last_operation_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    models.updateLastOperationAt(user_id,last_operation_at)
    profile = renderProfile.renderProfile(user_id)
    return profile


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(id="check_status", func= models.updateStatus, trigger='interval', hours=1) #一時間に一回ユーザーの操作を確認する
    scheduler.start()
    app.run(host="0.0.0.0", port=5002, debug=True)
