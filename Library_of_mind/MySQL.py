import MySQLdb
from sys import exit
import os

class ConMySQL(object):

    @classmethod
    def __getData(cls, query):

        data = []
        try:

            db = MySQLdb.connect('localhost', 'root', 'Murzyn12321', 'LOM')

            cur = db.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(query)
            data = cur.fetchallDict()
            cur.commit()

        except MySQLdb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            exit(1)

        finally:

            if cur:
                cur.close()
            if db:
                db.close()
            return data

    @classmethod
    def __setData(cls, query):

        try:

            db = MySQLdb.connect('localhost', 'root', 'Murzyn12321', 'LOM')

            cur = db.cursor()
            cur.execute(query)
            db.commit()

        except MySQLdb.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            exit(1)

        finally:

            if cur:
                cur.close()
            if db:
                db.close()

    @classmethod
    def getType(cls, pattern):
        
        query = "SELECT * FROM types_list where type REGEXP '" + pattern + "'"
        return cls.__getData(query)

    @classmethod
    def getKey(cls, pattern):
        query = "call show_rows_by_key('" + pattern + "')"
        return cls.__getData(query)

    @classmethod
    def getLib(cls, dictPattern={'id':'.*'}, oper='OR'):
        query = "SELECT * FROM VIEW_LIBRARY where"
        
        tmp = []
        for (k,v) in dictPattern.items():
            tmp.append(" %s REGEXP '%s' " % (k,v))
        query += oper.join(tmp)

        return cls.__getData(query)

    @classmethod
    def getWeit(cls, dictPattern={'id':'.*'}, oper='OR'):
        query = "SELECT * FROM VIEW_WAITING where"
        
        tmp = []
        for (k,v) in dictPattern.items():
            tmp.append(" %s REGEXP '%s' " % (k,v))
        query += oper.join(tmp)

        return cls.__getData(query)

    @classmethod
    def getUser(cls):
        
        query = "SELECT * FROM users_list where user = '" + os.environ['USER'] + "'"
        return cls.__getData(query)

    @classmethod
    def setType(cls, name, parent):
        
        query = "INSERT INTO types_list(type, id_parent) VALUES('" + name + "'," + parent + ")"
        cls.__setData(query)

    @classmethod
    def setUser(cls):
        
        query = "INSERT INTO users_list(user) VALUES('" + os.environ['USER'] + "')"
        cls.__setData(query)

    @classmethod
    def setRow(cls, name, id_type, description, key_list, access="ALL"):
        
        query = "INSERT INTO waiting_list(name, id_type, id_access, description, key_list, name_a) \
                VALUES('%s', %s, '%s', '%s', '%s', '%s')" % (name, id_type, access, description, key_list, os.environ['USER'])
        cls.__setData(query)

    @classmethod
    def updateUser(cls):
        
        query_last_log = "UPDATE users_list SET last_log = NOW() where user = '" + os.environ['USER'] + "'"
        cls.__setData(query_last_log)
        return cls.getUser()

if __name__ == '__main__':

    print ConMySQL.getLib({'name': 'rnc', 'type':'LOM'},'OR')
    print ConMySQL.updateUser()
    ConMySQL.setRow('tam',1,'dupadupa','XFT')
    print ConMySQL.getLib({'name':'tam'})
    print ConMySQL.getKey('XFT')
