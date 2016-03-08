import MySQLdb

class MySQL(object):

    __init__(self):
        self.db = MySQLdb.connect(host='172.19.20.19',user='lom',passwd='lom',db='LOM',port=3306)

