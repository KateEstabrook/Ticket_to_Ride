import city
import player
import route
import deck
import cards


ROUTES = [("Vancouver", "Seattle", 1, )]




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
