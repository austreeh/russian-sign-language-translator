import sqlite3

# A letter
args_example = ["Up", "fold", "fold", "fold", "fold", "fold", False, False, False, True, True ]


# fold = arc
# close = True

# A
A1 = ["A", "Up", "arc", "fold", "fold", "fold", "fold", False, False, False, False, False]
A2 = ["A", "Up", "arc", "fold", "fold", "fold", "fold", False, False, False, False, True]
A3 = ["A", "Up", "arc", "fold", "fold", "fold", "fold", False, False, False, True, False]
A4 = ["A", "Up", "arc", "fold", "fold", "fold", "fold", False, False, False, True, True]

# B
B1 = ["B", "Up", "arc", "direct", "arc", "fold", "fold", False, False, False, False, False]
B2 = ["B", "Up", "arc", "direct", "arc", "fold", "fold", False, False, True, False, False]
B3 = ["B", "Up", "arc", "direct", "arc", "fold", "fold", False, False, False, False, True]
B4 = ["B", "Up", "arc", "direct", "arc", "fold", "fold", False, False, True, False, True]
B5 = ["B", "Up", "arc", "direct", "arc", "fold", "fold", False, False, False, True, False]
B6 = ["B", "Up", "arc", "direct", "arc", "fold", "fold", False, False, True, True, False]
B7 = ["B", "Up", "arc", "direct", "arc", "fold", "fold", False, False, False, True, True]
B8 = ["B", "Up", "arc", "direct", "arc", "fold", "fold", False, False, True, True, True]

# V
V = ["V", "Up", "direct", "direct", "direct", "direct", "direct", False, False, False, True, True]

# G
G1 = ["G", "Down", "direct", "half", "fold", "fold", "fold", False, False, False, True, True]
G2 = ["G", "Down", "direct", "half", "fold", "fold", "fold", False, False, False, True, False]
G3 = ["G", "Down", "direct", "half", "fold", "fold", "fold", False, False, False, False, True]
G4 = ["G", "Down", "direct", "half", "fold", "fold", "fold", False, False, False, False, False]
G5 = ["G", "Down", "arc", "half", "fold", "fold", "fold", False, False, False, True, True]
G6 = ["G", "Down", "arc", "half", "fold", "fold", "fold", False, False, False, True, False]
G7 = ["G", "Down", "arc", "half", "fold", "fold", "fold", False, False, False, False, True]
G8 = ["G", "Down", "arc", "half", "fold", "fold", "fold", False, False, False, False, False]

# D
D = ["D", "Up", "arc", "direct", "direct", "fold", "fold", False, False, False, True, False]

# E
E1 = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, False, True, True]
E2 = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, True, True, True]
E3 = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, False, True, False]
E4 = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, True, True, False]
E5 = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, False, False, True]
E6 = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, True, False, True]
E7 = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, False, False, False]
E8 = ["E", "Up", "arc", "arc", "arc", "arc", "arc", True, True, True, False, False]

# Yo

# J # need fix
J1 = ["J", "Up", "arc", "half", "half", "half", "half", True, False, False, True, True]
J2 = ["J", "Up", "arc", "half", "half", "half", "half", True, True, False, True, True]
J3 = ["J", "Up", "arc", "half", "half", "half", "half", True, False, False, True, False]
J4 = ["J", "Up", "arc", "half", "half", "half", "half", True, True, False, True, False]
J5 = ["J", "Up", "arc", "half", "half", "half", "half", True, False, False, False, True]
J6 = ["J", "Up", "arc", "half", "half", "half", "half", True, True, False, False, True]
J7 = ["J", "Up", "arc", "half", "half", "half", "half", True, False, False, False, False]
J8 = ["J", "Up", "arc", "half", "half", "half", "half", True, True, False, False, False]
J9 = ["J", "Up", "direct", "half", "half", "half", "half", True, False, False, True, True]
J10 = ["J", "Up", "direct", "half", "half", "half", "half", True, True, False, True, True]
J11 = ["J", "Up", "direct", "half", "half", "half", "half", True, False, False, True, False]
J12 = ["J", "Up", "direct", "half", "half", "half", "half", True, True, False, True, False]
J13 = ["J", "Up", "direct", "half", "half", "half", "half", True, False, False, False, True]
J14 = ["J", "Up", "direct", "half", "half", "half", "half", True, True, False, False, True]
J15 = ["J", "Up", "direct", "half", "half", "half", "half", True, False, False, False, False]
J16 = ["J", "Up", "direct", "half", "half", "half", "half", True, True, False, False, False]

# Z

# I

# K # dynamic

# L # MAYBE HALF = DIRECT
L1 = ["L", "Down", "direct", "half", "half", "fold", "fold", False, False, False, False, True]
L2 = ["L", "Down", "arc", "half", "half", "fold", "fold", False, False, False, False, True]
L3 = ["L", "Down", "direct", "half", "half", "fold", "fold", False, False, False, False, False]
L4 = ["L", "Down", "arc", "half", "half", "fold", "fold", False, False, False, False, False]

# M # MAYBE HALF = DIRECT
M1 = ["M", "Down", "direct", "half", "half", "half", "fold", False, False, False, False, False]
M2 = ["M", "Down", "arc", "half", "half", "half", "fold", False, False, False, False, False]

# N
N1 = ["N", "Up", "arc", "direct", "direct", "arc", "direct", False, False, True, True, False]
N2 = ["N", "Up", "arc", "direct", "direct", "arc", "direct", False, False, True, False, False]
N3 = ["N", "Up", "arc", "direct", "direct", "arc", "direct", False, False, True, False, True]
N4 = ["N", "Up", "arc", "direct", "direct", "arc", "direct", False, False, True, True, True]
N5 = ["N", "Up", "direct", "direct", "direct", "arc", "direct", False, False, True, True, False]
N6 = ["N", "Up", "direct", "direct", "direct", "arc", "direct", False, False, True, False, False]
N7 = ["N", "Up", "direct", "direct", "direct", "arc", "direct", False, False, True, False, True]
N8 = ["N", "Up", "direct", "direct", "direct", "arc", "direct", False, False, True, True, True]

# O
O1 = ["O", "Up", "arc", "arc", "direct", "direct", "direct", True, False, False, False, False]
O2 = ["O", "Up", "arc", "arc", "direct", "direct", "direct", True, False, False, False, True]

# P
P1 = ["P", "Down", "direct", "half", "half", "fold", "fold", False, False, False, True, True]
P2 = ["P", "Down", "arc", "half", "half", "fold", "fold", False, False, False, True, True]
P3 = ["P", "Down", "direct", "half", "half", "fold", "fold", False, False, False, True, False]
P4 = ["P", "Down", "arc", "half", "half", "fold", "fold", False, False, False, True, False]

# R
R1 = ["R", "Up", "arc", "direct", "arc", "direct", "direct", False, True, False, False, False]
R2 = ["R", "Up", "arc", "direct", "arc", "direct", "direct", False, True, False, False, True]

# S
S1 = ["S", "Up", "direct", "arc", "arc", "arc", "arc", False, False, False, False, False]
S2 = ["S", "Up", "direct", "arc", "arc", "arc", "direct", False, False, False, False, False]
S3 = ["S", "Up", "direct", "arc", "arc", "arc", "arc", False, False, False, False, True]
S4 = ["S", "Up", "direct", "arc", "arc", "arc", "direct", False, False, False, False, True]
S5 = ["S", "Up", "direct", "arc", "arc", "arc", "arc", False, False, False, True, False]
S6 = ["S", "Up", "direct", "arc", "arc", "arc", "direct", False, False, False, True, False]
S7 = ["S", "Up", "direct", "arc", "arc", "arc", "arc", False, False, False, True, True]
S8 = ["S", "Up", "direct", "arc", "arc", "arc", "direct", False, False, False, True, True]

# T # SAME AS M
T1 = ["T", "Down", "direct", "half", "half", "half", "fold", False, False, False, True, True]
T2 = ["T", "Down", "arc", "half", "half", "half", "fold", False, False, False, True, True]

# U
U1 = ["U", "Up", "direct", "fold", "fold", "fold", "direct", False, False, False, True, True]
U2 = ["U", "Up", "direct", "fold", "fold", "fold", "direct", False, False, False, True, False]
U3 = ["U", "Up", "direct", "fold", "fold", "fold", "direct", False, False, False, False, True]
U4 = ["U", "Up", "direct", "fold", "fold", "fold", "direct", False, False, False, False, False]

# F # skip, like J

# H # need fix
H1 = ["H", "Up", "arc", "arc", "fold", "fold", "fold", False, True, False, False, False]
H2 = ["H", "Up", "arc", "arc", "fold", "fold", "fold", False, True, False, False, True]
H3 = ["H", "Up", "arc", "arc", "fold", "fold", "fold", False, True, False, True, False]
H4 = ["H", "Up", "arc", "arc", "fold", "fold", "fold", False, True, False, True, True]

# Ch # middle half - fold problem
Ch1 = ["Ch", "Up", "direct", "half", "half", "fold", "fold", True, True, False, False, False]
Ch2 = ["Ch", "Up", "direct", "half", "half", "fold", "fold", True, True, False, True, False]
Ch3 = ["Ch", "Up", "direct", "half", "half", "fold", "fold", True, True, False, False, True]
Ch4 = ["Ch", "Up", "direct", "half", "half", "fold", "fold", True, True, False, True, True]
Ch5 = ["Ch", "Up", "arc", "half", "half", "fold", "fold", True, True, False, False, False]
Ch6 = ["Ch", "Up", "arc", "half", "half", "fold", "fold", True, True, False, True, False]
Ch7 = ["Ch", "Up", "arc", "half", "half", "fold", "fold", True, True, False, False, True]
Ch8 = ["Ch", "Up", "arc", "half", "half", "fold", "fold", True, True, False, True, True]

# Sh
Sh1 = ["Sh", "Up", "arc", "half", "half", "half", "fold", False, False, False, True, True]
Sh2 = ["Sh", "Up", "arc", "half", "half", "direct", "fold", False, False, False, True, True]
Sh3 = ["Sh", "Up", "direct", "half", "half", "half", "fold", False, False, False, True, True]
Sh4 = ["Sh", "Up", "direct", "half", "half", "direct", "fold", False, False, False, True, True]

# Sh' # dynamic

# Soft
Sf1 = ["Soft", "Up", "direct", "direct", "fold", "fold", "fold", False, False, False, False, False]
Sf2 = ["Soft", "Up", "direct", "direct", "fold", "fold", "fold", False, False, False, True, False]
Sf3 = ["Soft", "Up", "direct", "direct", "fold", "fold", "fold", False, False, False, False, True]
Sf4 = ["Soft", "Up", "direct", "direct", "fold", "fold", "fold", False, False, False, True, True]

# bl
bl1 = ["bl", "Up", "arc", "direct", "arc", "arc", "direct", False, True, True, False, False]
bl2 = ["bl", "Up", "arc", "direct", "arc", "arc", "direct", False, True, True, True, False]
bl3 = ["bl", "Up", "arc", "direct", "arc", "arc", "direct", False, True, True, False, True] 
bl4 = ["bl", "Up", "arc", "direct", "arc", "arc", "direct", False, True, True, True, True]

# Ae
Ae1 = ["Ae", "Up", "direct", "arc", "fold", "fold", "fold", False, False, False, False, False]

# Ju
Ju1 = ["Ju", "Up", "direct", "half", "half", "half", "direct", True, True, True, True, True]
Ju2 = ["Ju", "Up", "direct", "half", "half", "half", "direct", True, True, True, True, False]
Ju3 = ["Ju", "Up", "direct", "half", "half", "half", "direct", True, True, True, False, True]
Ju4 = ["Ju", "Up", "direct", "half", "half", "half", "direct", True, True, True, False, False]

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

db = Database('signs.db')

db.insert(A1)
db.insert(A2)
db.insert(A3)
db.insert(A4)

db.insert(B1)
db.insert(B2)
db.insert(B3)
db.insert(B4)
db.insert(B5)
db.insert(B6)
db.insert(B7)
db.insert(B8)

db.insert(V)

db.insert(G1)
db.insert(G2)
db.insert(G3)
db.insert(G4)
db.insert(G5)
db.insert(G6)
db.insert(G7)
db.insert(G8)

db.insert(D)

db.insert(E1)
db.insert(E2)
db.insert(E3)
db.insert(E4)
db.insert(E5)
db.insert(E6)
db.insert(E7)
db.insert(E8)

db.insert(J1)
db.insert(J2)
db.insert(J3)
db.insert(J4)
db.insert(J5)
db.insert(J6)
db.insert(J7)
db.insert(J8)
db.insert(J9)
db.insert(J10)
db.insert(J11)
db.insert(J12)
db.insert(J13)
db.insert(J14)
db.insert(J15)
db.insert(J16)

db.insert(L1)
db.insert(L2)
db.insert(L3)
db.insert(L4)

db.insert(M1)
db.insert(M2)

db.insert(N1)
db.insert(N2)
db.insert(N3)
db.insert(N4)
db.insert(N5)
db.insert(N6)
db.insert(N7)
db.insert(N8)

db.insert(O1)
db.insert(O2)

db.insert(P1)
db.insert(P2)
db.insert(P3)
db.insert(P4)

db.insert(R1)
db.insert(R2)

db.insert(S1)
db.insert(S2)
db.insert(S3)
db.insert(S4)
db.insert(S5)
db.insert(S6)
db.insert(S7)
db.insert(S8)

db.insert(T1)
db.insert(T2)

db.insert(U1)
db.insert(U2)
db.insert(U3)
db.insert(U4)


db.insert(H1)
db.insert(H2)
db.insert(H3)
db.insert(H4)

db.insert(Ch1)
db.insert(Ch2)
db.insert(Ch3)
db.insert(Ch4)
db.insert(Ch5)
db.insert(Ch6)
db.insert(Ch7)
db.insert(Ch8)

db.insert(Sh1)
db.insert(Sh2)
db.insert(Sh3)
db.insert(Sh4)

db.insert(Sf1)
db.insert(Sf2)
db.insert(Sf3)
db.insert(Sf4)

db.insert(bl1)
db.insert(bl2)
db.insert(bl3)
db.insert(bl4)

db.insert(Ae1)

db.insert(Ju1)
db.insert(Ju2)
db.insert(Ju3)
db.insert(Ju4)

# db.init_types(type_example)
# db.insert(sign_example_A)
# print(db.fetch_types())
# db.insert("Be", "fold", "direct", "arc", "fold", "fold")
# db.insert("Ve", "direct", "direct", "direct", "direct", "direct")
