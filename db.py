import sqlite3

# A letter
args_example = ["Up", "fold", "fold", "fold", "fold", "fold", False, False, False, True, True ]


# fold = arc
# close = True

# P
P = []
# R
R = ["R", "Up", "arc", "direct", "arc", "direct", "direct", False, True, False, False, False]
# I
I = ["I", "Up", "direct", "half", "half", "direct", "direct", True, True, False, True, False]
# V
V = ["V", "Up", "direct", "direct", "direct", "direct", "direct", False, False, False, True, True]
# E
E = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, False, True, True]
# T
T = []

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS gesture "
            + "(name text, direction text, big_finger text, index_finger text, "
            + "middle_finger text, ring_finger text, little_finger text, big_index_touch boolean, " 
            + "big_middle_touch boolean, big_ring_touch boolean, index_middle_closed boolean, " 
            + "middle_ring_closed boolean)")
        self.conn.commit()
    
    def fetch(self):
        self.cur.execute("SELECT * FROM gesture")
        rows=self.cur.fetchall()
        return rows

    def insert(self, args):
        # create dynamic string request
        request_string = list("INSERT INTO gesture VALUES ( ")
        for element in args:
            request_string+="?,"
        request_string[len(request_string)-1] = ')' # change last ',' to ')'

        self.cur.execute("".join(request_string),tuple(args)) # make sql request
        self.conn.commit()  # commit

    def fetch_types(self):
        self.cur.execute("SELECT * FROM types")
        row=self.cur.fetchone()
        return row

    def update(self, id, args):
        columns = self.columns()
        request_string = list("UPDATE gesture SET ")
        for i in range(1,len(args)+1):
            request_string+=columns[i]+" = ?,"
        request_string[len(request_string)-1] = ' '
        request_string+= "WHERE id ="+str(id)
        print("".join(request_string))
        print(tuple(args))
        self.cur.execute("".join(request_string),tuple(args)) # make sql request
        self.conn.commit()

    def get_element(self, args_example):
        self.cur.execute("SELECT name FROM gesture WHERE direction=? AND big_finger=? AND "+
        "index_finger=? AND middle_finger=? AND ring_finger=? AND little_finger=? AND big_index_touch=? AND "+
        "big_middle_touch=? AND big_ring_touch=? AND index_middle_closed=? AND middle_ring_closed=?", 
        tuple(args_example))
        return self.cur.fetchone()

    def __del__(self):
        self.conn.close()

# db = Database('signs.db')
# db.insert(R)
# db.insert(I)
# db.insert(V)
# db.insert(E)


# db.init_types(type_example)
# db.insert(sign_example_A)
# print(db.fetch_types())
# db.insert("Be", "fold", "direct", "arc", "fold", "fold")
# db.insert("Ve", "direct", "direct", "direct", "direct", "direct")
