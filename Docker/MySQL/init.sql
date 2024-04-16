DROP DATABASE chatapp;
DROP USER 'testuser';


CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    id varchar(255) PRIMARY KEY,
    user_name varchar(255),
    password varchar(255),
    email varchar(255) NOT NULL,
    language varchar(4) NOT NULL,
    learning_language varchar(4) NOT NULL,
    country varchar(128),
    city varchar(128),
    last_operation_at DATETIME NOT NULL
);

CREATE TABLE channels (
    id varchar(255) PRIMARY KEY,
    name varchar(255) NOT NULL,
    created_at DATETIME NOT NULL,
    created_user_id varchar(255) NOT NULL REFERENCES users(id),
    join_user1_id varchar(255) REFERENCES users(id) ON DELETE CASCADE,
    join_user2_id varchar(255) REFERENCES users(id) ON DELETE CASCADE,
    join_flag boolean NOT NULL
);

CREATE TABLE messages (
    id serial PRIMARY KEY,
    message text NOT NULL,
    translated_message text NOT NULL,
    created_at timestamp NOT NULL default current_timestamp,
    user_id varchar(255) REFERENCES users(id),
    channel_id varchar(255) REFERENCES channels(id) ON DELETE CASCADE
);


INSERT INTO users(id, user_name, password, email, language, learning_language, country, city, last_operation_at) VALUES
    ('1', 'Alice', 'password1', 'alice@test.com', 'en', 'ja', 'USA', 'New York', NOW()),
    ('2', '石出', 'password2', 'ishide@test.com', 'ja', 'en', 'Japan', 'Tokyo', NOW());

INSERT INTO channels (id, name, created_at, created_user_id, join_user1_id, join_user2_id, join_flag) VALUES
    ('1', 'Channel 1', NOW(), '1', '1', '2', TRUE),
    ('2', 'Channel 2', NOW(), '2', '2', '1', FALSE);
            
INSERT INTO messages (id, message, translated_message, created_at, user_id, channel_id) VALUES
    ('1', 'Hello', 'こんにちは', NOW(), '1', '1'),
    ('2', 'How are you?', '元気ですか？', NOW(), '2', '1'),
    ('3', 'Nice to meet you.', 'はじめまして。', NOW(), '2', '2');