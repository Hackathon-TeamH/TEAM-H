import uuid
from datetime import timedelta

class Config:
    SECRET_KEY = uuid.uuid4().hex
    # セッションの時間はオンライン判別に必要になるため変更予定
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)