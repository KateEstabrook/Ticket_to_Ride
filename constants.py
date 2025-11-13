"""
Constants for project
"""

import platform
import arcade

PLAYER_SCALING = 0.05
BOARD_SCALE = 0.8

SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_display_size()
WINDOW_TITLE = "Ticket to Ride"
if platform.system() == "Darwin":  # macOS
    WINDOW_WIDTH = SCREEN_WIDTH
    WINDOW_HEIGHT = SCREEN_HEIGHT - 115

else:
    WINDOW_WIDTH = SCREEN_WIDTH - 400
    WINDOW_HEIGHT = SCREEN_HEIGHT - 180

BOARD_WIDTH = 1150
BOARD_HEIGHT = 720
BOARD_LEFT = (WINDOW_WIDTH - BOARD_WIDTH) // 2
BOARD_BOTTOM = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2

CITY_SCALE = 0.0111
CITY_SCALE_YELLOW = 0.016
TRAIN_SCALE = 0.06

COLORS = ["pink", "blue", "orange", "white", "green", "yellow", "black", "red"]

PLAYER_COLORS = ["red", "yellow", "green", "blue"]
STARTING_CARDS = 103

CITIES = {
    "Calgary": {"CITY_IMG_X": 587, "CITY_IMG_Y": 212},
    "Vancouver": {"CITY_IMG_X": 266, "CITY_IMG_Y": 255},
    "Seattle": {"CITY_IMG_X": 261, "CITY_IMG_Y": 390},
    "Portland": {"CITY_IMG_X": 207, "CITY_IMG_Y": 512},
    "San Francisco": {"CITY_IMG_X": 173, "CITY_IMG_Y": 995},
    "Los Angeles": {"CITY_IMG_X": 362, "CITY_IMG_Y": 1250},
    "Helena": {"CITY_IMG_X": 832, "CITY_IMG_Y": 535},
    "Salt Lake City": {"CITY_IMG_X": 655, "CITY_IMG_Y": 838},
    "Las Vegas": {"CITY_IMG_X": 520, "CITY_IMG_Y": 1108},
    "Phoenix": {"CITY_IMG_X": 656, "CITY_IMG_Y": 1268},
    "Winnipeg": {"CITY_IMG_X": 1134, "CITY_IMG_Y": 238},
    "Denver": {"CITY_IMG_X": 974, "CITY_IMG_Y": 915},
    "Santa Fe": {"CITY_IMG_X": 956, "CITY_IMG_Y": 1134},
    "El Paso": {"CITY_IMG_X": 944, "CITY_IMG_Y": 1355},
    "Duluth": {"CITY_IMG_X": 1410, "CITY_IMG_Y": 520},
    "Omaha": {"CITY_IMG_X": 1334, "CITY_IMG_Y": 747},
    "Kansas City": {"CITY_IMG_X": 1385, "CITY_IMG_Y": 870},
    "Oklahoma City": {"CITY_IMG_X": 1338, "CITY_IMG_Y": 1082},
    "Dallas": {"CITY_IMG_X": 1385, "CITY_IMG_Y": 1297},
    "Houston": {"CITY_IMG_X": 1486, "CITY_IMG_Y": 1395},
    "Sault St. Marie": {"CITY_IMG_X": 1720, "CITY_IMG_Y": 364},
    "Chicago": {"CITY_IMG_X": 1708, "CITY_IMG_Y": 674},
    "Saint Louis": {"CITY_IMG_X": 1600, "CITY_IMG_Y": 874},
    "Little Rock": {"CITY_IMG_X": 1558, "CITY_IMG_Y": 1092},
    "New Orleans": {"CITY_IMG_X": 1715, "CITY_IMG_Y": 1365},
    "Toronto": {"CITY_IMG_X": 1986, "CITY_IMG_Y": 411},
    "Pittsburgh": {"CITY_IMG_X": 2029, "CITY_IMG_Y": 635},
    "Nashville": {"CITY_IMG_X": 1828, "CITY_IMG_Y": 970},
    "Atlanta": {"CITY_IMG_X": 1950, "CITY_IMG_Y": 1052},
    "Charleston": {"CITY_IMG_X": 2180, "CITY_IMG_Y": 1071},
    "Miami": {"CITY_IMG_X": 2259, "CITY_IMG_Y": 1459},
    "Raleigh": {"CITY_IMG_X": 2112, "CITY_IMG_Y": 912},
    "Washington": {"CITY_IMG_X": 2255, "CITY_IMG_Y": 747},
    "New York": {"CITY_IMG_X": 2233, "CITY_IMG_Y": 526},
    "Boston": {"CITY_IMG_X": 2363, "CITY_IMG_Y": 346},
    "Montreal": {"CITY_IMG_X": 2189, "CITY_IMG_Y": 200}
}

ROUTES = {
    "Vancouver": {"Seattle": 1, "Calgary": 3},
    "Seattle": {"Portland": 1, "Calgary": 4, "Vancouver": 1, "Helena": 6},
    "Portland": {"San Francisco": 5, "Seattle": 1, "Salt Lake City": 6},
    "San Francisco": {"Portland": 5, "Salt Lake City": 5, "Los Angeles": 3},
    "Los Angeles": {"San Francisco": 3, "Las Vegas": 2,
                    "Phoenix": 3, "El Paso": 6},
    "Calgary": {"Vancouver": 3, "Seattle": 4, "Helena": 4, "Winnipeg": 6},
    "Helena": {"Calgary": 4, "Seattle": 6, "Salt Lake City": 3,
               "Winnipeg": 4, "Duluth": 6, "Omaha": 5, "Denver": 4},
    "Salt Lake City": {"Portland": 6, "San Francisco": 5, "Las Vegas": 3, "Denver": 3, "Helena": 3},
    "Las Vegas": {"Salt Lake City": 3, "Los Angeles": 2},
    "Phoenix": {"Los Angeles": 3, "Denver": 5, "Santa Fe": 3, "El Paso": 3},
    "Winnipeg": {"Calgary": 6, "Helena": 4, "Duluth": 4, "Sault St. Marie": 6},
    "Denver": {"Helena": 4, "Salt Lake City": 3, "Phoenix": 5, "Omaha": 4,
               "Oklahoma City": 4, "Santa Fe": 2, "Kansas City": 4},
    "Santa Fe": {"Denver": 2, "Phoenix": 3, "El Paso": 2, "Oklahoma City": 3},
    "El Paso": {"Santa Fe": 2, "Phoenix": 3, "Los Angeles": 6, "Oklahoma City": 5,
                "Dallas": 4, "Houston": 6},
    "Duluth": {"Winnipeg": 4, "Helena": 6, "Omaha": 2, "Chicago": 3, "Toronto": 6,
               "Sault St. Marie": 3},
    "Omaha": {"Duluth": 2, "Helena": 5, "Chicago": 4, "Kansas City": 1, "Denver": 4},
    "Kansas City": {"Omaha": 1, "Denver": 4, "Saint Louis": 2, "Oklahoma City": 2},
    "Oklahoma City": {"Kansas City": 2, "Denver": 4, "El Paso": 5, "Dallas": 2,
                      "Little Rock": 2, "Santa Fe": 3},
    "Dallas": {"El Paso": 4, "Houston": 1, "Oklahoma City": 2, "Little Rock": 2},
    "Houston": {"Dallas": 1, "El Paso": 6, "New Orleans": 2},
    "Sault St. Marie": {"Winnipeg": 6, "Duluth": 3, "Montreal": 5, "Toronto": 2},
    "Chicago": {"Toronto": 4, "Duluth": 3, "Omaha": 4, "Saint Louis": 2, "Pittsburgh": 3},
    "Saint Louis": {"Chicago": 2, "Pittsburgh": 5, "Nashville": 2, "Little Rock": 2,
                    "Kansas City": 2},
    "Little Rock": {"Saint Louis": 2, "Nashville": 3, "New Orleans": 3, "Dallas": 2,
                    "Oklahoma City": 2},
    "New Orleans": {"Little Rock": 3, "Houston": 2, "Atlanta": 4, "Miami": 6},
    "Toronto": {"Sault St. Marie": 2, "Montreal": 3, "Duluth": 6, "Chicago": 4, "Pittsburgh": 2},
    "Pittsburgh": {"Toronto": 2, "Chicago": 3, "New York": 2, "Saint Louis": 5, "Nashville": 4,
                   "Washington": 2, "Raleigh": 2},
    "Nashville": {"Saint Louis": 2, "Pittsburgh": 4, "Little Rock": 3, "Atlanta": 1, "Raleigh": 3},
    "Atlanta": {"Nashville": 1, "Raleigh": 2, "Charleston": 2, "Miami": 5, "New Orleans": 4},
    "Charleston": {"Raleigh": 2, "Atlanta": 2, "Miami": 4},
    "Miami": {"Charleston": 4, "Atlanta": 5, "New Orleans": 6},
    "Raleigh": {"Charleston": 2, "Atlanta": 2, "Nashville": 3, "Washington": 2, "Pittsburgh": 2},
    "Washington": {"Raleigh": 2, "Pittsburgh": 2, "New York": 2},
    "New York": {"Washington": 2, "Pittsburgh": 2, "Montreal": 3, "Boston": 2},
    "Boston": {"New York": 2, "Montreal": 2},
    "Montreal": {"Boston": 2, "New York": 3, "Toronto": 3, "Sault St. Marie": 5}
}

# For double routes, use list of lists
TRAINS = {
    ("Montreal", "Boston"): [
        {"positions": [(2252, 230, 220), (2320, 288, 220)], "color": "colorless"},
        {"positions": [(2232, 256, 220), (2301, 313, 220)], "color": "colorless"}
    ],
    ("Boston", "New York"): [
        {"positions": [(2320, 394, 123), (2273, 470, 123)], "color": "yellow"},
        {"positions": [(2346, 414, 123), (2298, 488, 123)], "color": "red"}
    ],
    ("Montreal", "New York"): [
        {"positions": [(2182, 280, 80), (2196, 367, 80), (2210, 456, 80)], "color": "blue"}
    ],
    ("New York", "Washington"): [
        {"positions": [(2262, 595, 85), (2270, 682, 85)], "color": "black"},
        {"positions": [(2234, 593, 85), (2240, 683, 85)], "color": "orange"}
    ],
    ("Washington", "Raleigh"): [
        {"positions": [(2226, 811, 130), (2170, 877, 130)], "color": "colorless"},
        {"positions": [(2200, 792, 130), (2146, 856, 130)], "color": "colorless"}
    ],
    ("Raleigh", "Charleston"): [
        {"positions": [(2163, 954, 35), (2205, 1014, 116)], "color": "colorless"}
    ],
    ("Charleston", "Miami"): [
        {"positions": [(2183, 1137, 85), (2192, 1223, 80),
                       (2211, 1309, 70), (2247, 1390, 60)], "color": "pink"}
    ],
    ("Miami", "Atlanta"): [
        {"positions": [(2211, 1402, 48), (2152, 1335, 48), (2100, 1267, 48),
                       (2042, 1198, 48), (1990, 1130, 48)], "color": "blue"}
    ],
    ("Miami", "New Orleans"): [
        {"positions": [(2193, 1438, 45), (2130, 1377, 38), (2060, 1327, 30),
                       (1973, 1306, 0), (1887, 1317, -11), (1805, 1350, -28)], "color": "red"}
    ],
    ("Atlanta", "Charleston"): [
        {"positions": [(2028, 1080, 0), (2114, 1084, 0)], "color": "colorless"}
    ],
    ("Seattle", "Calgary"): [
        {"positions": [(335, 385, 0), (424, 380, 172), (503, 347, 143),
                       (560, 278, 118)], "color": "colorless"}
    ],
    ("Calgary", "Vancouver"): [
        {"positions": [(341, 238, 174), (429, 230, 174), (517, 219, 174)], "color": "colorless"}
    ],
    ("Calgary", "Winnipeg"): [
        {"positions": [(652, 191, 159), (734, 165, 168), (821, 153, 175),
                       (910, 155, 184), (998, 170, 194), (1080, 201, 202)], "color": "white"}
    ],
    ("Helena", "Duluth"): [
        {"positions": [(903, 534, 0), (990, 533, 0), (1079, 531, 0),
                       (1167, 530, 0), (1255, 528, 0), (1343, 528, 0)], "color": "orange"}
    ],
    ("Seattle", "Vancouver"): [
        {"positions": [(278, 320, 90)], "color": "colorless"},
        {"positions": [(246, 320, 90)], "color": "colorless"}
    ],
    ("Portland", "Salt Lake City"): [
        {"positions": [(276, 526, 192), (360, 550, 197), (440, 590, 210), (510, 641, 215),
                       (576, 700, 228), (625, 776, 236)], "color": "blue"}
    ],
    ("San Francisco", "Salt Lake City"): [
        {"positions": [(248, 955, 163), (332, 927, 163), (412, 899, 163),
                       (495, 873, 163), (576, 846, 163)], "color": "orange"},
        {"positions": [(261, 982, 163), (343, 955, 163), (424, 928, 163),
                       (504, 902, 163), (587, 874, 163)], "color": "white"}
    ],
    ("Seattle", "Helena"): [
        {"positions": [(328, 433, 190), (416, 454, 190), (498, 470, 190),
                       (586, 489, 190), (670, 508, 190), (758, 528, 190)], "color": "yellow"}
    ],
    ("Seattle", "Portland"): [
        {"positions": [(216, 445, 110)], "color": "colorless"},
        {"positions": [(248, 453, 110)], "color": "colorless"}
    ],
    ("Salt Lake City", "Denver"): [
        {"positions": [(723, 862, 11), (808, 878, 11), (891, 894, 11)], "color": "yellow"},
        {"positions": [(729, 833, 11), (814, 849, 11), (897, 865, 11)], "color": "red"}
    ],
    ("Salt Lake City", "Las Vegas"): [
        {"positions": [(577, 1071, 138), (627, 996, 113), (649, 912, 99)], "color": "orange"}
    ],
    ("El Paso", "Dallas"): [
        {"positions": [(1054, 1358, 174), (1141, 1344, 174),
                       (1228, 1332, 174), (1314, 1319, 174)], "color": "red"}
    ],
    ("Helena", "Salt Lake City"): [
        {"positions": [(701, 752, 120), (745, 678, 120), (789, 603, 120)], "color": "pink"}
    ],
    ("San Francisco", "Los Angeles"): [
        {"positions": [(217, 1050, 65), (260, 1128, 56), (315, 1195, 45)], "color": "pink"},
        {"positions": [(192, 1068, 65), (235, 1146, 56), (290, 1211, 45)], "color": "yellow"}
    ],
    ("Santa Fe", "El Paso"): [
        {"positions": [(946, 1289, 95), (951, 1201, 95)], "color": "colorless"}
    ],
    ("Santa Fe", "Denver"): [
        {"positions": [(956, 1073, 95), (962, 983, 95)], "color": "colorless"}
    ],
    ("Denver", "Omaha"): [
        {"positions": [(1024, 863, 141), (1100, 816, 153), (1180, 785, 165),
                       (1267, 765, 173)], "color": "pink"}
    ],
    ("Denver", "Oklahoma City"): [
        {"positions": [(1015, 988, 42), (1089, 1039, 26), (1173, 1062, 11),
                       (1262, 1072, 2)], "color": "red"}
    ],
    ("Los Angeles", "Las Vegas"): [
        {"positions": [(384, 1174, 117), (452, 1117, 170)], "color": "colorless"}
    ],
    ("Los Angeles", "Phoenix"): [
        {"positions": [(423, 1230, 173), (509, 1225, 0), (598, 1236, 193)], "color": "colorless"}
    ],
    ("Los Angeles", "El Paso"): [
        {"positions": [(424, 1296, 37), (499, 1340, 27), (582, 1369, 17),
                       (669, 1385, 10), (759, 1390, 178), (844, 1376, 173)], "color": "black"}
    ],
    ("Santa Fe", "Oklahoma City"): [
        {"positions": [(1027, 1133, 170), (1115, 1123, 170), (1202, 1112, 170)], "color": "blue"}
    ],
    ("Phoenix", "El Paso"): [
        {"positions": [(715, 1288, 15), (798, 1312, 15), (883, 1337, 15)], "color": "colorless"}
    ],
    ("Phoenix", "Denver"): [
        {"positions": [(680, 1202, 112), (719, 1127, 121), (765, 1051, 126),
                       (823, 988, 141), (901, 943, 158)], "color": "white"}
    ],
    ("Phoenix", "Santa Fe"): [
        {"positions": [(731, 1230, 160), (812, 1195, 160), (893, 1159, 160)], "color": "colorless"}
    ],
    ("Helena", "Winnipeg"): [
        {"positions": [(891, 474, 135), (952, 413, 135), (1013, 350, 135),
                       (1075, 287, 135)], "color": "blue"}
    ],
    ("Duluth", "Winnipeg"): [
        {"positions": [(1178, 290, 223), (1243, 352, 223),
                       (1305, 412, 223), (1367, 473, 223)], "color": "black"}
    ],
    ("Helena", "Omaha"): [
        {"positions": [(924, 583, 25), (1004, 616, 25), (1086, 649, 25),
                       (1168, 682, 25), (1248, 716, 25)], "color": "red"}
    ],
    ("Calgary", "Helena"): [
        {"positions": [(634, 273, 50), (688, 342, 50),
                       (746, 408, 50), (802, 476, 50)], "color": "colorless"}
    ],
    ("Helena", "Denver"): [
        {"positions": [(861, 600, 67), (893, 679, 67),
                       (925, 760, 67), (958, 841, 67)], "color": "green"}
    ],
    ("Portland", "San Francisco"): [
        {"positions": [(198, 579, 116), (171, 664, 103), (161, 752, 90),
                       (163, 840, 85), (178, 926, 76)], "color": "pink"},
        {"positions": [(165, 574, 116), (139, 659, 103), (128, 747, 90),
                       (129, 835, 85), (146, 921, 76)], "color": "green"}
    ],
    ("New Orleans", "Atlanta"): [
        {"positions": [(1760, 1324, 109), (1801, 1246, 119),
                       (1853, 1174, 137), (1912, 1113, 137)], "color": "orange"},
        {"positions": [(1736, 1300, 109), (1779, 1217, 125),
                       (1830, 1150, 137), (1888, 1089, 137)], "color": "yellow"}
    ],
    ("Atlanta", "Raleigh"): [
        {"positions": [(2006, 1033, 137), (2074, 973, 137)], "color": "colorless"},
        {"positions": [(1989, 1006, 137), (2055, 948, 137)], "color": "colorless"}
    ],
    ("Montreal", "Toronto"): [
        {"positions": [(2123, 234, 155), (2052, 279, 140), (1994, 352, 115)], "color": "colorless"}
    ],
    ("Toronto", "Pittsburgh"): [
        {"positions": [(2007, 475, 87), (2014, 565, 87)], "color": "colorless"}
    ],
    ("Pittsburgh", "New York"): [
        {"positions": [(2160, 534, 148), (2080, 582, 148)], "color": "white"},
        {"positions": [(2094, 610, 148), (2170, 565, 148)], "color": "green"}
    ],
    ("Pittsburgh", "Washington"): [
        {"positions": [(2101, 678, 28), (2180, 720, 28)], "color": "colorless"}
    ],
    ("Raleigh", "Pittsburgh"): [
        {"positions": [(2058, 730, 75), (2078, 817, 75)], "color": "colorless"}
    ],
    ("Raleigh", "Nashville"): [
        {"positions": [(1878, 932, 147), (1962, 895, 164), (2047, 885, 0)], "color": "black"}
    ],
    ("Nashville", "Atlanta"): [
        {"positions": [(1881, 1008, 35)], "color": "colorless"}
    ],
    ("Montreal", "Sault St. Marie"): [
        {"positions": [(2100, 193, 0), (2013, 202, -10), (1927, 226, -13),
                       (1846, 262, 156), (1773, 312, 146)], "color": "black"}
    ],
    ("New Orleans", "Little Rock"): [
        {"positions": [(1675, 1310, 60), (1632, 1231, 60), (1592, 1152, 60)], "color": "green"}
    ],
    ("Little Rock", "Nashville"): [
        {"positions": [(1623, 1085, -5), (1708, 1062, -22), (1785, 1014, -40)], "color": "white"}
    ],
    ("Nashville", "Pittsburgh"): [
        {"positions": [(1819, 913, 120), (1863, 842, 132), (1935, 782, 148),
                       (1999, 718, 125)], "color": "yellow"}
    ],
    ("Pittsburgh", "Saint Louis"): [
        {"positions": [(1966, 685, 150), (1890, 730, 150), (1813, 772, 150),
                       (1737, 817, 150), (1660, 862, 150)], "color": "green"}
    ],
    ("Saint Louis", "Nashville"): [
        {"positions": [(1661, 926, 18), (1744, 952, 18)], "color": "colorless"}
    ],
    ("Saint Louis", "Little Rock"): [
        {"positions": [(1588, 939, 104), (1570, 1023, 104)], "color": "colorless"}
    ],
    ("Pittsburgh", "Chicago"): [
        {"positions": [(1954, 639, 5), (1866, 639, -7), (1779, 660, -15)], "color": "black"},
        {"positions": [(1941, 600, 5), (1855, 609, -7), (1765, 625, -15)], "color": "orange"}
    ],
    ("Toronto", "Sault St. Marie"): [
        {"positions": [(1885, 392, 13), (1800, 373, 13)], "color": "colorless"}
    ],
    ("Toronto", "Duluth"): [
        {"positions": [(1909, 439, -11), (1824, 451, -11), (1737, 465, -11),
                       (1650, 481, -11), (1564, 498, -11), (1476, 513, -11)], "color": "pink"}
    ],
    ("Sault St. Marie", "Winnipeg"): [
        {"positions": [(1653, 334, 13), (1566, 316, 13), (1482, 298, 13), (1395, 280, 13),
                       (1311, 262, 13), (1222, 244, 13)], "color": "colorless"}
    ],
    ("Sault St. Marie", "Duluth"): [
        {"positions": [(1656, 395, -22), (1575, 433, -22), (1494, 466, -22)], "color": "colorless"}
    ],
    ("Toronto", "Chicago"): [
        {"positions": [(1948, 465, 145), (1870, 505, 162), (1791, 543, 148),
                       (1720, 602, 135)], "color": "white"}
    ],
    ("Chicago", "Saint Louis"): [
        {"positions": [(1653, 728, 125), (1605, 804, 125)], "color": "green"},
        {"positions": [(1681, 742, 125), (1635, 815, 125)], "color": "white"}
    ],
    ("Duluth", "Omaha"): [
        {"positions": [(1371, 588, 113), (1338, 674, 113)], "color": "colorless"},
        {"positions": [(1399, 601, 113), (1368, 682, 113)], "color": "colorless"}
    ],
    ("Chicago", "Omaha"): [
        {"positions": [(1637, 665, 8), (1553, 652, 8), (1470, 673, 148),
                       (1396, 722, 148)], "color": "blue"}
    ],
    ("Chicago", "Duluth"): [
        {"positions": [(1630, 625, 13), (1543, 601, 20), (1462, 566, 25)], "color": "red"}
    ],
    ("Omaha", "Kansas City"): [
        {"positions": [(1384, 802, 64)], "color": "colorless"},
        {"positions": [(1355, 820, 64)], "color": "colorless"}
    ],
    ("Kansas City", "Saint Louis"): [
        {"positions": [(1537, 885, 0), (1450, 886, 0)], "color": "pink"},
        {"positions": [(1539, 849, 0), (1450, 853, 0)], "color": "blue"}
    ],
    ("Kansas City", "Denver"): [
        {"positions": [(1315, 878, 160), (1233, 906, 170),
                       (1146, 916, -5), (1057, 915, 5)], "color": "black"},
        {"positions": [(1317, 912, 160), (1233, 937, 170), (1144, 949, -5),
                       (1057, 951, 5)], "color": "orange"}
    ],
    ("Kansas City", "Oklahoma City"): [
        {"positions": [(1369, 934, 109), (1344, 1017, 109)], "color": "colorless"},
        {"positions": [(1401, 942, 109), (1374, 1027, 109)], "color": "colorless"}
    ],
    ("Little Rock", "Oklahoma City"): [
        {"positions": [(1498, 1083, 0), (1405, 1086, 0)], "color": "colorless"}
    ],
    ("Little Rock", "Dallas"): [
        {"positions": [(1504, 1147, 128), (1452, 1219, 128)], "color": "colorless"}
    ],
    ("New Orleans", "Houston"): [
        {"positions": [(1642, 1371, -10), (1555, 1386, -10)], "color": "colorless"}
    ],
    ("Dallas", "Houston"): [
        {"positions": [(1447, 1332, 47)], "color": "colorless"},
        {"positions": [(1425, 1354, 47)], "color": "colorless"}
    ],
    ("Houston", "El Paso"): [
        {"positions": [(1425, 1434, -17), (1338, 1456, -10), (1251, 1462, 2),
                       (1164, 1452, 7), (1078, 1435, 17), (996, 1399, 30)], "color": "green"}
    ],
    ("El Paso", "Oklahoma City"): [
        {"positions": [(1010, 1330, 165), (1092, 1296, 155), (1168, 1252, 150),
                       (1237, 1197, 136), (1294, 1131, 128)], "color": "yellow"}
    ],
    ("Oklahoma City", "Dallas"): [
        {"positions": [(1352, 1149, 82), (1362, 1234, 82)], "color": "colorless"},
        {"positions": [(1381, 1144, 82), (1393, 1231, 82)], "color": "colorless"}
    ]
}

CARDS =  [
    "orange.png",
    "black.png",
    "blue.png",
    "green.png",
    "pink.png",
    "red.png",
    "white.png",
    "yellow.png",
    "wild.png"
]

PLAYER_CARDS = {
    "Orange" : [2560, 1150, CARDS[0]],
    "Black" : [2840, 1150, CARDS[1]],
    "Blue" : [3120, 1150, CARDS[2]],
    "Green" : [2560, 1330, CARDS[3]],
    "Pink" : [2840, 1330, CARDS[4]],
    "Red" : [3120, 1330, CARDS[5]],
    "White" : [2560, 1510, CARDS[6]],
    "Yellow" : [2840, 1510, CARDS[7]],
    "Wild" : [3120, 1510, CARDS[8]]
}

FACEUP_CARDS = {
    "First" : [-60, 630],
    "Second" : [-60, 830],
    "Third" : [-60, 1030],
    "Fourth" : [-60, 1230],
    "Fifth" : [-60, 1430]
}

DEST_CARDS = {
    "First" : [2840, 270],
    "Second" : [3120, 270],
    "Third" : [2560, 450],
    "Fourth" : [2840, 450],
    "Fifth" : [3120, 450],
    "Sixth" : [2560, 630],
    "Seventh" : [2840, 630],
    "Eighth" : [3120, 630]
}

EXIT_BUTTON = (128, 0, 0)
SAVE_BUTTON = (0, 153, 0)

ROUTES_LST = [("Vancouver", "Seattle", 1, "colorless"), ("Vancouver", "Seattle", 1, "colorless"),
          ("Vancouver", "Calgary", 3, "colorless"), ("Seattle", "Portland", 1, "colorless"),
          ("Seattle", "Portland", 1, "colorless"), ("Seattle", "Calgary", 4, "colorless"),
          ("Seattle", "Helena", 6, "yellow"), ("Portland", "San Francisco", 5, "green"),
          ("Portland", "San Francisco", 5, "pink"), ("Portland", "Salt Lake City", 6, "blue"),
          ("San Francisco", "Salt Lake City", 5, "white"),
          ("San Francisco", "Salt Lake City", 5, "orange"),
          ("San Francisco", "Los Angeles", 3, "yellow"),
          ("San Francisco", "Los Angeles", 3, "pink"),
          ("Los Angeles", "Las Vegas", 2, "colorless"), ("Los Angeles", "Phoenix", 3, "colorless"),
          ("Los Angeles", "El Paso", 6, "black"), ("Calgary", "Helena", 4, "colorless"),
          ("Calgary", "Winnipeg", 6, "white"), ("Helena", "Salt Lake City", 3, "pink"),
          ("Helena", "Winnipeg", 4, "blue"), ("Helena", "Duluth", 6, "orange"),
          ("Helena", "Omaha", 5, "red"), ("Helena", "Denver", 4, "green"),
          ("Salt Lake City", "Denver", 3, "red"), ("Salt Lake City", "Denver", 3, "yellow"),
          ("Salt Lake City", "Las Vegas", 3, "orange"), ("Phoenix", "Denver", 5, "white"),
          ("Phoenix", "Santa Fe", 3, "colorless"), ("Phoenix", "El Paso", 3, "colorless"),
          ("Winnipeg", "Duluth", 4, "black"), ("Winnipeg", "Sault St. Marie", 6, "colorless"),
          ("Denver", "Omaha", 4, "pink"), ("Denver", "Oklahoma City", 4, "red"),
          ("Denver", "Santa Fe", 2, "colorless"), ("Denver", "Kansas City", 4, "black"),
          ("Denver", "Kansas City", 4, "orange"), ("Santa Fe", "El Paso", 2, "colorless"),
          ("Santa Fe", "Oklahoma City", 3, "blue"), ("El Paso", "Oklahoma City", 5, "yellow"),
          ("El Paso", "Dallas", 4, "red"), ("El Paso", "Houston", 6, "green"),
          ("Duluth", "Omaha", 2, "colorless"), ("Duluth", "Omaha", 2, "colorless"),
          ("Duluth", "Sault St. Marie", 3, "colorless"),
          ("Duluth", "Chicago", 3, "red"), ("Duluth", "Toronto", 6, "pink"),
          ("Omaha", "Chicago", 4, "blue"), ("Omaha", "Kansas City", 1, "colorless"),
          ("Omaha", "Kansas City", 1, "colorless"), ("Kansas City", "Saint Louis", 2, "pink"),
          ("Kansas City", "Saint Louis", 2, "blue"),
          ("Kansas City", "Oklahoma City", 2, "colorless"),
          ("Kansas City", "Oklahoma City", 2, "colorless"),
          ("Oklahoma City", "Dallas", 2, "colorless"),
          ("Oklahoma City", "Dallas", 2, "colorless"),
          ("Oklahoma City", "Little Rock", 2, "colorless"),
          ("Dallas", "Houston", 1, "colorless"), ("Dallas", "Houston", 1, "colorless"),
          ("Dallas", "Little Rock", 2, "colorless"), ("Houston", "New Orleans", 2, "colorless"),
          ("Sault St. Marie", "Montreal", 5, "black"),
          ("Sault St. Marie", "Toronto", 2, "colorless"),
          ("Chicaco", "Toronto", 4, "white"), ("Chicaco", "Saint Louis", 2, "white"),
          ("Chicaco", "Saint Louis", 2, "green"), ("Chicaco", "Pittsburgh", 3, "black"),
          ("Chicaco", "Pittsburgh", 3, "orange"), ("Saint Louis", "Pittsburgh", 5, "green"),
          ("Saint Louis", "Nashville", 2, "colorless"),
          ("Saint Louis", "Little Rock", 2, "colorless"),
          ("Little Rock", "Nashville", 3, "white"), ("Little Rock", "New Orleans", 3, "green"),
          ("New Orleans", "Atlanta", 4, "yellow"), ("New Orleans", "Atlanta", 4, "orange"),
          ("New Orleans", "Miami", 6, "red"), ("Toronto", "Montreal", 3, "colorless"),
          ("Toronto", "Pittsburgh", 2, "colorless"), ("Pittsburgh", "New York", 2, "white"),
          ("Pittsburgh", "New York", 2, "green"), ("Pittsburgh", "Nashville", 4, "yellow"),
          ("Pittsburgh", "Washington", 2, "colorless"), ("Pittsburgh", "Raleigh", 2, "colorless"),
          ("Nashville", "Atlanta", 1, "colorless"), ("Nashville", "Raleigh", 3, "black"),
          ("Atlanta", "Raleigh", 2, "colorless"),  ("Atlanta", "Raleigh", 2, "colorless"),
          ("Atlanta", "Charleston", 2, "colorless"), ("Atlanta", "Miami", 5, "blue"),
          ("Charleston", "Raleigh", 2, "colorless"), ("Charleston", "Miami", 4, "pink"),
          ("Raleigh", "Washington", 2, "colorless"), ("Raleigh", "Washington", 2, "colorless"),
          ("Washington", "New York", 2, "orange"), ("Washington", "New York", 2, "black"),
          ("New York", "Montreal", 4, "blue"), ("New York", "Boston", 2, "red"),
          ("New York", "Boston", 2, "yellow"), ("Boston", "Montreal", 2, "colorless"),
          ("Boston", "Montreal", 2, "colorless")]

DESTINATIONS = [("Boston", "Miami", 12), ("Calgary", "Phoenix", 13),
                ("Calgary", "Salt Lake City", 7),
                ("Chicago", "New Orleans", 7), ("Chicago", "Santa Fe", 9),
                ("Dallas", "New York", 11),
                ("Denver", "El Paso", 4), ("Denver", "Pittsburgh", 11),
                ("Duluth", "El Paso", 10),
                ("Duluth", "Houston", 8), ("Helena", "Los Angeles", 8),
                ("Kansas City", "Houston", 5),
                ("Los Angeles", "Chicago", 16), ("Los Angeles", "Miami", 20),
                ("Los Angeles", "New York", 21),
                ("Montreal", "Atlanta", 9), ("Montreal", "New Orleans", 13),
                ("New York", "Atlanta", 6),
                ("Portland", "Nashville", 17), ("Portland", "Phoenix", 11),
                ("San Francisco", "Atlanta", 17),
                ("Sault St. Marie", "Nashville", 8), ("Sault St. Marie", "Oklahoma City", 9),
                ("Seattle", "Los Angeles", 9), ("Seattle", "New York", 22),
                ("Toronto", "Miami", 10),
                ("Vancouver", "Montreal", 20), ("Vancouver", "Santa Fe", 13),
                ("Winnipeg", "Houston", 12), ("Winnipeg", "Little Rock", 11)]
