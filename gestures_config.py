gestures_list = []

TOUCHES = [True, False]
ANGLES = ["open", "close", "cross"]
BIG_POSES = ["direct", "arc"]
FINGER_POSES = ["direct", "half", "arc", "fold"]

# bit - big_index_touch
# bmt - big_middle_touch
# brt - big_ring_touch
# ima - index_middle_angle
# mra - middle_ring_angle

# bfp - big_finger_pose
# ifp - index_finger_pose
# mfp - middle_fibger_pose
# rfp - ring_finger_pose
# lfp - little_finger_pose

# allow direct little finger test

# tool gesture # use it for ",", ".", " ", "?"
gestures_list.append(["Tool", "Up", "direct", "direct", "direct", "direct", "direct", False, False, False, "open", "open"])
gestures_list.append(["Tool", "Up", "direct", "direct", "direct", "direct", "direct", False, False, False, "close", "open"])

# A
for lfp in FINGER_POSES[1:4]:
    for bit in TOUCHES:
        for bmt in TOUCHES:
            for brt in TOUCHES:
                for ima in ANGLES:
                    for mra in ANGLES:
                        gestures_list.append(["А", "Up", "arc", "fold", "fold", "fold", lfp, bit, bmt, brt, ima, mra])
                        # gestures_list.append(["А", "Up", "direct", "fold", "fold", "fold", lfp, bit, bmt, brt, ima, mra])


# B
for bfp in BIG_POSES:
    for bmt in TOUCHES:
        for brt in TOUCHES:
            for ima in ANGLES:
                for mra in ANGLES:
                    gestures_list.append(["Б", "Up", bfp, "direct", "arc", "fold", "fold", False, bmt, brt, ima, mra])
# V
gestures_list.append(["В", "Up", "direct", "direct", "direct", "direct", "direct", False, False, False, "close", "close"])

# G
for ifp in FINGER_POSES[0:2]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["Г", "Down", "direct", ifp, "fold", "fold", "fold", False, False, False, ima, mra])

# D
for bfp in BIG_POSES:
    for brt in TOUCHES:
        for mra in ANGLES[0:2]:
            gestures_list.append(["Д", "Up", bfp, "direct", "direct", "fold", "fold", False, False, brt, "close", mra])
# fix add
gestures_list.append(["Д", 'Up', 'direct', 'direct', 'direct', 'fold', 'fold', False, False, False, 'open', 'open'])


# Ye
for bfp in BIG_POSES:
    for bmt in TOUCHES:
        for brt in TOUCHES:
            for ima in ANGLES[0:2]:
                for mra in ANGLES[0:2]:
                    gestures_list.append(["Е", "Up", bfp, "arc", "arc", "arc", "arc", True, bmt, brt, ima, mra])
gestures_list.append(['Е','Up', 'arc', 'arc', 'direct', 'direct', 'arc', True, True, True, 'close', 'close'])
gestures_list.append(['Е','Up', 'direct', 'arc', 'direct', 'arc', 'arc', True, True, True, 'close', 'close'])
gestures_list.append(['Е','Up', 'direct', 'arc', 'direct', 'direct', 'direct', True, True, True, 'close', 'close'])
gestures_list.append(['Е','Up', 'direct', 'fold', 'fold', 'fold', 'fold', False, True, False, 'open', 'open'])
gestures_list.append(['Е','Up', 'direct', 'fold', 'fold', 'fold', 'fold', False, True, True, 'open', 'open'])
gestures_list.append(['Е','Up', 'direct', 'arc', 'fold', 'fold', 'fold', True, True, True, 'open', 'open'])
gestures_list.append(['Е','Up', 'direct', 'arc', 'arc', 'fold', 'arc', True, True, True, 'close', 'close'])
gestures_list.append(['Е','Up', 'direct', 'fold', 'fold', 'fold', 'fold', True, True, True, 'open', 'open'])
gestures_list.append(['Е','Up', 'direct', 'arc', 'direct', 'direct', 'arc', True, True, True, 'close', 'close'])
gestures_list.append(['Е','Up', 'direct', 'fold', 'fold', 'fold', 'arc', True, True, True, 'open', 'open'])
gestures_list.append(['Е','Up', 'direct', 'fold', 'fold', 'fold', 'arc', True, True, True, 'close', 'close'])
gestures_list.append(['Е','Up', 'direct', 'arc', 'fold', 'fold', 'arc', True, True, True, 'open', 'open'])


# Zh
for bmt in TOUCHES:
    for brt in TOUCHES:
        for ima in ANGLES:
            for mra in ANGLES:
                gestures_list.append(["Ж", "Up", "direct", "half", "half", "half", "half", True, bmt, brt, ima, mra])

# Z
for bfp in BIG_POSES:
    for lfp in FINGER_POSES[2:4]:
        for brt in TOUCHES:
            for ima in ANGLES:
                for mra in ANGLES:
                    gestures_list.append(["З", "Up", bfp, "direct", "fold", "fold", lfp, False, True, brt, ima, mra])

# I # PROBLEM
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[2:4]:
        for mfp in FINGER_POSES[2:4]:
            for rfp in FINGER_POSES[0:2]:
                for lfp in FINGER_POSES[0:2]:
                    for ima in ANGLES:
                        for mra in ANGLES:
                            gestures_list.append(["И", "Up", bfp, ifp, mfp, rfp, lfp, True, False, False, ima, mra])
                            gestures_list.append(["И", "Up", bfp, ifp, mfp, rfp, lfp, True, True, False, ima, mra])
                            gestures_list.append(["И", "Up", bfp, ifp, mfp, rfp, lfp, False, True, False, ima, mra])
gestures_list.append(["И", "Up", "direct", "arc", "direct", "direct", "direct", True, True, False, "open", "open"])
gestures_list.append(["И", "Up", "direct", "arc", "direct", "direct", "direct", True, True, False, "close", "open"])
gestures_list.append(["И", "Up", "direct", "arc", "direct", "direct", "direct", True, True, False, "open", "close"])
gestures_list.append(["И", "Up", "direct", "arc", "direct", "direct", "direct", True, True, False, "open", "cross"])
gestures_list.append(["И", "Up", "direct", "arc", "direct", "direct", "direct", True, True, False, "close", "cross"])


# Yi # PROBLEM #2

# K # dynamic
for bfp in BIG_POSES:
    for mra in ANGLES:
        gestures_list.append(["К", "Up", bfp, "direct", "direct", "fold", "fold", False, False, True, "open", mra])

# L
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[0:2]:
        for mfp in FINGER_POSES[0:2]:
            for mra in ANGLES:
                gestures_list.append(["Л", "Down", bfp, ifp, mfp, "fold", "fold", False, False, True, "open", mra])

# M
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[0:2]:
        for mfp in FINGER_POSES[0:2]:
            for rfp in FINGER_POSES[0:2]:
                gestures_list.append(["М", "Down", bfp, ifp, mfp, rfp, "fold", False, False, False, "open", "open"])

# N
for rfp in FINGER_POSES[2:4]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["Н", "Up", "direct", "direct", "direct", rfp, "direct", False, False, True, ima, mra])

# O
for ifp in FINGER_POSES[2:4]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["О", "Up", "direct", ifp, "direct", "direct", "direct", True, False, False, ima, mra])

# P
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[0:2]:
        for mfp in FINGER_POSES[0:2]:
            for mra in ANGLES:
                gestures_list.append(["П", "Down", bfp, ifp, mfp, "fold", "fold", False, False, True, "close", mra])

# R
for mfp in FINGER_POSES[2:4]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["Р", "Up", "direct", "direct", mfp, "direct", "direct", False, True, False, ima, mra])

# S
for bfp in BIG_POSES:
    for mfp in FINGER_POSES[0:3:2]:
        for lfp in FINGER_POSES[0:3:2]:
            for ima in ANGLES:
                for mra in ANGLES:
                    gestures_list.append(["С", "Up", bfp, "arc", mfp, "arc", lfp, False, False, False, ima, mra])

# T
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[0:2]:
        for mfp in FINGER_POSES[0:2]:
            for rfp in FINGER_POSES[0:2]:
                gestures_list.append(["Т", "Down", bfp, ifp, mfp, rfp, "fold", False, False, False, "close", "close"])

# U
for ifp in FINGER_POSES[1:4]:
    for mfp in FINGER_POSES[1:4]:
        for rfp in FINGER_POSES[1:4]:
            for ima in ANGLES:
                for mra in ANGLES:
                    gestures_list.append(["У", "Up", "direct", ifp, mfp, rfp, "direct", False, False, False, ima, mra])

# F
for ifp in FINGER_POSES[1:4:2]:
    for rfp in FINGER_POSES[1:4:2]:
        for lfp in FINGER_POSES[1:4:2]:
            for ima in ANGLES:
                for mra in ANGLES:
                    gestures_list.append(["Ф", "Up", "direct", ifp, "half", rfp, lfp, False, False, False, ima, mra])

# H
for bfp in BIG_POSES:
    for brt in TOUCHES:
        for ima in ANGLES:
            for mra in ANGLES:
                gestures_list.append(["Х", "Up", bfp, "arc", "fold", "fold", "fold", False, True, brt, ima, mra])

# Ts # Use B, dynamic

# Ch
for bfp in BIG_POSES:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["Ч", "Up", bfp, "half", "half", "fold", "fold", True, True, False, ima, mra])
            gestures_list.append(["Ч", "Up", bfp, "half", "fold", "fold", "fold", True, True, False, ima, mra])
            gestures_list.append(["Ч", "Up", bfp, "fold", "half", "fold", "fold", True, True, False, ima, mra])

# Sh
for ifp in FINGER_POSES[0:2]:
    for mfp in FINGER_POSES[0:2]:
        for rfp in FINGER_POSES[0:2]:
            gestures_list.append(["Ш", "Up", "direct", ifp, mfp, rfp, "fold", False, False, False, "close", "close"])

# Tsh # use SH, dynamic

# Soft
for lfp in FINGER_POSES[2:4]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["Ь", "Up", "direct", "direct", "fold", "fold", lfp, False, False, False, ima, mra])

# bl
for bfp in BIG_POSES:
    for mfp in FINGER_POSES[2:4]:
        for rfp in FINGER_POSES[2:4]:
            for brt in TOUCHES:
                for ima in ANGLES:
                    for mra in ANGLES:
                        gestures_list.append(["Ы", "Up", bfp, "direct", mfp, rfp, "direct", False, True, brt, ima, mra])
                        gestures_list.append(["Ы", "Up", bfp, "direct", mfp, rfp, "direct", True, False, brt, ima, mra]) # ?

# Hard # use Soft, dynamic

# E
for bfp in BIG_POSES:
        for ima in ANGLES:
            for mra in ANGLES:
                gestures_list.append(["Э", "Up", bfp, "arc", "fold", "fold", "fold", False, False, False, ima, mra])

# Ju
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[1:4:1]:
        for mfp in FINGER_POSES[1:4:1]:
            for rfp in FINGER_POSES[1:4:1]:
                for bmt in TOUCHES:
                    for brt in TOUCHES:
                        for ima in ANGLES:
                            for mra in ANGLES:
                                gestures_list.append(["Ю", "Up", bfp, ifp, mfp, rfp, "direct", True, bmt, brt, ima, mra])


# Ya
for bfp in BIG_POSES:
    for mra in ANGLES[0:2]:
        gestures_list.append(["Я", "Up", bfp, "direct", "direct", "fold", "fold", False, False, True, "cross", mra])
