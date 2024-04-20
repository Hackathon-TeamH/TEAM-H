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
      print('エラー:' + e)
      abort(5000)
    finally:
      cursor.close()

  def getUser(email):
    try:
      connect = DB.getConnection()
      cursor = connect.cursor()
      sql = "SELECT * FROM user WHERE email=%s;"
      cursor.execute(sql, (email))
      user = cursor.fetchone()
      return user
    except Exception as e:
      print('エラー:' + e)
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
      print('エラー:' + e)
      abort(500)
    finally:
      cursor.close()