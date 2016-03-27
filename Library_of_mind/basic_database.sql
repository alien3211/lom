DROP TABLE IF EXISTS keys_list;
DROP TABLE IF EXISTS waiting_list;
DROP TABLE IF EXISTS library_list;
DROP TABLE IF EXISTS types_list;
DROP TABLE IF EXISTS users_list;
DROP TABLE IF EXISTS log;
DROP TABLE IF EXISTS help_list;

DROP TRIGGER IF EXISTS update_news;

DROP VIEW IF EXISTS TYPE_TREE;
DROP VIEW IF EXISTS VIEW_WAITING;
DROP VIEW IF EXISTS VIEW_LIBRARY;

DROP PROCEDURE IF EXISTS show_rows_by_key;
DROP PROCEDURE IF EXISTS insert_role;

delimiter //



/*----------------------------------
---         Create Table
----------------------------------*/
CREATE TABLE types_list (
    id_type INTEGER NOT NULL AUTO_INCREMENT,
    type TEXT,
    id_parent INTEGER DEFAULT NULL,
    PRIMARY KEY (id_type),
    KEY types (id_parent),
    CONSTRAINT types FOREIGN KEY (id_parent) REFERENCES types_list (id_type)
);
//

CREATE TABLE users_list (
    user VARCHAR(50),
    date_s TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_log TIMESTAMP NULL DEFAULT NULL,
    if_new INT,
    PRIMARY KEY (user)
);
//


CREATE TABLE waiting_list (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name varchar(255) UNIQUE NOT NULL,
    id_type INTEGER NOT NULL,
    id_access VARCHAR(50) DEFAULT 'ALL',
    description TEXT NOT NULL,
    key_list TEXT NOT NULL,
    name_a TEXT NOT NULL,
    date_a TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name_m VARCHAR(50) DEFAULT NULL,
    date_m TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_type) REFERENCES types_list (id_type)
);
//

CREATE TABLE library_list (
    id INTEGER NOT NULL AUTO_INCREMENT,
    name varchar(255) UNIQUE NOT NULL,
    id_type INTEGER NOT NULL,
    id_access VARCHAR(50) DEFAULT 'ALL',
    description TEXT NOT NULL,
    key_list TEXT NOT NULL,
    name_a TEXT NOT NULL,
    date_a TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    name_m VARCHAR(50) DEFAULT NULL,
    date_m TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (id_type) REFERENCES types_list (id_type)
);
//

CREATE TABLE log (
    user TEXT,
    name TEXT,
    mod_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
//

CREATE TABLE keys_list(
    key_name VARCHAR(255),
    id_lib INTEGER,
    PRIMARY KEY (key_name, id_lib),
    FOREIGN KEY (id_lib) REFERENCES library_list (id)
);
//

CREATE TABLE help_list(
    id INTEGER NOT NULL AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    s_name VARCHAR(5) NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (id)
);
//

/*----------------------------------
---         Create INDEX
----------------------------------*/

CREATE INDEX wait_name ON waiting_list(name);
//
CREATE INDEX wait_type ON waiting_list(id_type);
//
CREATE INDEX lib_name ON library_list(name);
//
CREATE INDEX lib_type ON library_list(id_type);
//

/*----------------------------------
---        Create PROCEDURE
----------------------------------*/
CREATE PROCEDURE insert_role(in RoleID INT, in MenuID VARCHAR(500))
BEGIN
    DECLARE idx, prev_idx INT;
    DECLARE v_id VARCHAR(20);
    DECLARE tmp_n VARCHAR(20) DEFAULT NULL;

    SET idx := locate(',', MenuID,1);
    SET prev_idx := 1;

    WHILE idx > 0 DO
        SET v_id := substr(MenuID, prev_idx, idx-prev_idx);
	insert into keys_list VALUES(v_id, RoleID);
        SET prev_idx := idx+1;
        SET idx := locate(',',MenuID,prev_idx);
    END WHILE;

    SET v_id := substr(MenuID, prev_idx);
    INSERT INTO keys_list VALUES(v_id, RoleID);
END
//

CREATE PROCEDURE show_rows_by_key(in key_n VARCHAR(500))
BEGIN
    select VIEW_LIBRARY.* FROM (SELECT DISTINCT id_lib FROM keys_list WHERE LOWER(key_name) REGEXP LOWER(key_n)) AS id_key_list LEFT JOIN VIEW_LIBRARY ON id_key_list.id_lib = VIEW_LIBRARY.id;
END
//

/*----------------------------------
---         Create TRIGGER
----------------------------------*/

CREATE TRIGGER update_news AFTER INSERT ON waiting_list
FOR EACH ROW
BEGIN
    UPDATE users_list SET if_new = 1;
    INSERT INTO log(user, name) VALUES (NEW.name_a, NEW.name);
    INSERT INTO library_list select * from waiting_list where id = NEW.id;
    CALL insert_role(NEW.id, NEW.key_list);
END;
//

/*----------------------------------
---         Create VIEW
----------------------------------*/

CREATE VIEW TYPE_TREE AS
SELECT p.id_type AS ID, p.type AS CHILDREN, s.type AS PARENT FROM types_list p JOIN types_list s ON p.id_parent = s.id_type;
//

CREATE VIEW VIEW_WAITING AS
SELECT id, name, type, description, key_list, name_a, date_a, name_m, date_m, id_access FROM waiting_list NATURAL JOIN types_list;
//

CREATE VIEW VIEW_LIBRARY AS
SELECT id, name, type, description, key_list, name_a, date_a, name_m, date_m, id_access FROM library_list NATURAL JOIN types_list;
//

/*----------------------------------
---         Insert into table
----------------------------------*/

INSERT INTO types_list(type) VALUES("LOM");
//
INSERT INTO help_list(name, s_name, description) VALUES("ALL","","");
//
INSERT INTO help_list(name, s_name, description) VALUES("set","","");
//
INSERT INTO help_list(name, s_name, description) VALUES("search","s","");
//
INSERT INTO help_list(name, s_name, description) VALUES("add","a","");
//
INSERT INTO help_list(name, s_name, description) VALUES("update","u", "");
//
INSERT INTO help_list(name, s_name, description) VALUES("type","t","");
//
INSERT INTO help_list(name, s_name, description) VALUES("key","k","");
//
INSERT INTO help_list(name, s_name, description) VALUES("news","n","");
//



delimiter ;
