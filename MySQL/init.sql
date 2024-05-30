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
    created_at DATETIME NOT NULL,
    last_operation_at DATETIME NOT NULL,
    is_active BOOLEAN NOT NULL
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
    user_id varchar(255) REFERENCES users(id),
    last_message_at DATETIME NOT NULL default current_timestamp
);

CREATE TABLE memberships(
    user_id varchar(255) REFERENCES users(id),
    channel_id varchar(255) REFERENCES channels(id) ON DELETE CASCADE
);