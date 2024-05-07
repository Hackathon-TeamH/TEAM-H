from flask import abort
from util.db import DB

class models:
  def create_user(id,name,email,password,lang,learning_lang,country,city,last_operation_at):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "INSERT INTO users (id, user_name, email, password, language, learning_language, country, city, last_operation_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
          cursor.execute(sql, (id,name,email,password,lang,learning_lang,country,city,last_operation_at))
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
  def getMessageAll(channel_id):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "SELECT m.id, user_id, user_name, message, translated_message, created_at "\
              "FROM messages AS m INNER JOIN users AS u ON m.user_id = u.id "\
              "WHERE channel_id = %s "\
              "ORDER BY created_at ASC"\
          ";"
          cursor.execute(sql, (channel_id))
          messages = cursor.fetchall()
          return messages
      except Exception as e:
          print(f"エラー: {e}")
          abort(500)
      finally:
          cursor.close()

  #メッセージ格納
  def createMessage(message, translated_message, user_id, channel_id):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "INSERT INTO messages(message, translated_message, user_id, channel_id) VALUES(%s, %s, %s, %s)"
          cursor.execute(sql, (message, translated_message, user_id, channel_id))
          connect.commit()
      except Exception as e:
          print(f"エラー: {e}")
          abort(500)
      finally:
          cursor.close()


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
        sql = "SELECT * FROM channels WHERE id=%s;"
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
        sql = "SELECT * FROM memberships WHERE user_id=%s;"
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
        sql = "SELECT * FROM channels WHERE channel_name=%s;"
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
        sql = "INSERT INTO memberships(user_id, channel_id) VALUES(%s, %s);"
        cur.execute(sql, (user_id, channel_id))
        conn.commit()
    except Exception as e:
        print(f"エラー: {e}")
        abort(500)
    finally:
        cur.close()


 #user_channnelテーブルからそのチャンネルにいるユーザーを取得
  def getChannelMemberId(channel_id):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "SELECT user_id FROM memberships WHERE channel_id = %s;"
          cursor.execute(sql, (channel_id))
          members = cursor.fetchall()
          return members
      except Exception as e:
          print(f"エラー: {e}")
          abort(500)
      finally:
          cursor.close()


  #学びたい言語を取得
  def getLearningLanguage(user_id):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "SELECT learning_language FROM users WHERE id = %s;"
          cursor.execute(sql, (user_id))
          src_lang = cursor.fetchone()
          return src_lang
      except Exception as e:
          print(f"エラー: {e}")
          abort(500)
      finally:
          cursor.close()

  #話せる言語を取得          
  def getNativeLanguage(user_id):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "SELECT learning_language FROM users WHERE id = %s;"
          cursor.execute(sql, (user_id))
          dest_lang = cursor.fetchone()
          return dest_lang
      except Exception as e:
          print(f"エラー: {e}")
          abort(500)
      finally:
          cursor.close()


   #メッセージIDからメッセージ取得
  def getMessageById(message_id):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "SELECT user_id, channel_id FROM messages WHERE id=%s;"
          cursor.execute(sql, (message_id))
          message_info = cursor.fetchone()
          return message_info
      except Exception as e:
          print(f"エラー:{e}")
          abort(500)
      finally:
          cursor.close()


  #メッセージ編集
  def changeMessage(new_message, new_translated_message, message_id):
      try:
          connect = DB.getConnection()
          cursor = connect.cursor()
          sql = "UPDATE messages SET message=%s, translated_message=%s WHERE message_id=%s;"
          cursor.execute(sql, (new_message, new_translated_message, message_id))
          connect.commit()
      except Exception as e:
          print(f"エラー:{e}")
          abort(500)
      finally:
          cursor.close()


 
     