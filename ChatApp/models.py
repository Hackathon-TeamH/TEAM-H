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
      cursor.close()