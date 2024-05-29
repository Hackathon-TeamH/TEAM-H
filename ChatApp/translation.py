from googletrans import Translator
from models import models

#言語コードはISO-639コードに準拠

#Translatorオブジェクトを生成
trans = Translator()


#翻訳
def translation(message, src, dest):
    result = trans.translate(message, src=src, dest=dest)
    translation_message = result.text
    
    return translation_message


#翻訳言語取得
def get_language_pair(user_id, channel_id):
    source_lang = models.getLearningLanguage(user_id).get("learning_language") 
    for user in models.getChannelMemberId(channel_id):
        if user["user_id"] != user_id:
            recipient_id = user["user_id"]
            target_lang = models.getLearningLanguage(recipient_id).get("learning_language")
            break
        else:
            target_lang = models.getNativeLanguage(user_id).get("language")

    return (source_lang, target_lang)


#flashメッセージ翻訳
def flash_trans(user_id,alertmessage):
        learning_lang = models.getLearningLanguage(user_id)
        target_lang = learning_lang["learning_language"]
        alert = translation(alertmessage, "ja", target_lang)
        return alert


# googletransでの言語判定
def google_detect(message):
     detect = trans.detect(message)
     lang = detect.lang
     return lang

