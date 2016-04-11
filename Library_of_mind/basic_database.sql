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
SELECT p.id_type AS ID, p.type AS CHILDREN, s.type AS PARENT, s.id_type AS ID_PARENT FROM types_list p JOIN types_list s ON p.id_parent = s.id_type;
//

CREATE VIEW VIEW_WAITING AS
SELECT id, name, type, id_type, description, key_list, name_a, date_a, name_m, date_m, id_access FROM waiting_list NATURAL JOIN types_list;
//

CREATE VIEW VIEW_LIBRARY AS
SELECT id, name, type, id_type, description, key_list, name_a, date_a, name_m, date_m, id_access FROM library_list NATURAL JOIN types_list;
//

/*----------------------------------
---         Insert into table
----------------------------------*/

INSERT INTO types_list(type) VALUES("LOM");
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(2,"Tools",1);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(3,"Programing",1);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(4,"Books",1);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(5,"Electronic",1);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(6,"Great Project",1);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(7,"Platform",2);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(8,"Tips & Tricks",2);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(9,"Linux",7);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(10,"Windows",7);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(11,"Developer",3);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(12,"Tips & Tricks",11);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(13,"Language",11);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(14,"Web Developer",3);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(15,"Tips & Tricks",14);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(16,"Language",14);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(17,"Arduino",5);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(18,"Project",17);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(19,"RaspberryPi",5);
//
INSERT INTO types_list(id_type, type, id_parent) VALUES(20,"Project",19);
//


INSERT INTO help_list(name, s_name, description) VALUES("ALL","","<tt>Usage:
  <span>s</span>   |  <span>search</span>  -- <span>show row  by pattern</span>
  <span>t</span>   |  <span>type</span>    -- <span>show types by pattern</span>
  <span>k</span>   |  <span>key</span>     -- <span>show keys  by pattern</span>
  <span>a</span>   |  <span>add</span>     -- <span>add row</span>
  <span>u</span>   |  <span>update</span>  -- <span>update row</span>
  <span>n</span>   |  <span>news</span>    -- <span>new row since the last use</span>
  <span>bye</span> |  <span>exit</span>    -- <span>exit WINDOW</span>
  <span>set</span> |  <span>set</span>     -- <span>show/set env</span>
  <span>h</span>   |  <span>help</span>    -- <span>this message</span>
  <span>his</span> |  <span>history</span> -- <span>show history</span>

  <span>More about command use help &lt;command&gt;</span></tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("set","","<tt>Usage:
  <span>set</span>                - show all variable
  <span>set variable value</span> - set variable

Example:
  <span>set history 2000</span>   - change length of stored history
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("search","s","<tt>Usage:
  <span>s[earch]</span>                      - show all row
  <span>s [-i,-n,-t,-d,-k,-a] pattern</span> - show row by pattern
Options:
  -i[d]            - regex pattern by id
  -n[ame]          - regex pattern by name
  -t[ype]          - regex pattern by type
  -d[esc[ription]] - regex pattern by description
  -k[ey]           - regex pattern by key
  -a[utor]         - regex pattern by autor

Double clik or select and press enter - show more info about row

Example:
  <span>s -i [1-10] -k python</span>   - between options is 'OR'
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("add","a","<tt>Usage:
  <span>a[dd]</span>              - add new row (open new window)
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("update","u", "<tt>Usage:
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("type","t","<tt>Usage:
  <span>t[ype]</span>             - show all tree type 
  <span>t[ype] patern</span>      - show tree by patern

Double clik or select and press enter - show all row by this type

Example:
  <span>t language</span>         - show tree language type
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("key","k","<tt>Usage:
  <span>k[ey]</span>             - show all keys
  <span>k[ey] patern</span>      - show keys by patern

Double clik or select and press enter - show all row by this key

Example:
  <span>k python</span>          - show python key
  </tt>
");
//
INSERT INTO help_list(name, s_name, description) VALUES("news","n","<tt>Usage:
  <span>n[ews]</span>             - show new rows that 
                       have been added since your last login
  </tt>
");
//


delimiter ;
