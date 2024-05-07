DROP DATABASE chatapp;
DROP USER 'testuser';


CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users(
  id varchar(255) PRIMARY KEY,
  user_name varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  email varchar(255) UNIQUE NOT NULL,
  language varchar(4) NOT NULL,
  learning_language varchar(4) NOT NULL,
  country varchar(128),
  city varchar(128),
  last_operation_at DATETIME NOT NULL
);


CREATE TABLE messages (
    id serial PRIMARY KEY,
    message text NOT NULL,
    translated_message text NOT NULL,
    created_at timestamp NOT NULL default current_timestamp,
    user_id varchar(255) REFERENCES users(id),
    channel_id varchar(255) REFERENCES channels(id) ON DELETE CASCADE
);

CREATE TABLE channels(
  id varchar(255) PRIMARY KEY,
  channel_name varchar(255) NOT NULL,
  created_at DATETIME NOT NULL default current_timestamp,
  user_id varchar(255) REFERENCES users(id)
);

CREATE TABLE memberships(
  user_id varchar(255) REFERENCES users(id),
  channel_id varchar(255) REFERENCES channels(id)
);

-- ハッシュ化後のパスワードを登録する必要がありそう（未対応）
INSERT INTO users(id, user_name, password, email, language, learning_language, country, city, last_operation_at) VALUES ("35d485b3-f3e0-4b34-84bd-3460487c711e", "TEST_USER1", "password", "test1@email.com", "ja", "en", "日本", "東京", '2024-04-14 22:00:00');
INSERT INTO users(id, user_name, password, email, language, learning_language, country, city, last_operation_at) VALUES ("ab0bf204-3df1-4a52-b14a-89f18e8a8188", "TEST_USER2", "password", "test2@email.com", "en", "ja", "US", "LosAngeles", '2024-04-14 22:00:00');

INSERT INTO messages (id, message, translated_message, created_at, user_id, channel_id) VALUES
    ("1", "Hello", "こんにちは", NOW(), "35d485b3-f3e0-4b34-84bd-3460487c711e", "1"),
    ("2", "How are you?", "元気ですか？", NOW(), "35d485b3-f3e0-4b34-84bd-3460487c711e", "2"),
    ("3", "Nice to meet you.", "はじめまして。", NOW(), "ab0bf204-3df1-4a52-b14a-89f18e8a8188", "2");

INSERT INTO channels(id, channel_name, created_at, user_id) VALUES
    ("1", "TEST_CHANNEL1", NOW(), "35d485b3-f3e0-4b34-84bd-3460487c711e"),
    ("2", "TEST_CHANNEL2", NOW(), "ab0bf204-3df1-4a52-b14a-89f18e8a8188"),
    ("3", "ほうれんそう", NOW(), "35d485b3-f3e0-4b34-84bd-3460487c711e"),
    ("4", "小松菜", NOW(), "35d485b3-f3e0-4b34-84bd-3460487c711e"),
    ("5", "チンゲン菜", NOW(), "35d485b3-f3e0-4b34-84bd-3460487c711e"),
    ("6", "配管工に赤い帽子は必要なのか", NOW(), "35d485b3-f3e0-4b34-84bd-3460487c711e");

INSERT INTO memberships(user_id, channel_id) VALUES
    ("35d485b3-f3e0-4b34-84bd-3460487c711e", "1"),
    ("35d485b3-f3e0-4b34-84bd-3460487c711e", "2"),
    ("ab0bf204-3df1-4a52-b14a-89f18e8a8188", "2"),
    ("35d485b3-f3e0-4b34-84bd-3460487c711e", "3"),
    ("35d485b3-f3e0-4b34-84bd-3460487c711e", "4"),
    ("35d485b3-f3e0-4b34-84bd-3460487c711e", "5"),
    ("35d485b3-f3e0-4b34-84bd-3460487c711e", "6");