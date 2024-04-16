from flask import Flask, render_template, request, redirect, url_for

from models import dbConnect
import translation 

app = Flask(__name__)

from googletrans import Translator

  

# チャットページ
@app.route('/')
def index():
    sentmessage = dbConnect.getMessageAll()
    return render_template('index.html', sentmessage=sentmessage)


#チャット送信
@app.route('/', methods=['POST'])
def blank():
    
    #ログイン処理でsessionに入れたidを使う
    #user_id = session.get("id")　
    user_id = 1
    if user_id is None:
        return redirect('/login') #リンク先は要調整

    #チャンネルに入るときにフロントに渡したidをもらう
    #channel_id = request.form.get('channel_id')
    channel_id = 1

    message = request.form.get('message')
    if message is None:
        return redirect('/')

    language_pair = dbConnect.translationlanguage(user_id)
    
    for l in language_pair:
        output_language = l['language']
        input_language = l['learning_language']
    
    translated_message = translation.translation(input_language, output_language, message)
    dbConnect.createMessage(message, translated_message, user_id, channel_id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)