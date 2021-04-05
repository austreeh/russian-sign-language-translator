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

# A
for bit in TOUCHES:
    for bmt in TOUCHES:
        for brt in TOUCHES:
            for ima in ANGLES[0:2]:
                for mra in ANGLES[0:2]:
                    gestures_list.append(["A", "Up", "arc", "fold", "fold", "fold", "fold", bit, bmt, brt, ima, mra])

# B
for bfp in BIG_POSES:
    for brt in TOUCHES:
        for ima in ANGLES[0:2]:
            for mra in ANGLES[0:2]:
                gestures_list.append(["B", "Up", bfp, "direct", "arc", "fold", "fold", False, False, brt, ima, mra])

# V
gestures_list.append(["V", "Up", "direct", "direct", "direct", "direct", "direct", False, False, False, "close", "close"])

# G
for ifp in FINGER_POSES[0:2]:
    for ima in ANGLES[0:2]:
        for mra in ANGLES[0:2]:
            gestures_list.append(["G", "Down", "direct", ifp, "fold", "fold", "fold", False, False, False, ima, mra])

# D
for bfp in BIG_POSES:
    for mra in ANGLES[0:2]:
        gestures_list.append(["D", "Up", bfp, "direct", "direct", "fold", "fold", False, False, True, "close", mra])

# Ye
for brt in TOUCHES:
    for ima in ANGLES[0:2]:
        for mra in ANGLES[0:2]:
            gestures_list.append(["Ye", "Up", "direct", "arc", "arc", "arc", "arc", True, True, brt, ima, mra])

# Yo # same as Ye but with trajectory

# Zh
for bmt in TOUCHES:
    for brt in TOUCHES:
        for ima in ANGLES:
            for mra in ANGLES:
                gestures_list.append(["Zh", "Up", "direct", "half", "half", "half", "half", True, bmt, brt, ima, mra])

# Z
for bfp in BIG_POSES:
    for lfp in FINGER_POSES[2:4]:
        for brt in TOUCHES:
            for ima in ANGLES:
                for mra in ANGLES:
                    gestures_list.append(["Z", "Up", bfp, "direct", "fold", "fold", lfp, False, True, brt, ima, mra])

# I # PROBLEM

# Yi # PROBLEM #2

# K # dynamic
for bfp in BIG_POSES:
    for mra in ANGLES:
        gestures_list.append(["K", "Up", bfp, "direct", "direct", "fold", "fold", False, False, True, "open", mra])

# L
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[0:2]:
        for mfp in FINGER_POSES[0:2]:
            for mra in ANGLES:
                gestures_list.append(["L", "Down", bfp, ifp, mfp, "fold", "fold", False, False, True, "open", mra])

# M
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[0:2]:
        for mfp in FINGER_POSES[0:2]:
            for rfp in FINGER_POSES[0:2]:
                gestures_list.append(["M", "Down", bfp, ifp, mfp, rfp, "fold", False, False, False, "open", "open"])

# N
for rfp in FINGER_POSES[2:4]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["N", "Up", "direct", "direct", "direct", rfp, "direct", False, False, True, ima, mra])

# O
for ifp in FINGER_POSES[2:4]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["O", "Up", "direct", ifp, "direct", "direct", "direct", True, False, False, ima, mra])

# P
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[0:2]:
        for mfp in FINGER_POSES[0:2]:
            for mra in ANGLES:
                gestures_list.append(["P", "Down", bfp, ifp, mfp, "fold", "fold", False, False, True, "close", mra])

# R
for mfp in FINGER_POSES[2:4]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["R", "Up", "direct", "direct", mfp, "direct", "direct", False, True, False, ima, mra])

# S
for bfp in BIG_POSES:
    for lfp in FINGER_POSES[0:3:2]:
        for ima in ANGLES:
            for mra in ANGLES:
                gestures_list.append(["S", "Up", bfp, "arc", "arc", "arc", lfp, False, False, False, ima, mra])

# T
for bfp in BIG_POSES:
    for ifp in FINGER_POSES[0:2]:
        for mfp in FINGER_POSES[0:2]:
            for rfp in FINGER_POSES[0:2]:
                gestures_list.append(["T", "Down", bfp, ifp, mfp, rfp, "fold", False, False, False, "close", "close"])

# U
for ima in ANGLES:
    for mra in ANGLES:
        gestures_list.append(["U", "Up", "direct", "fold", "fold", "fold", "direct", False, False, False, ima, mra])

# F
for ima in ANGLES:
    for mra in ANGLES:
        gestures_list.append(["F", "Up", "direct", "half", "half", "half", "half", False, False, False, ima, mra])

# H
for bfp in BIG_POSES:
    for brt in TOUCHES:
        for ima in ANGLES:
            for mra in ANGLES:
                gestures_list.append(["H", "Up", bfp, "arc", "fold", "fold", "fold", False, True, brt, ima, mra])

# Ts # Use B, dynamic

# Ch # need fix

# Sh
for mfp in FINGER_POSES[0:2]:
    for rfp in FINGER_POSES[0:2]:
        gestures_list.append(["Sh", "Up", "direct", "direct", mfp, rfp, "fold", False, False, False, "close", "close"])

# Tsh # use SH, dynamic

# Soft
for lfp in FINGER_POSES[2:4]:
    for ima in ANGLES:
        for mra in ANGLES:
            gestures_list.append(["Soft", "Up", "direct", "direct", "fold", "fold", lfp, False, False, False, ima, mra])

# bl
for bfp in BIG_POSES:
    for mfp in FINGER_POSES[2:4]:
        for rfp in FINGER_POSES[2:4]:
            for brt in TOUCHES:
                for ima in ANGLES:
                    for mra in ANGLES:
                        gestures_list.append(["bl", "Up", bfp, "direct", mfp, rfp, "direct", False, True, brt, ima, mra])

# Hard # use Soft, dynamic

# E
for bfp in BIG_POSES:
        for ima in ANGLES:
            for mra in ANGLES:
                gestures_list.append(["E", "Up", bfp, "arc", "fold", "fold", "fold", False, False, False, ima, mra])

# Ju

# Ya
for bfp in BIG_POSES:
    for mra in ANGLES[0:2]:
        gestures_list.append(["Ya", "Up", bfp, "direct", "direct", "fold", "fold", False, False, True, "cross", mra])
