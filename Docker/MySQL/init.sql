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
  last_operation_at DATETIME NOT NULL,
)


INSERT INTO users(id, user_name, password, email, language, learning_language, country, city, last_operation_at) VALUES ("35d485b3-f3e0-4b34-84bd-3460487c711e", "TEST_USER1", "password", "test1@email.com", "jpn", "eng", "日本", "東京", '2024-04-14 22:00:00')
INSERT INTO users(id, user_name, password, email, language, learning_language, country, city, last_operation_at) VALUES ("ab0bf204-3df1-4a52-b14a-89f18e8a8188", "TEST_USER2", "password", "test2@email.com", "eng", "jpn", "US", "LosAngeles", '2024-04-14 22:00:00')