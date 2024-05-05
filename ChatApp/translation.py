from googletrans import Translator
from models import models

#言語コードはISO-639コードに準拠

#Translatorオブジェクトを生成
trans = Translator()


#翻訳
def translation(message, src, dest):
    result = trans.translate(message, src, dest)
    translation_message = result.text
    
    return translation_message


#翻訳言語取得
def get_language_pair(user_id, channel_id):
    source_lang = models.getLearningLang(user_id).get("learning_language") 
    print(f"翻訳元言語は{source_lang}")

    for user in models.getChannelMemberId(channel_id):
        if user["user_id"] != user_id:
            recipient_id = user["user_id"]
            target_lang = models.getLearningLang(recipient_id).get("learning_language")
            break
        else:
            target_lang = models.getNativeLang(user_id).get("learning_language")
            print(target_lang)

    print(f"翻訳先言語は{target_lang}")

    return (source_lang, target_lang)
