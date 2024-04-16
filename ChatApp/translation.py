from googletrans import Translator

#言語コードはISO-639コードに準拠

#Translatorオブジェクトを生成
trans = Translator()

def translation(message, src, dest):
    result = trans.translate(message, src, dest)
    translation_message = result.text
    
    return translation_message


    