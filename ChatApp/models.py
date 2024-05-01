from flask import abort
from util.db import DB

class models:
  def create_user(id,name,email,password,lng,learning_lng,country,city,last_operation_at):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "INSERT INTO users (id, user_name, email, password, language, learning_language, country, city, last_operation_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
          cursor.execute(sql, (id,name,email,password,lng,learning_lng,country,city,last_operation_at))
          connect.commit()
      except Exception as e:
          print(f"エラー: {e}")
          abort(5000)
      finally:
          cursor.close()

  def getUser(email):
    try:
      connect = DB.getConnection()
      cursor = connect.cursor()
      sql = "SELECT * FROM users WHERE email=%s;"
      cursor.execute(sql, (email))
      user = cursor.fetchone()
      return user
    except Exception as e:
      print(f"エラー: {e}")
      abort(500)
    finally:
      cursor.close()

  # 最後に操作した日時を更新
  def updateLastOperationAt(id,last_operation_at):
    try:
      connect = DB.getConnection()
      cursor = connect.cursor()
      sql = "UPDATE users SET last_operation_at=%s WHERE id=%s;"
      cursor.execute(sql, (last_operation_at,id))
      user = cursor.fetchone()
      return user
    except Exception as e:
      print(f"エラー: {e}")
      abort(500)
    finally:
      cursor.close()

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
  def translationLanguage(id):
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

  #チャンネル一覧取得
  def getChannelAll():
    try:
        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM channels;"
        cur.execute(sql)
        channels = cur.fetchall()
        return channels
    except Exception as e:
        print(f"エラー: {e}")
        abort(500)
    finally:
        cur.close()         
  
  #指定したchannel_idに対応するチャンネルを取得
  def getChannelById(channel_id):
    try:
        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM channels WHERE channel_id=%S;"
        cur.execute(sql, (channel_id))
        channel = cur.fetchone()
        return channel
    except Exception as e:
        print(f"エラー: {e}")
        abort(500)
    finally:
        cur.close()
 
  #指定したユーザーが参加しているチャンネルを取得
  def getChannelByUserId(user_id):
    try:
        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM users_channels WHERE user_id=%S;"
        cur.execute(sql, (user_id))
        channel = cur.fetchall()
        return channel
    except Exception as e:
        print(f"エラー: {e}")
        abort(500)
    finally:
        cur.close()

#   チャンネル名にUNIQUE制約を課さないなら不要？      
  def getChannelByName(channel_name):
    try:
        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM channels WHERE channel_name=%S;"
        cur.execute(sql, (channel_name))
        channel = cur.fetchone()
        return channel
    except Exception as e:
        print(f"エラー: {e}")
        abort(500)
    finally:
        cur.close()

  def addChannel(id, channel_name, user_id):
    try:
        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "INSERT INTO channels(id, channel_name, user_id) VALUES(%s, %s, %s);"
        cur.execute(sql, (id, channel_name, user_id))
        conn.commit()
    except Exception as e:
        print(f"エラー: {e}")
        abort(500)
    finally:
        cur.close()

# users_channelsテーブルに追加
  def addToUsersChannels(user_id, channel_id):
    try:
        conn = DB.getConnection()
        cur = conn.cursor()
        sql = "INSERT INTO users_channels(user_id, channel_id) VALUES(%s, %s);"
        cur.execute(sql, (user_id, channel_id))
        conn.commit()
    except Exception as e:
        print(f"エラー: {e}")
        abort(500)
    finally:
        cur.close()

     