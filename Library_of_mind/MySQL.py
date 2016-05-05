import MySQLdb
from sys import exit
from datetime import datetime
import os
import log

class ConMySQL(object):

    @classmethod
    def __getData(cls, query, *arg):

        data = []
        try:

            db = MySQLdb.connect(ConMySQL.ip, 'lom', 'lom', 'LOM')
            cur = db.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query, arg)
            data = cur.fetchallDict()

        except MySQLdb.Error, e:

            log.LOG("Error %d: %s" % (e.args[0], e.args[1]))
	    self.print_error_message("Error %d: %s" % (e.args[0], e.args[1]))

        finally:

            if cur:
                cur.close()
            if db:
                db.close()
            return data

    @classmethod
    def __setData(cls, query, *arg):

        try:

            db = MySQLdb.connect(ConMySQL.ip, 'lom', 'lom', 'LOM')
            cur = db.cursor()
            cur.execute(query, arg)
            db.commit()

        except MySQLdb.Error, e:

            log.LOG("Error %d: %s" % (e.args[0], e.args[1]))
	    self.print_error_message("Error %d: %s" % (e.args[0], e.args[1]))
	#    raise e

        finally:

            if cur:
                cur.close()
            if db:
                db.close()

    @classmethod
    def getType(cls, pattern=".*"):
    	"""
    Get Types from DB by pattern
    pattern -> regexp"""

        query = "SELECT * FROM types_list where type REGEXP %s"
        return cls.__getData(query, pattern)


    @classmethod
    def getWhereTypeAndParent(cls, text, id_parent):
    	"""
    Get Types from DB by text
    text -> text
    id_parent -> int"""

        query = "SELECT * FROM types_list where type = %s AND id_parent = %s"
        return cls.__getData(query, text, id_parent)

    @classmethod
    def getTypeByTree(cls, pattern=".*"):
    	"""
    Get Types tree from DB by pattern
    pattern -> regexp"""

        query = "SELECT ID, CHILDREN, ID_PARENT, PARENT FROM TYPE_TREE where PARENT REGEXP %s"
        treeData = cls.__getData(query, pattern)

        result = {('LOM', 1L): []}

        for row in treeData:
            child = (row['CHILDREN'], row['ID'])
            parent = (row['PARENT'], row['ID_PARENT'])


            if parent in result.keys():
                result[parent].append(child)
            else:
                result[(parent)] = [child]

        return result

    @classmethod
    def getKeys(cls, pattern=".*"):
    	"""
    Get Keys from DB by pattern
    pattern -> regexp"""

        query = "SELECT * FROM keys_list where key_name REGEXP %s"
        return cls.__getData(query, pattern)

    @classmethod
    def getUniqueKeys(cls, pattern=".*"):
    	"""
    Get unique Keys from DB by pattern
    pattern -> regexp"""

        query = "SELECT DISTINCT key_name FROM keys_list where key_name REGEXP %s"
        return cls.__getData(query, pattern)

    @classmethod
    def getRowByKey(cls, pattern=".*"):
    	"""
    Get row from DB by pattern key
    pattern -> regexp(key)"""

        query = "call show_rows_by_key(%s)"
        return cls.__getData(query, pattern)

    @classmethod
    def getLib(cls, dictPattern={'id':'.*'}, oper='OR', access='ALL'):
    	"""
    Get rows from Library DB
    dictPattern -> dict{column : pattern}
	example {'id' : '[1-5]'} or {'id' : '[1-5]', ''name' : 'RNC'}
    oper -> str['OR', 'AND']
	example oper='AND'
	SQL: query .. where id REGEXP '[1-5]' AND name REGEXP 'RNC'
    access -> str ['All', [$USER]]"""

        query = "SELECT * FROM VIEW_WAITING where id_access = %s AND "

        tmp = []
        for (k,v) in dictPattern.items():
            tmp.append(" %s REGEXP '%s' " % (MySQLdb.escape_string(k), MySQLdb.escape_string(str(v))))
        query += oper.join(tmp)

        return cls.__getData(query, access)

    @classmethod
    def getLibDefaultDick(cls, dictPattern={'id':['.*']}, oper='OR', access='ALL'):
        """
    Get rows from Library DB
    dictPattern -> dict{column : pattern}
	example {'id' : '[1-5]'} or {'id' : '[1-5]', ''name' : 'RNC'}
    oper -> str['OR', 'AND']
	example oper='AND'
	SQL: query .. where id REGEXP '[1-5]' AND name REGEXP 'RNC'
    access -> str ['All', [$USER]]"""

        query = "SELECT * FROM VIEW_WAITING where id_access = %s AND "

        result = []
        for (k,val) in dictPattern.items():
	    for v in val:
	        tmp_query = query + " " + k + " REGEXP %s"
	        result.extend(cls.__getData(tmp_query, access, v))

        return {x['id']: x for x in result}.values()

    @classmethod
    def getWeit(cls, dictPattern={'id':'.*'}, oper='OR', access='ALL'):
    	"""
    Get rows from waiting DB
    dictPattern -> dict{column : pattern}
	example {'id' : '[1-5]'} or {'id' : '[1-5]', ''name' : 'RNC'}
    oper -> str['OR', 'AND']
	example oper='AND'
	SQL: query .. where id REGEXP '[1-5]' AND name REGEXP 'RNC'
    access -> str ['All', [$USER]]"""

        query = "SELECT * FROM VIEW_WAITING where id_access = %s AND "

        tmp = []
        for (k,v) in dictPattern.items():
            tmp.append(" %s REGEXP '%s' " % (MySQLdb.escape_string(k), MySQLdb.escape_string(v)))
        query += oper.join(tmp)

        return cls.__getData(query, access)

    @classmethod
    def getUser(cls, user):
    	"""Get User from DB"""

        query = "SELECT * FROM users_list where user = %s"
        return cls.__getData(query, user)

    @classmethod
    def getNews(cls, user):
    	"""Get News from DB"""

        duser = cls.getUser(user)
	if len(duser) >= 1:
	    duser = cls.getUser(user)[0]
	    query = "SELECT * FROM VIEW_WAITING WHERE date_a > '" + duser['last_log'].strftime("%Y-%m-%d %T") + "'"
	else:
	    cls.updateUser(user)
	    query = "SELECT * FROM VIEW_WAITING WHERE date_a < '1970-01-01 12:00:00'"



        return cls.__getData(query)

    @classmethod
    def getHelp(cls, com='ALL'):
    	"""Get Help from DB"""

        query = "SELECT name, s_name, description FROM help_list WHERE name = %s OR s_name = %s"
        help = cls.__getData(query, com, com)

	if help:
	    return help
	else:
	    return cls.__getData("SELECT name, s_name, description FROM help_list WHERE name = 'ALL'")

    @classmethod
    def setType(cls, name, parent):
    	"""
    Add new type
    name -> str
    parent -> id_type"""

        query = "INSERT INTO types_list(type, id_parent) VALUES(%s, %s)"
        cls.__setData(query, name, parent)

    @classmethod
    def setUser(cls, user):
    	"""Add new user"""

        query = "INSERT INTO users_list(user) VALUES(%s)"
        cls.__setData(query, user)

    @classmethod
    def setRow(cls, name, id_type, description, key_list, user, access='ALL'):
    	"""
    Add new row to waiting
    name -> str
    id_type -> int (refer to type)
    description -> str
    key_list -> str (list keys example: "RNC,,3gsim_Refer" without space)
    user -> str ($USER)
    access -> str ['All', [$USER]]"""

        query = "INSERT INTO waiting_list(name, id_type, id_access, description, key_list, name_a) \
                VALUES(%s, %s, %s, %s, %s, %s)"
        cls.__setData(query, name, id_type, access, description, key_list.replace(' ',''), user)

    @classmethod
    def UpdateLib(cls, dictPattern, row_id, user):
    	"""
    Update row from waiting DB
    dictPattern -> dict{column : string}
	example {'name' : 'new', 'description' : 'new description'}
    id -> str
    user -> str ($USER)"""

        query = "UPDATE waiting_list SET"

        tmp = []
        for (k,v) in dictPattern.items():
	    if str(v).isdigit():
                tmp.append(" %s = %s " % (MySQLdb.escape_string(k), v))
	    else:
                tmp.append(" %s = '%s' " % (MySQLdb.escape_string(k), MySQLdb.escape_string(v)))
        query += ', '.join(tmp) + ", date_m = NOW(), name_m = '" + user + "' WHERE id = " + str(row_id)


        return cls.__setData(query)

    @classmethod
    def updateUser(cls, user):
    	"""Update user last_login"""

	befor_update = cls.getUser(user)
	if not befor_update:
	    cls.setUser(user)
	    query_add_type="INSERT INTO types_list(type, id_parent) SELECT %s, id_type from types_list where type = 'Users' and id_parent = 1;"
            cls.__setData(query_add_type, user)
        query_last_log = "UPDATE users_list SET last_log = NOW() where user = %s"

        cls.__setData(query_last_log, user)
        return befor_update

if __name__ == '__main__':

    ConMySQL.ip = '172.19.20.19'
    #ConMySQL.UpdateLib({'name_a', 'alte'}, 1)
    print ConMySQL.UpdateLib({'name_a': 'alte', 'id_type' : '10'},'1')
    #print ConMySQL.getHelp('ps aux | sort -n -k 6 | awk \'{sum += $6/1024; print $6/1024 " MB\t\t" $11} END {print "Total " sum " MB"}\'')
    print ConMySQL.getLib({'id': '1'},'OR')
    #print ConMySQL.getLib({'name': 'treeview', 'type':'LOM'},'OR')
    #print ConMySQL.getLib({'name':'tam'})
    #print ConMySQL.getUser(os.environ['USER'])
    #print ConMySQL.getTypeByTree()
    #print ConMySQL.getKeys()
    #print ConMySQL.getUniqueKeys()
    #print ConMySQL.getNews(os.environ['USER'])
    #print ConMySQL.updateUser('ps aux | sort -n -k 6 | awk \'{sum += $6/1024; print $6/1024 " MB\t\t" $11} END {print "Total " sum " MB"}\'')
