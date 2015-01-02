DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS WAITING;
DROP TABLE IF EXISTS LIBRARY;
DROP TABLE IF EXISTS TYPES;
DROP TABLE IF EXISTS ACCESS;
DROP TABLE IF EXISTS KEYS;

CREATE TABLE ACCESS
    (id_access INTEGER PRIMARY KEY AUTOINCREMENT,
    access TEXT);

CREATE TABLE TYPES
    (id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT);

CREATE TABLE USERS 
    (user TEXT PRIMARY KEY,
    id_access INTEGER REFERENCES ACCESS(id_access),
    date_s DATE DEFAULT (datetime('now')),
    last_log DATE DEFAULT (datetime('now')),
    if_new INT);

CREATE TABLE KEYS
    (key TEXT PRIMARY KEY,
    id_lib TEXT);

CREATE TABLE WAITING
    (id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    id_type INTEGER REFERENCES TYPES(id_type),
    id_access INTEGER REFERENCES ACCESS(id_access),
    description TEXT,
    key TEXT,
    name_a TEXT,
    data_a DATE DEFAULT (datetime('now')),
    name_m TEXT DEFAULT NULL,
    data_m DATE DEFAULT NULL);

CREATE TABLE LIBRARY
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    id_type INTEGER REFERENCES TYPES(id_type),
    id_access INTEGER REFERENCES ACCESS(id_access),
    description TEXT,
    key TEXT,
    name_a TEXT,
    data_a DATE DEFAULT (datetime('now')),
    name_m TEXT DEFAULT NULL,
    data_m DATE DEFAULT NULL);

CREATE TABLE LOG
    (user TEXT,
    name TEXT,
    mod_date DATE DEFAULT (datetime('now')));

CREATE INDEX wait_name ON WAITING(name);
CREATE INDEX wait_type ON WAITING(id_type);
CREATE INDEX lib_name ON WAITING(name);
CREATE INDEX lib_type ON WAITING(id_type);

CREATE TRIGGER update_news AFTER INSERT ON WAITING
BEGIN
UPDATE USERS SET if_new = 1;
INSERT INTO LOG(user, name) VALUES (NEW.name_a, NEW.name);
END;
