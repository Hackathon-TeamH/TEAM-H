from flask import abort
from util.DB import DB

class models:
  def create_user(id,name,email,password,lng,learning_lng,country,city,last_operation_at):
    try:
      connect = DB.getConnection()
      cursor = connect.cursor()
      sql = "INSERT INTO users (id, user_name, email, password, language, learning_language, country, city, last_operation_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
      cursor.execute(sql, (id,name,email,password,lng,learning_lng,country,city,last_operation_at))
      connect.commit()
    except Exception as e:
      print('エラー' + e)
      abort(5000)
    finally:
      cursor.close()from flask import abort
from util.DB import DB


class dbConnect:
    #メッセージ一覧取得
    #channnelidごとに分ける予定
    def getMessageAll():
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT message, translated_message FROM messages;"
            cur.execute(sql)
            messages = cur.fetchall()
            return messages
        except:
            print('Exception1が発生しています')
            abort(500)
        finally:
            cur.close()

    #メッセージ格納
    def createMessage(message, translated_message, user_id, channel_id):
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
            cur.close()

    #翻訳元と翻訳対象言語を取得
    def translationlanguage(id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT language, learning_language FROM users WHERE id = %s;"
            cur.execute(sql, (id))
            lang = cur.fetchall()
            return lang
        except:
            print('Exception3が発生しています')
            abort(500)
        finally:
            cur.close()