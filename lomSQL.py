import sqlite3

class lomsql:
    
    def __init__(self, name="test.db"):
        self.name = name
        print "Connected to ",self.name

    def add(self, operation):
        conn = sqlite3.connect(self.name)
        conn.execute(operation)
        conn.commit()
        conn.close()

    def get(self, operation):
        expr = operation.split()[0]
        if (expr not in "CREATE") or (expr not in "INSERT") or (expr not in "DROP") or (expr not in "UPDATE"):
            conn = sqlite3.connect(self.name)
            table = conn.execute(operation).fetchall()
            conn.close()
            return table
    
