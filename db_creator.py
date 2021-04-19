import sqlite3
from gestures_config import *

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS gesture "
            + "(name text, direction text, big_finger text, index_finger text, "
            + "middle_finger text, ring_finger text, little_finger text, big_index_touch boolean, " 
            + "big_middle_touch boolean, big_ring_touch boolean, index_middle_closed text, " 
            + "middle_ring_closed text)")
        self.conn.commit()

    def insert(self, args):
        # create dynamic string request
        request_string = list("INSERT INTO gesture VALUES ( ")
        for element in args:
            request_string+="?,"
        request_string[len(request_string)-1] = ')' # change last ',' to ')'

        self.cur.execute("".join(request_string),tuple(args)) # make sql request
        self.conn.commit()  # commit

    def get_element(self, args_example):
        self.cur.execute("SELECT name FROM gesture WHERE direction=? AND big_finger=? AND "+
        "index_finger=? AND middle_finger=? AND ring_finger=? AND little_finger=? AND big_index_touch=? AND "+
        "big_middle_touch=? AND big_ring_touch=? AND index_middle_closed=? AND middle_ring_closed=?", 
        tuple(args_example))
        return self.cur.fetchone()

    def __del__(self):
        self.conn.close()

# SQLITE3 in memory google

# db = Database('signs.db')

# for element in gestures_list:
    # db.insert(element)
