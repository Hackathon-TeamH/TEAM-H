from flask import abort
from util.db import DB
from datetime import datetime, timedelta

class models:
    def create_user(id,name,email,password,lang,learning_lang,country,city,created_at,last_operation_at,is_active):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "INSERT INTO users (id, user_name, email, \
                password, language, learning_language, country, \
                city,created_at, last_operation_at,is_active\
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (id,name,email,password,lang,learning_lang,country,city,created_at,last_operation_at,is_active))
            connect.commit()
        except Exception as e:
            abort(500)
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
            abort(500)
        finally:
            cursor.close()

    def getUserWithId(id):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "SELECT * FROM users WHERE id=%s;"
            cursor.execute(sql, (id))
            user = cursor.fetchone()
            return user
        except Exception as e:
            abort(500)
        finally:
            cursor.close()

    # 最後に操作した日時を更新
    def updateLastOperationAt(id,last_operation_at):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "UPDATE users SET last_operation_at=%s, is_active=1 WHERE id=%s;"
            cursor.execute(sql, (last_operation_at,id))
            connect.commit()
        except Exception as e:
            abort(500)
        finally:
            cursor.close()


    #メッセージ一覧取得
    def getMessageAll(channel_id):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "SELECT m.id, user_id, user_name, message, translated_message, m.created_at "\
                "FROM messages AS m INNER JOIN users AS u ON m.user_id = u.id "\
                "WHERE channel_id = %s "\
                "ORDER BY created_at ASC"\
            ";"
            cursor.execute(sql, (channel_id))
            messages = cursor.fetchall()
            return messages
        except Exception as e:
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
            abort(500)
        finally:
            cur.close()

    #指定したユーザーが参加しているチャンネルを取得
    def getChannelByUserId(user_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT channel_id, channel_name, created_at, last_message_at "\
                "FROM memberships AS ms INNER JOIN channels AS c ON ms.channel_id = c.id "\
                "WHERE ms.user_id = %s "\
                "ORDER BY last_message_at DESC"\
            ";"
            cur.execute(sql, (user_id))
            channel = cur.fetchall()
            return channel
        except Exception as e:
            abort(500)
        finally:
            cur.close()

    # チャンネル名にUNIQUE制約を課さないなら不要？
    def getChannelByName(channel_name):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE channel_name=%s;"
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
            return channel
        except Exception as e:
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
            abort(500)
        finally:
            cur.close()

    # membershipsテーブルに追加
    def addToMemberships(user_id, channel_id):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO memberships(user_id, channel_id) VALUES(%s, %s);"
            cur.execute(sql, (user_id, channel_id))
            conn.commit()
        except Exception as e:
            abort(500)
        finally:
            cur.close()


    #membershipsテーブルからそのチャンネルにいるユーザーを取得
    def getChannelMemberId(channel_id):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "SELECT user_id FROM memberships WHERE channel_id = %s;"
            cursor.execute(sql, (channel_id))
            members = cursor.fetchall()
            return members
        except Exception as e:
            abort(500)
        finally:
            cursor.close()


    # 最後にメッセージが送信された日時を更新
    def updateLastMessageAt(id):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "UPDATE channels SET last_message_at=NOW() WHERE id=%s;"
            cursor.execute(sql, (id))
            connect.commit()
        except Exception as e:
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
            abort(500)
        finally:
            cursor.close()

    #話せる言語を取得
    def getNativeLanguage(user_id):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "SELECT language FROM users WHERE id = %s;"
            cursor.execute(sql, (user_id))
            dest_lang = cursor.fetchone()
            return dest_lang
        except Exception as e:
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
            abort(500)
        finally:
            cursor.close()


    #メッセージ削除
    def deleteMessage(message_id):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "DELETE FROM messages WHERE id=%s;"
            cursor.execute(sql, (message_id))
            connect.commit()
        except Exception as e:
            abort(500)
        finally:
            cursor.close()


    def changeInactive(id):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "UPDATE users SET is_active=%s WHERE id=%s;"
            cursor.execute(sql, (0,id,))
            connect.commit()
        except Exception as e:
            abort(500)
        finally:
            cursor.close()

    def updateStatus():
        threshold_time = datetime.now() - timedelta(hours=1)
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "UPDATE users SET is_active = 0 WHERE last_operation_at < %s;"
            cursor.execute(sql, (threshold_time,))
            connect.commit()
        except Exception as e:
            abort(500)
        finally:
            cursor.close()

    def getOtherLanguageUserList(lang):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE language=%s AND is_active=1;"
            cur.execute(sql, (lang))
            users = cur.fetchall()
            return users
        except Exception as e:
            abort(500)
        finally:
            cur.close()

        
    #チャンネル削除
    def deletechannel(channel_id):
        try:
            connect = DB.getConnection()
            cursor = connect.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cursor.execute(sql, (channel_id))
            connect.commit()
        except Exception as e:
            abort(500)
        finally:
            cursor.close()

