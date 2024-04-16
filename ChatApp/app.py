from flask import Flask, render_template, request, redirect, url_for

from models import dbConnect
import translation 


app = Flask(__name__)
  

# チャットページ
@app.route('/')
def chat():
    sent_message = dbConnect.getMessageAll()
    return render_template('chat.html', sent_message=sent_message)


#チャット送信
@app.route('/', methods=['POST'])
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
    #送信者の学ぶ言語→受信者の学ぶ言語への設定に変更予定
    language_pair = dbConnect.translationlanguage(user_id)
    
    for lang in language_pair:
        src = lang['learning_language']
        dest = lang['language']
    
    translated_message = translation.translation(message, src, dest)
    dbConnect.createMessage(message, translated_message, user_id, channel_id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)