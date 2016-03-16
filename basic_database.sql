DROP TABLE IF EXISTS USERS;
DROP TABLE IF EXISTS WAITING;
DROP TABLE IF EXISTS LIBRARY;
DROP TABLE IF EXISTS TYPES;
DROP TABLE IF EXISTS KEYS;
DROP TABLE IF EXISTS LOG;

CREATE TABLE TYPES
    (id_type INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    id_parent INTEGER REFERENCES TYPES(id_type));


CREATE TABLE USERS
    (user TEXT PRIMARY KEY,
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
    id_access TEXT DEFAULT 'ALL',
    description TEXT,
    key TEXT,
    name_a TEXT,
    date_a DATE DEFAULT (datetime('now')),
    name_m TEXT DEFAULT NULL,
    date_m DATE DEFAULT NULL);

CREATE TABLE LIBRARY
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    id_type INTEGER REFERENCES TYPES(id_type),
    id_access TEXT DEFAULT 'ALL',
    description TEXT,
    key TEXT,
    name_a TEXT,
    date_a DATE DEFAULT (datetime('now')),
    name_m TEXT DEFAULT NULL,
    date_m DATE DEFAULT NULL);

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

CREATE VIEW TYPE_TREE AS
SELECT p.type AS CHILDREN, s.type AS PARENT FROM TYPES p JOIN TYPES s ON p.id_parent = s.id_type;

CREATE VIEW VIEW_WAITING AS
SELECT id, name, type, description, key, name_a, date_a, name_m, date_m FROM WAITING NATURAL JOIN types WHERE id_access = 'ALL';

CREATE VIEW VIEW_LIBRARY AS
SELECT id, name, type, description, key, name_a, date_a, name_m, date_m FROM LIBRARY NATURAL JOIN types WHERE id_access = 'ALL';


INSERT INTO TYPES(type) VALUES("LOM");
