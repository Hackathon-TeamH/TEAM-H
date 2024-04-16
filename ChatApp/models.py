import pymysql
from flask import abort
from util.DB import DB


class dbConnect:
    def getMessageAll():
        #cur = None  # tryブロックの外でcurをNoneで初期化
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT message, translated_message FROM messages;"
            cur.execute(sql)
            messages = cur.fetchall() #タプルで1行ずつ返す
            return messages
        except:
            print('Exception1が発生しています')
            abort(500)
        finally:
            #if cur is not None:  # curがNoneでないことを確認してからcloseを呼び出す
            cur.close()


    def createMessage(message, translated_message, user_id, channel_id):
        #cur = None  # tryブロックの外でcurをNoneで初期化
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(message, translated_message, user_id, channel_id) VALUES(%s, %s, %s, %s)"
            cur.execute(sql, (message, translated_message, user_id, channel_id))
            conn.commit()
        except:
            print('Exception2が発生しています')
            abort(500)
        finally:
            #if cur is not None:  # curがNoneでないことを確認してからcloseを呼び出す
            cur.close()

    def translationlanguage(id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT language, learning_language FROM users WHERE id = %s;"
            cur.execute(sql, (id))
            lang = cur.fetchall() #タプルで1行ずつ返す
            return lang
        except:
            print('Exception3が発生しています')
            abort(500)
        finally:
            #if cur is not None:  # curがNoneでないことを確認してからcloseを呼び出す
            cur.close()