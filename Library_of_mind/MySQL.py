import MySQLdb
from sys import exit
from datetime import datetime
import os

class ConMySQL(object):

    @classmethod
    def __getData(cls, query):

        data = []
        try:

            db = MySQLdb.connect('172.19.20.19', 'lom', 'lom', 'LOM')

            cur = db.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            data = cur.fetchallDict()

        except MySQLdb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])

        finally:

            if cur:
                cur.close()
            if db:
                db.close()
            return data

    @classmethod
    def __setData(cls, query):

        try:

            db = MySQLdb.connect('172.19.20.19', 'lom', 'lom', 'LOM')

            cur = db.cursor()
            cur.execute(query)
            db.commit()

        except MySQLdb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
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

        query = "SELECT * FROM types_list where type REGEXP '" + pattern + "'"
        return cls.__getData(query)


    @classmethod
    def getWhereTypeAndParent(cls, text, id_parent):
    	"""
    Get Types from DB by text
    text -> text
    id_parent -> int"""

        query = "SELECT * FROM types_list where type = '" + text + "' AND id_parent = " + str(id_parent)
        return cls.__getData(query)

    @classmethod
    def getTypeByTree(cls, pattern=".*"):
    	"""
    Get Types tree from DB by pattern
    pattern -> regexp"""

        query = "SELECT ID, CHILDREN, ID_PARENT, PARENT FROM TYPE_TREE where PARENT REGEXP '" + pattern + "'"
        treeData = cls.__getData(query)

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

        query = "SELECT * FROM keys_list where key_name REGEXP '" + pattern + "'"
        return cls.__getData(query)

    @classmethod
    def getUniqueKeys(cls, pattern=".*"):
    	"""
    Get unique Keys from DB by pattern
    pattern -> regexp"""

        query = "SELECT DISTINCT key_name FROM keys_list where key_name REGEXP '" + pattern + "'"
        return cls.__getData(query)

    @classmethod
    def getRowByKey(cls, pattern=".*"):
    	"""
    Get row from DB by pattern key
    pattern -> regexp(key)"""

        query = "call show_rows_by_key('" + pattern + "')"
        return cls.__getData(query)

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

        query = "SELECT * FROM VIEW_WAITING where id_access = '" + access + "' AND "

        tmp = []
        for (k,v) in dictPattern.items():
            tmp.append(" %s REGEXP '%s' " % (k,v))
        query += oper.join(tmp)

        return cls.__getData(query)

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

        query = "SELECT * FROM VIEW_WAITING where id_access = '" + access + "' AND "

        tmp = []
        for (k,v) in dictPattern.items():
            tmp.append(" %s REGEXP '%s' " % (k,v))
        query += oper.join(tmp)

        return cls.__getData(query)

    @classmethod
    def getUser(cls, user):
    	"""Get User from DB"""

        query = "SELECT * FROM users_list where user = '" + user + "'"
        return cls.__getData(query)

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

        query = "SELECT name, s_name, description FROM help_list WHERE name = '" + com + "' OR s_name = '" + com + "'"
        help = cls.__getData(query)

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

        query = "INSERT INTO types_list(type, id_parent) VALUES('" + name + "'," + str(parent) + ")"
        cls.__setData(query)

    @classmethod
    def setUser(cls, user):
    	"""Add new user"""

        query = "INSERT INTO users_list(user) VALUES('" + user + "')"
        cls.__setData(query)

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
                VALUES('%s', %s, '%s', '%s', '%s', '%s')" % (name, id_type, access, description, key_list.replace(' ',''), user)
        cls.__setData(query)

    @classmethod
    def updateUser(cls, user):
    	"""Update user last_login"""

	befor_update = cls.getUser(user)
	if not befor_update:
	    cls.setUser(user)
        query_last_log = "UPDATE users_list SET last_log = NOW() where user = '" + user + "'"

        cls.__setData(query_last_log)
        return befor_update

if __name__ == '__main__':

    print ConMySQL.getLib({'name': 'rnc', 'type':'LOM'},'OR')
    print ConMySQL.getLib({'name':'tam'})
    print ConMySQL.getUser(os.environ['USER'])
    print ConMySQL.getTypeByTree()
    print ConMySQL.getKeys()
    print ConMySQL.getUniqueKeys()
    print ConMySQL.getNews(os.environ['USER'])
    print ConMySQL.updateUser('ealatet')
