"""
Ticket to Ride Board
With dictionaries for cities including paths
"""
import time

import arcade
import platform

PLAYER_SCALING = 0.05

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
    "Los Angeles": {"San Francisco": 3, "Las Vegas": 2, "Phoenix": 3, "El Paso": 6},
    "Calgary": {"Vancouver": 3, "Seattle": 4, "Helena": 4, "Winnipeg": 6},
    "Helena": {"Calgary": 4, "Seattle": 6, "Salt Lake City": 3, "Winnipeg": 4, "Duluth": 6, "Omaha": 5, "Denver": 4},
    "Salt Lake City": {"Portland": 6, "San Francisco": 5, "Las Vegas": 3, "Denver": 3, "Helena": 3},
    "Las Vegas": {"Salt Lake City": 3, "Los Angeles": 2},
    "Phoenix": {"Los Angeles": 3, "Denver": 5, "Santa Fe": 3, "El Paso": 3},
    "Winnipeg": {"Calgary": 6, "Helena": 4, "Duluth": 4, "Sault St. Marie": 6},
    "Denver": {"Helena": 4, "Salt Lake City": 3, "Phoenix": 5, "Omaha": 4, "Oklahoma City": 4, "Santa Fe": 2, "Kansas City": 4},
    "Santa Fe": {"Denver": 2, "Phoenix": 3, "El Paso": 2, "Oklahoma City": 3},
    "El Paso": {"Santa Fe": 2, "Phoenix": 3, "Los Angeles": 6, "Oklahoma City": 5, "Dallas": 4, "Houston": 6},
    "Duluth": {"Winnipeg": 4, "Helena": 6, "Omaha": 2, "Chicago": 3, "Toronto": 6, "Sault St. Marie": 3},
    "Omaha": {"Duluth": 2, "Helena": 5, "Chicago": 4, "Kansas City": 1, "Denver": 4},
    "Kansas City": {"Omaha": 1, "Denver": 4, "Saint Louis": 2, "Oklahoma City": 2},
    "Oklahoma City": {"Kansas City": 2, "Denver": 4, "El Paso": 5, "Dallas": 2, "Little Rock": 2, "Santa Fe": 3},
    "Dallas": {"El Paso": 4, "Houston": 1, "Oklahoma City": 2, "Little Rock": 2},
    "Houston": {"Dallas": 1, "El Paso": 6, "New Orleans": 2},
    "Sault St. Marie": {"Winnipeg": 6, "Duluth": 3, "Montreal": 5, "Toronto": 2},
    "Chicago": {"Toronto": 4, "Duluth": 3, "Omaha": 4, "Saint Louis": 2, "Pittsburgh": 3},
    "Saint Louis": {"Chicago": 2, "Pittsburgh": 5, "Nashville": 2, "Little Rock": 2, "Kansas City": 2},
    "Little Rock": {"Saint Louis": 2, "Nashville": 3, "New Orleans": 3, "Dallas": 2, "Oklahoma City": 2},
    "New Orleans": {"Little Rock": 3, "Houston": 2, "Atlanta": 4, "Miami": 6},
    "Toronto": {"Sault St. Marie": 2, "Montreal": 3, "Duluth": 6, "Chicago": 4, "Pittsburgh": 2},
    "Pittsburgh": {"Toronto": 2, "Chicago": 3, "New York": 2, "Saint Louis": 5, "Nashville": 4, "Washington": 2, "Raleigh": 2},
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
    ("Seattle", "Calgary"): [[(335, 385, 0), (424, 380, 172), (503, 347, 143), (560, 278, 118)]],
    ("Calgary", "Vancouver"): [[(341, 238, 174), (429, 230, 174), (517, 219, 174)]],
    ("Helena", "Duluth"): [[(905, 533, 0), (992, 533, 0), (1079, 532, 0), (1167, 531, 0), (1255, 530, 0), (1343, 529, 0)]],
    ("Seattle", "Vancouver"): [[(278, 320, 90)], [(246, 320, 90)]],
    ("Portland", "Salt Lake City"): [[(276, 526, 192), (360, 550, 197), (440, 590, 202), (508, 640, 207), (574, 698, 220), (625, 776, 234)]],
    ("San Francisco", "Salt Lake City"): [[(220, 900, 163), (300, 950, 163), (400, 900, 163), (500, 870, 163), (600, 820, 163)]],
    ("Seattle", "Helena"): [[(328, 433, 190), (416, 454, 190), (498, 470, 190), (586, 489, 190), (670, 508, 190), (758, 528, 190)]],
    ("Seattle", "Portland"): [[(216,445, 110)], [(248, 453, 110)]],
    ("Montreal", "Boston"):[[(2252, 230, 220), (2320, 288, 220)], [(2232, 256, 220), (2301, 313, 220)]],
    ("Boston", "New York"): [[(2320, 394, 123), (2273, 470, 123)], [(2346, 414, 123), (2298, 488, 123)]],
    ("Montreal", "New York"): [[(2182, 280, 80), (2196, 367, 80), (2210, 456, 80)]],
    ("New York", "Washington"): [[(2262, 595, 85), (2270, 682, 85)], [(2234, 593, 85), (2240, 683, 85)]],
    ("Washington", "Raleigh"): [[(2226, 811, 130), (2170, 877, 130)], [(2200, 792, 130), (2146, 856, 130)]],
    ("Raleigh", "Charleston"): [[(2163, 954, 35), (2205, 1014, 116)]],
    ("Charleston", "Miami"): [[(2183, 1137, 85), (2192, 1223, 80), (2211, 1309, 70), (2247, 1390, 60)]],
    ("Miami", "Atlanta"): [[(2211, 1402, 48), (2152, 1335, 48), (2100, 1267, 48), (2042, 1198, 48), (1990, 1130, 48)]],
    ("Miami", "New Orleans"): [[(2193, 1438, 45), (2130, 1377, 38), (2060, 1327, 30), (1973, 1306, 0), (1887, 1317, -11), (1805, 1350, -28)]],
    ("Atlanta", "Charleston"): [[(2028, 1080, 0), (2114, 1084, 0)]],
    ("Salt Lake City", "Denver"): [[(723, 862, 11), (808, 878, 11), (891, 894, 11)], [(729, 833, 11), (814, 849, 11), (897, 865, 11)]],
    ("El Paso", "Dallas"): [[(1020, 1360, 18), (1115, 1358, 10), (1210, 1348, 4), (1295, 1330, 0)]],
    ("Helena", "Salt Lake City"): [[(775, 610, 72), (735, 695, 76), (695, 775, 78)]],
    ("San Francisco", "Los Angeles"): [[(215, 1060, 65), (275, 1145, 58), (330, 1220, 52)]],
    ("Santa Fe", "El Paso"): [[(952, 1195, 82), (950, 1275, 84)]],
    ("Santa Fe", "Denver"): [[(960, 1040, 160), (968, 975, 163)]],
    ("Phoenix", "El Paso"): [[(730, 1295, 12), (815, 1320, 8), (890, 1340, 5)]],
    ("Helena", "Winnipeg"): [[(910, 430, 172), (975, 370, 176), (1040, 315, 179), (1095, 268, 181)]],
    ("Helena", "Omaha"): [[(910, 595, 28), (1005, 635, 24), (1100, 672, 20), (1195, 707, 16), (1275, 738, 12)]],
    ("Calgary", "Helena"): [[(630, 285, 112), (690, 355, 118), (745, 425, 122), (795, 490, 126)]],
    ("Portland", "San Francisco"): [[(149, 443, 75), (144, 518, 78), (140, 592, 82), (136, 668, 85), (132, 731, 87)]],
    ("New Orleans", "Atlanta"): [[(1760, 1324, 109), (1801, 1246, 119), (1853, 1174, 137), (1912, 1113, 137)], [(1736, 1300, 109), (1779, 1217, 125), (1830, 1150, 137), (1888, 1089, 137)]],
    ("Atlanta", "Raleigh"): [[(2006, 1033, 137), (2074, 973, 137)], [(1989, 1006, 137), (2055, 948, 137)]],
    ("Montreal", "Toronto"): [[(2123, 234, 155), (2052, 279, 140), (1994, 352, 115)]],
    ("Toronto", "Pittsburgh"): [[(2007, 475, 87), (2014, 565, 87)]],
    ("Pittsburgh", "New York"): [[(2160, 534, 148), (2080, 582, 148)], [(2094, 610, 148), (2170, 565, 148)]],
    ("Pittsburgh", "Washington"): [[(2101, 678, 28), (2180, 720, 28)]],
    ("Raleigh", "Pittsburgh"): [[(2058, 730, 75), (2078, 817, 75)]],
    ("Raleigh", "Nashville"): [[(1878, 932, 147), (1962, 895, 164), (2047, 885, 0)]],
    ("Nashville", "Atlanta"): [[(1881, 1008, 35)]],
    ("Montreal", "Sault St. Marie"): [[(2100, 193, 0), (2013, 202, -10), (1927, 226, -13), (1846, 262, 156), (1773, 312, 146)]],
    ("New Orleans", "Little Rock"): [[(1675, 1310, 60), (1632, 1231, 60), (1592, 1152, 60)]],
    ("Little Rock", "Nashville"): [[(1623, 1085, -5), (1708, 1062, -22), (1785, 1014, -40)]],
    ("Nashville", "Pittsburgh"): [[(1819, 913, 120), (1863, 842, 132), (1935, 782, 148), (1999, 718, 125)]],
    ("Pittsburgh", "Saint Louis"): [[(1966, 685, 150), (1890, 730, 150), (1813, 772, 150), (1737, 817, 150), (1660, 862, 150)]],
    ("Saint Louis", "Nashville"): [[(1661, 926, 18), (1744, 952, 18)]],
    ("Saint Louis", "Little Rock"): [[(1588, 939, 104), (1570, 1023, 104)]],
    ("Pittsburgh", "Chicago"): [[(1954, 639, 5), (1866, 639, -7), (1779, 660, -15)], [(1941, 600, 5), (1855, 609, -7), (1765, 625, -15)]],
    ("Toronto", "Sault St. Marie"): [[(1885, 392, 13), (1800, 373, 13)]],
    ("Toronto", "Duluth"): [[(1909, 439, -11), (1824, 451, -11), (1737, 465, -11), (1650, 481, -11), (1564, 498, -11), (1476, 513, -11)]]
}

"""
TRAINS = {
    ("Seattle", "Calgary"): [[(335, 385, 0), (424, 380, 172), (503, 347, 143), (560, 278, 118)]],
    ("Calgary", "Vancouver"): [[(341, 238, 174), (429, 230, 174), (517, 219, 174)]],
    ("Helena", "Duluth"): [[(903, 534, 0), (990, 533, 0), (1079, 531, 0), (1167, 530, 0), (1255, 528, 0), (1343, 528, 0)]],
    ("Seattle", "Vancouver"): [[(278, 320, 90)], [(246, 320, 90)]],
    ("Portland", "Salt Lake City"): [[(276, 526, 192), (360, 550, 197), (440, 590, 210), (510, 641, 215), (576, 700, 228), (625, 776, 236)]],
    ("San Francisco", "Salt Lake City"): [[(248, 955, 163), (332, 927, 163), (412, 899, 163), (495, 873, 163), (576, 846, 163)], [(261, 982, 163), (343, 955, 163), (424, 928, 163), (504, 902, 163), (587, 874, 163)]],
    ("Seattle", "Helena"): [[(328, 433, 190), (416, 454, 190), (498, 470, 190), (586, 489, 190), (670, 508, 190), (758, 528, 190)]],
    ("Seattle", "Portland"): [[(216,445, 110)], [(248, 453, 110)]],
    ("Montreal", "Boston"):[[(2252, 230, 220), (2320, 288, 220)], [(2232, 256, 220), (2301, 313, 220)]],
    ("Boston", "New York"): [[(2320, 394, 213), (2273, 470, 213)], [(2346, 414, 213), (2298, 488, 213)]],
    ("Montreal", "New York"): [[(2182, 280, 80), (2196, 367, 80), (2210, 456, 80)]],
    ("New York", "Washington"): [[(2262, 595, 85), (2270, 682, 85)], [(2234, 593, 85), (2240, 683, 85)]],
    ("Washington", "Raleigh"): [[(2226, 811, 220), (2170, 877, 220)], [(2200, 792, 220), (2146, 856, 220)]],
    ("Raleigh", "Charleston"): [[(2163, 954, 35), (2205, 1014, 26)]],
    ("Charleston", "Miami"): [[(2183, 1137, 85), (2192, 1223, 80), (2211, 1309, 70), (2247, 1390, 60)]],
    ("Miami", "Atlanta"): [[(2211, 1402, 48), (2152, 1335, 48), (2100, 1267, 48), (2042, 1198, 48), (1990, 1130, 48)]],
    ("Miami", "New Orleans"): [[(2193, 1438, 45), (2130, 1377, 38), (2060, 1327, 30), (1973, 1306, 0), (1887, 1317, -11), (1805, 1350, -28)]],
    ("Atlanta", "Charleston"): [[(2028, 1080, 0), (2114, 1084, 0)]],
    ("Salt Lake City", "Denver"): [[(723, 862, 11), (808, 878, 11), (891, 894, 11)], [(729, 833, 11), (814, 849, 11), (897, 865, 11)]],
    ("El Paso", "Dallas"): [[(1054, 1358, 174), (1141, 1344, 174), (1228, 1332, 174), (1314, 1319, 174)]],
    ("Helena", "Salt Lake City"): [[(701, 752, 120), (745, 678, 120), (789, 603, 120)]],
    ("San Francisco", "Los Angeles"): [[(217, 1050, 65), (260, 1128, 56), (315, 1195, 45)], [(192, 1068, 65), (235, 1146, 56), (290, 1211, 45)]],
    ("Santa Fe", "El Paso"): [[(946, 1289, 95), (951, 1201, 95)]],
    ("Santa Fe", "Denver"): [[(956, 1073, 95), (962, 983, 95)]],
    ("Los Angeles", "Las Vegas"): [[(384, 1174, 117), (452, 1117, 170)]],
    ("Santa Fe", "Oklahoma"): [[(1027, 1133, 170), (1115, 1123, 170), (1202, 1112, 170)]],
    ("Phoenix", "El Paso"): [[(715, 1288, 15), (798, 1312, 15), (883, 1337, 15)]],
    ("Phoenix", "Santa Fe"): [[(731, 1230, 160), (812, 1195, 160), (893, 1159, 160)]],
    ("Helena", "Winnipeg"): [[(891, 474, 135), (952, 413, 135), (1013, 350, 135), (1075, 287, 135)]],
    ("Helena", "Omaha"): [[(924, 583, 25), (1004, 616, 25), (1086, 649, 25), (1168, 682, 25), (1248, 716, 25)]],
    ("Calgary", "Helena"): [[(634, 273, 50), (688, 342, 50), (746, 408, 50), (802, 476, 50)]],
    ("Helena", "Denver"): [[(861, 600, 67), (893, 679, 67), (925, 760, 67), (958, 841, 67)]],
    ("Portland", "San Francisco"): [[(198, 579, 116), (171, 664, 103), (161, 752, 90), (163, 840, 85), (178, 926, 76)], [(165, 574, 116), (139, 659, 103), (128, 747, 90), (129, 835, 85), (146, 921, 76)]],
    ("New Orleans", "Atlanta"): [[(1760, 1324, 109), (1801, 1246, 119), (1853, 1174, 47), (1912, 1113, 47)], [(1736, 1300, 109), (1779, 1217, 125), (1830, 1150, 47), (1888, 1089, 47)]],
    ("Atlanta", "Raleigh"): [[(2006, 1033, 47), (2074, 973, 47)], [(1989, 1006, 47), (2055, 948, 47)]],
    ("Montreal", "Toronto"): [[(2123, 234, 65), (2052, 279, 50), (1994, 352, 115)]],
    ("Toronto", "Pittsburgh"): [[(2007, 475, 87), (2014, 565, 87)]],
    ("Pittsburgh", "New York"): [[(2160, 534, 58), (2080, 582, 58)], [(2094, 610, 58), (2170, 565, 58)]],
    ("Pittsburgh", "Washington"): [[(2101, 678, 28), (2180, 720, 28)]],
    ("Raleigh", "Pittsburgh"): [[(2058, 730, 75), (2078, 817, 75)]],
    ("Raleigh", "Nashville"): [[(1878, 932, 57), (1962, 895, 74), (2047, 885, 0)]],
    ("Nashville", "Atlanta"): [[(1881, 1008, 35)]],
    ("Montreal", "Sault St. Marie"): [[(2100, 193, 0), (2013, 202, -10), (1927, 226, -13), (1846, 262, 66), (1773, 312, 56)]]
}
"""

class GameView(arcade.View):
    """
    Main application class
    """

    def __init__(self):
        """Initializer"""

        # Call the parent class initializer
        super().__init__()

        # Background image will be stored in this variable
        self.background = arcade.load_texture("images/board.png")

        # Train pieces
        # One list for all train sprites (create it ONCE)
        self.train_list = arcade.SpriteList()

        # Load textures once
        orange_train = arcade.load_texture("images/train_piece.png")

        # Create a mapping of city pairs to train sprites
        # Structure: {(city1, city2): [[sprites for route 1], [sprites for route 2]]}
        self.train_map = {}

        # Track which routes are taken
        # Structure: {(city1, city2): [False, False]} for double routes
        self.route_taken = {}

        # Build sprites from TRAINS
        for train, routes in TRAINS.items():
            self.train_map[train] = []
            self.route_taken[train] = [False] * len(routes)

            for route_positions in routes:
                route_sprites = []
                for ix, iy, angle in route_positions:
                    train_sprite = arcade.Sprite()
                    train_sprite.append_texture(orange_train)
                    train_sprite.set_texture(0)
                    train_sprite.scale = TRAIN_SCALE
                    train_sprite.angle = angle
                    train_sprite.alpha = 255  # start fully transparent
                    self.place_train_sprite(ix, iy, train_sprite, top_left=True)

                    self.train_list.append(train_sprite)
                    route_sprites.append(train_sprite)

                self.train_map[train].append(route_sprites)

        # One list for all city sprites (create it ONCE)
        self.city_list = arcade.SpriteList()

        # Load textures once
        base_tex = arcade.load_texture("images/city.png")
        hover_tex = arcade.load_texture("images/button_yellow.png")

        # Build sprites from CITIES
        for city in CITIES:
            # Skip cities with no coordinates yet
            if "CITY_IMG_X" not in CITIES[city].keys() or "CITY_IMG_Y" not in CITIES[city].keys():
                continue

            # Create one sprite per city
            self.city = arcade.Sprite()
            self.city.append_texture(base_tex)
            self.city.append_texture(hover_tex)
            self.city.set_texture(0)
            self.city.scale = CITY_SCALE

            # Position it using your helper
            self.place_city(
                CITIES[city]["CITY_IMG_X"], CITIES[city]["CITY_IMG_Y"],
                top_left=True, scale=None
            )

            # Add to the shared list
            self.city_list.append(self.city)

        self.selected_cities = []  # list of selected city sprites (max. 2)

        # Variables that will hold sprite lists
        self.player_sprite = arcade.Sprite(
            "images/cursor.png",
            scale=PLAYER_SCALING,
        )
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)


    def reset(self):
        """Restart the game."""
        # Set up the player
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50

    def img_to_screen(self, ix: float, iy: float, *, top_left: bool = False) -> tuple[float, float]:
        """
        Convert a coordinate on the background image (in image pixels) to the window/screen coordinate.
        Works because you draw the background stretched to WINDOW_*.
        """
        # Flip Y if coordinates were measured from the image's top edge
        if top_left:
            iy = self.background.height - iy

        sx = BOARD_WIDTH / self.background.width
        sy = BOARD_HEIGHT / self.background.height
        return ix * sx + BOARD_LEFT, iy * sy + BOARD_BOTTOM

    def place_city(self, ix: float, iy: float, *, top_left: bool = False, scale: float | None = None) -> None:
        """
        Position the city sprite using image-pixel coordinates.
        """
        x, y = self.img_to_screen(ix, iy, top_left=top_left)
        self.city.center_x = x
        self.city.center_y = y
        if scale is not None:
            self.city.scale = scale

    def place_train_sprite(self, ix: float, iy: float, train_sprite: arcade.Sprite, *, top_left: bool = False) -> None:
        x, y = self.img_to_screen(ix, iy, top_left=top_left)
        train_sprite.center_x = x
        train_sprite.center_y = y

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw the background texture
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(BOARD_LEFT, BOARD_BOTTOM,  BOARD_WIDTH, BOARD_HEIGHT),
        )

        # Draw all the sprites.
        self.train_list.draw()
        self.city_list.draw()
        self.player_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Called whenever the mouse moves.
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        pass

    # Helper to get the name of the city sprite in self.selected_cities
    def sprite_to_name(self, spr: arcade.Sprite) -> str:
        idx = self.city_list.index(spr)
        return list(CITIES.keys())[idx]

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Generate a list of all cities that collided with the cursor
            # fingertip = top-left corner of the cursor image
            tip_x = self.player_sprite.center_x - self.player_sprite.width / 3
            tip_y = self.player_sprite.center_y + self.player_sprite.height / 3

            # which cities are exactly under that point?
            hits = arcade.get_sprites_at_point((tip_x, tip_y), self.city_list)

            city = hits[0]

            # If this city is already selected -> deselect it
            if city in self.selected_cities:
                city.set_texture(0)
                city.scale = CITY_SCALE
                self.selected_cities.remove(city)
                return

            if len(self.selected_cities) == 0:
                # If no city is already selected, select it
                city.set_texture(1)
                city.scale = CITY_SCALE_YELLOW
                self.selected_cities.append(city)
                return

            # Otherwise, select it; if already 2 selected, drop both
            if len(self.selected_cities) == 2:
                newest = self.selected_cities.pop(1)
                newest.set_texture(0)
                newest.scale = CITY_SCALE

                oldest = self.selected_cities.pop(0)
                oldest.set_texture(0)
                oldest.scale = CITY_SCALE

            first_city_name = self.sprite_to_name(self.selected_cities[0])
            second_city_name = self.sprite_to_name(city)

            if second_city_name in ROUTES.get(first_city_name, {}):
                # Mark this one as selected
                city.set_texture(1)
                city.scale = CITY_SCALE_YELLOW
                self.selected_cities.append(city)

                # Show trains between the two selected cities
                self.show_trains_between(first_city_name, second_city_name)
                city.scale = CITY_SCALE
                self.selected_cities[0].scale = CITY_SCALE
                self.selected_cities[0].set_texture(0)
                city.set_texture(0)
                self.selected_cities.clear()

            # if this point is reached it means that the second city is
            # not adjacent to the first, so it must not be connected by a path

    # Actions to make if specific buttons are pressed
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.reset()
        elif symbol == arcade.key.ESCAPE:
            self.window.close()

    def show_trains_between(self, city1, city2):
        """Show train sprites for a route between two connected cities."""
        city_pair = (city1, city2)
        reverse_pair = (city2, city1)

        # Determine which pair exists
        if city_pair in self.train_map:
            pair = city_pair
        elif reverse_pair in self.train_map:
            pair = reverse_pair
        else:
            return

        # Find first available route (not taken)
        for i, taken in enumerate(self.route_taken[pair]):
            if not taken:
                # Mark this route as taken
                self.route_taken[pair][i] = True

                # Make all sprites for this route visible
                for train_sprite in self.train_map[pair][i]:
                    train_sprite.set_texture(0)
                    train_sprite.alpha = 255
                break


def main():
    """ Main function """
    if platform.system() == "Darwin":  # macOS
        window = arcade.Window(SCREEN_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=False)
        window.set_location(0, 0)
    else:
        window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE, fullscreen=True, resizable=False)

    game = GameView()
    game.reset()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()