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


# db = Database('signs.db')

# for element in gestures_list:
#     db.insert(element)

# db.insert(A1)
# db.insert(A2)
# db.insert(A3)
# db.insert(A4)

# db.insert(B1)
# db.insert(B2)
# db.insert(B3)
# db.insert(B4)
# db.insert(B5)
# db.insert(B6)
# db.insert(B7)
# db.insert(B8)

# db.insert(V)

# db.insert(G1)
# db.insert(G2)
# db.insert(G3)
# db.insert(G4)

# db.insert(D)

# db.insert(E1)
# db.insert(E2)
# db.insert(E3)
# db.insert(E4)
# db.insert(E5)
# db.insert(E6)
# db.insert(E7)
# db.insert(E8)

# db.insert(J1)
# db.insert(J2)
# db.insert(J3)
# db.insert(J4)
# db.insert(J5)
# db.insert(J6)
# db.insert(J7)
# db.insert(J8)


# db.insert(L1)
# db.insert(L2)
# db.insert(L3)
# db.insert(L4)

# db.insert(M1)
# db.insert(M2)

# db.insert(N1)
# db.insert(N2)
# db.insert(N3)
# db.insert(N4)

# db.insert(O1)
# db.insert(O2)

# db.insert(P1)
# db.insert(P2)
# db.insert(P3)
# db.insert(P4)

# db.insert(R1)
# db.insert(R2)

# db.insert(S1)
# db.insert(S2)
# db.insert(S3)
# db.insert(S4)
# db.insert(S5)
# db.insert(S6)
# db.insert(S7)
# db.insert(S8)

# db.insert(T1)
# db.insert(T2)

# db.insert(U1)
# db.insert(U2)
# db.insert(U3)
# db.insert(U4)


# db.insert(H1)
# db.insert(H2)
# db.insert(H3)
# db.insert(H4)

# db.insert(Ch1)
# db.insert(Ch2)
# db.insert(Ch3)
# db.insert(Ch4)

# db.insert(Sh1)
# db.insert(Sh2)
# db.insert(Sh3)
# db.insert(Sh4)

# db.insert(Sf1)
# db.insert(Sf2)
# db.insert(Sf3)
# db.insert(Sf4)

# db.insert(bl1)
# db.insert(bl2)
# db.insert(bl3)
# db.insert(bl4)

# db.insert(Ae1)

# db.insert(Ju1)
# db.insert(Ju2)
# db.insert(Ju3)
# db.insert(Ju4)

# db.init_types(type_example)
# db.insert(sign_example_A)
# print(db.fetch_types())
# db.insert("Be", "fold", "direct", "arc", "fold", "fold")
# db.insert("Ve", "direct", "direct", "direct", "direct", "direct")
