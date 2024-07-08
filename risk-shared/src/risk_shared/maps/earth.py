from risk_shared.models.card_model import CardModel
from risk_shared.maps.map import Map


def create_cards() -> dict[int, CardModel]:
    cards = [
        {"card_id": 0, "territory_id": 0, "symbol": "Infantry"},
        {"card_id": 1, "territory_id": 1, "symbol": "Cavalry"},
        {"card_id": 2, "territory_id": 2, "symbol": "Artillery"},
        {"card_id": 3, "territory_id": 3, "symbol": "Artillery"},
        {"card_id": 4, "territory_id": 4, "symbol": "Cavalry"},
        {"card_id": 5, "territory_id": 5, "symbol": "Artillery"},
        {"card_id": 6, "territory_id": 6, "symbol": "Cavalry"},
        {"card_id": 7, "territory_id": 7, "symbol": "Cavalry"},
        {"card_id": 8, "territory_id": 8, "symbol": "Artillery"},
        {"card_id": 9, "territory_id": 9, "symbol": "Artillery"},
        {"card_id": 10, "territory_id": 10, "symbol": "Infantry"},
        {"card_id": 11, "territory_id": 11, "symbol": "Artillery"},
        {"card_id": 12, "territory_id": 12, "symbol": "Cavalry"},
        {"card_id": 13, "territory_id": 13, "symbol": "Artillery"},
        {"card_id": 14, "territory_id": 14, "symbol": "Cavalry"},
        {"card_id": 15, "territory_id": 15, "symbol": "Artillery"},
        {"card_id": 16, "territory_id": 16, "symbol": "Cavalry"},
        {"card_id": 17, "territory_id": 17, "symbol": "Infantry"},
        {"card_id": 18, "territory_id": 18, "symbol": "Cavalry"},
        {"card_id": 19, "territory_id": 19, "symbol": "Cavalry"},
        {"card_id": 20, "territory_id": 20, "symbol": "Artillery"},
        {"card_id": 21, "territory_id": 21, "symbol": "Infantry"},
        {"card_id": 22, "territory_id": 22, "symbol": "Infantry"},
        {"card_id": 23, "territory_id": 23, "symbol": "Infantry"},
        {"card_id": 24, "territory_id": 24, "symbol": "Infantry"},
        {"card_id": 25, "territory_id": 25, "symbol": "Cavalry"},
        {"card_id": 26, "territory_id": 26, "symbol": "Cavalry"},
        {"card_id": 27, "territory_id": 27, "symbol": "Cavalry"},
        {"card_id": 28, "territory_id": 28, "symbol": "Infantry"},
        {"card_id": 29, "territory_id": 29, "symbol": "Artillery"},
        {"card_id": 30, "territory_id": 30, "symbol": "Infantry"},
        {"card_id": 31, "territory_id": 31, "symbol": "Infantry"},
        {"card_id": 32, "territory_id": 32, "symbol": "Infantry"},
        {"card_id": 33, "territory_id": 33, "symbol": "Infantry"},
        {"card_id": 34, "territory_id": 34, "symbol": "Infantry"},
        {"card_id": 35, "territory_id": 35, "symbol": "Cavalry"},
        {"card_id": 36, "territory_id": 36, "symbol": "Cavalry"},
        {"card_id": 37, "territory_id": 37, "symbol": "Artillery"},
        {"card_id": 38, "territory_id": 38, "symbol": "Artillery"},
        {"card_id": 39, "territory_id": 39, "symbol": "Infantry"},
        {"card_id": 40, "territory_id": 40, "symbol": "Artillery"},
        {"card_id": 41, "territory_id": 41, "symbol": "Artillery"},
        {"card_id": 42, "territory_id": None, "symbol": "Wildcard"},
        {"card_id": 43, "territory_id": None, "symbol": "Wildcard"}
    ]

    cards = dict([(card["card_id"], CardModel(**card)) for card in cards])
    return cards


def create_map():
    vertices = {
        "ALASKA": 0,
        "ALBERTA": 1,
        "CENTRAL_AMERICA": 2,
        "EASTERN_US": 3,
        "GREENLAND": 4,
        "NORTHWEST_TERRITORY": 5,
        "ONTARIO": 6,
        "QUEBEC": 7,
        "WESTERN_US": 8,
        "GREAT_BRITAIN": 9,
        "ICELAND": 10,
        "NORTHERN_EUROPE": 11,
        "SCANDINAVIA": 12,
        "SOUTHERN_EUROPE": 13,
        "UKRAINE": 14,
        "WESTERN_EUROPE": 15,
        "AFGHANISTAN": 16,
        "CHINA": 17,
        "INDIA": 18,
        "IRKUTSK": 19,
        "JAPAN": 20,
        "KAMCHATKA": 21,
        "MIDDLE_EAST": 22,
        "MONGOLIA": 23,
        "SIAM": 24,
        "SIBERIA": 25,
        "URAL": 26,
        "YAKUTSK": 27,
        "ARGENTINA": 28,
        "BRAZIL": 29,
        "VENEZUELA": 30,
        "PERU": 31,
        "CONGO": 32,
        "EAST_AFRICA": 33,
        "EGYPT": 34,
        "MADAGASCAR": 35,
        "NORTH_AFRICA": 36,
        "SOUTH_AFRICA": 37,
        "EASTERN_AUSTRALIA": 38,
        "NEW_GUINEA": 39,
        "INDONESIA": 40,
        "WESTERN_AUSTRALIA": 41,
    }

    continents = {
        0 : [
                vertices["ALASKA"],
                vertices["ALBERTA"],
                vertices["CENTRAL_AMERICA"],
                vertices["EASTERN_US"],
                vertices["GREENLAND"],
                vertices["NORTHWEST_TERRITORY"],
                vertices["ONTARIO"],
                vertices["QUEBEC"],
                vertices["WESTERN_US"]
            ],
        1 : [
                vertices["GREAT_BRITAIN"],
                vertices["ICELAND"],
                vertices["NORTHERN_EUROPE"],
                vertices["SCANDINAVIA"],
                vertices["SOUTHERN_EUROPE"],
                vertices["UKRAINE"],
                vertices["WESTERN_EUROPE"],
            ],
        2 : [
                vertices["AFGHANISTAN"],
                vertices["CHINA"],
                vertices["INDIA"],
                vertices["IRKUTSK"],
                vertices["JAPAN"],
                vertices["KAMCHATKA"],
                vertices["MIDDLE_EAST"],
                vertices["MONGOLIA"],
                vertices["SIAM"],
                vertices["SIBERIA"],
                vertices["URAL"],
                vertices["YAKUTSK"],
            ],
        3: [
                vertices["ARGENTINA"],
                vertices["BRAZIL"],
                vertices["VENEZUELA"],
                vertices["PERU"],
            ],
        4: [
                vertices["CONGO"],
                vertices["EAST_AFRICA"],
                vertices["EGYPT"],
                vertices["MADAGASCAR"],
                vertices["NORTH_AFRICA"],
                vertices["SOUTH_AFRICA"]
            ],
        5: [
                vertices["EASTERN_AUSTRALIA"],
                vertices["NEW_GUINEA"],
                vertices["INDONESIA"],
                vertices["WESTERN_AUSTRALIA"],
            ],
    }

    continent_names = {
        0: "NORTH_AMERICA",
        1: "EUROPE",
        2: "ASIA",
        3: "SOUTH_AMERICA",
        4: "AFRICA",
        5: "AUSTRALIA"
    }

    continent_bonuses = {
        0 : 5,
        1 : 5,
        2 : 7,
        3 : 2,
        4 : 3,
        5 : 2,
    }

    edges = {
        vertices["ALASKA"]: [
            vertices["ALBERTA"],
            vertices["NORTHWEST_TERRITORY"],
            vertices["KAMCHATKA"],
        ],
        vertices["ALBERTA"]: [
            vertices["ONTARIO"],
            vertices["NORTHWEST_TERRITORY"],
            vertices["ALASKA"],
            vertices["WESTERN_US"],
        ],
        vertices["CENTRAL_AMERICA"]: [
            vertices["EASTERN_US"],
            vertices["WESTERN_US"],
            vertices["VENEZUELA"],
        ],
        vertices["EASTERN_US"]: [
            vertices["QUEBEC"],
            vertices["ONTARIO"],
            vertices["WESTERN_US"],
            vertices["CENTRAL_AMERICA"],
        ],
        vertices["GREENLAND"]: [
            vertices["NORTHWEST_TERRITORY"],
            vertices["ONTARIO"],
            vertices["QUEBEC"],
            vertices["ICELAND"],
        ],
        vertices["NORTHWEST_TERRITORY"]: [
            vertices["GREENLAND"],
            vertices["ALASKA"],
            vertices["ALBERTA"],
            vertices["ONTARIO"],
        ],
        vertices["ONTARIO"]: [
            vertices["QUEBEC"],
            vertices["GREENLAND"],
            vertices["NORTHWEST_TERRITORY"],
            vertices["ALBERTA"],
            vertices["WESTERN_US"],
            vertices["EASTERN_US"],
        ],
        vertices["QUEBEC"]: [
            vertices["GREENLAND"],
            vertices["ONTARIO"],
            vertices["EASTERN_US"],
        ],
        vertices["WESTERN_US"]: [
            vertices["EASTERN_US"],
            vertices["ONTARIO"],
            vertices["ALBERTA"],
            vertices["CENTRAL_AMERICA"],
        ],
        vertices["GREAT_BRITAIN"]: [
            vertices["NORTHERN_EUROPE"],
            vertices["SCANDINAVIA"],
            vertices["ICELAND"],
            vertices["WESTERN_EUROPE"],
        ],
        vertices["ICELAND"]: [
            vertices["SCANDINAVIA"],
            vertices["GREENLAND"],
            vertices["GREAT_BRITAIN"],
        ],
        vertices["NORTHERN_EUROPE"]: [
            vertices["UKRAINE"],
            vertices["SCANDINAVIA"],
            vertices["GREAT_BRITAIN"],
            vertices["WESTERN_EUROPE"],
            vertices["SOUTHERN_EUROPE"],
        ],
        vertices["SCANDINAVIA"]: [
            vertices["UKRAINE"],
            vertices["ICELAND"],
            vertices["GREAT_BRITAIN"],
            vertices["NORTHERN_EUROPE"],
        ],
        vertices["SOUTHERN_EUROPE"]: [
            vertices["MIDDLE_EAST"],
            vertices["UKRAINE"],
            vertices["NORTHERN_EUROPE"],
            vertices["WESTERN_EUROPE"],
            vertices["NORTH_AFRICA"],
            vertices["EGYPT"],
        ],
        vertices["UKRAINE"]: [
            vertices["AFGHANISTAN"],
            vertices["URAL"],
            vertices["SCANDINAVIA"],
            vertices["NORTHERN_EUROPE"],
            vertices["SOUTHERN_EUROPE"],
            vertices["MIDDLE_EAST"],
        ],
        vertices["WESTERN_EUROPE"]: [
            vertices["SOUTHERN_EUROPE"],
            vertices["NORTHERN_EUROPE"],
            vertices["GREAT_BRITAIN"],
            vertices["NORTH_AFRICA"],
        ],
        vertices["AFGHANISTAN"]: [
            vertices["CHINA"],
            vertices["URAL"],
            vertices["UKRAINE"],
            vertices["MIDDLE_EAST"],
            vertices["INDIA"],
        ],
        vertices["CHINA"]: [
            vertices["MONGOLIA"],
            vertices["SIBERIA"],
            vertices["URAL"],
            vertices["AFGHANISTAN"],
            vertices["INDIA"],
            vertices["SIAM"],
        ],
        vertices["INDIA"]: [
            vertices["SIAM"],
            vertices["CHINA"],
            vertices["AFGHANISTAN"],
            vertices["MIDDLE_EAST"],
        ],
        vertices["IRKUTSK"]: [
            vertices["KAMCHATKA"],
            vertices["YAKUTSK"],
            vertices["SIBERIA"],
            vertices["MONGOLIA"],
        ],
        vertices["JAPAN"]: [
            vertices["KAMCHATKA"],
            vertices["MONGOLIA"],
        ],
        vertices["KAMCHATKA"]: [
            vertices["ALASKA"],
            vertices["YAKUTSK"],
            vertices["IRKUTSK"],
            vertices["MONGOLIA"],
            vertices["JAPAN"],
        ],
        vertices["MIDDLE_EAST"]: [
            vertices["INDIA"],
            vertices["AFGHANISTAN"],
            vertices["UKRAINE"],
            vertices["SOUTHERN_EUROPE"],
            vertices["EGYPT"],
            vertices["EAST_AFRICA"],
        ],
        vertices["MONGOLIA"]: [
            vertices["JAPAN"],
            vertices["KAMCHATKA"],
            vertices["IRKUTSK"],
            vertices["SIBERIA"],
            vertices["CHINA"],
        ],
        vertices["SIAM"]: [
            vertices["CHINA"],
            vertices["INDIA"],
            vertices["INDONESIA"],
        ],
        vertices["SIBERIA"]: [
            vertices["YAKUTSK"],
            vertices["URAL"],
            vertices["CHINA"],
            vertices["MONGOLIA"],
            vertices["IRKUTSK"],
        ],
        vertices["URAL"]: [
            vertices["SIBERIA"],
            vertices["UKRAINE"],
            vertices["AFGHANISTAN"],
            vertices["CHINA"],
        ],
        vertices["YAKUTSK"]: [
            vertices["KAMCHATKA"],
            vertices["SIBERIA"],
            vertices["IRKUTSK"],
        ],
        vertices["ARGENTINA"]: [
            vertices["BRAZIL"],
            vertices["PERU"],
        ],
        vertices["BRAZIL"]: [
            vertices["NORTH_AFRICA"],
            vertices["VENEZUELA"],
            vertices["PERU"],
            vertices["ARGENTINA"],
        ],
        vertices["VENEZUELA"]: [
            vertices["CENTRAL_AMERICA"],
            vertices["PERU"],
            vertices["BRAZIL"],
        ],
        vertices["PERU"]: [
            vertices["BRAZIL"],
            vertices["VENEZUELA"],
            vertices["ARGENTINA"],
        ],
        vertices["CONGO"]: [
            vertices["EAST_AFRICA"],
            vertices["NORTH_AFRICA"],
            vertices["SOUTH_AFRICA"],
        ],
        vertices["EAST_AFRICA"]: [
            vertices["MIDDLE_EAST"],
            vertices["EGYPT"],
            vertices["NORTH_AFRICA"],
            vertices["CONGO"],
            vertices["SOUTH_AFRICA"],
            vertices["MADAGASCAR"],
        ],
        vertices["EGYPT"]: [
            vertices["MIDDLE_EAST"],
            vertices["SOUTHERN_EUROPE"],
            vertices["NORTH_AFRICA"],
            vertices["EAST_AFRICA"],
        ],
        vertices["MADAGASCAR"]: [
            vertices["EAST_AFRICA"],
            vertices["SOUTH_AFRICA"],
        ],
        vertices["NORTH_AFRICA"]: [
            vertices["EAST_AFRICA"],
            vertices["EGYPT"],
            vertices["SOUTHERN_EUROPE"],
            vertices["WESTERN_EUROPE"],
            vertices["BRAZIL"],
            vertices["CONGO"],
        ],
        vertices["SOUTH_AFRICA"]: [
            vertices["MADAGASCAR"],
            vertices["EAST_AFRICA"],
            vertices["CONGO"],
        ],
        vertices["EASTERN_AUSTRALIA"]: [
            vertices["NEW_GUINEA"],
            vertices["WESTERN_AUSTRALIA"],
        ],
        vertices["NEW_GUINEA"]: [
            vertices["INDONESIA"],
            vertices["WESTERN_AUSTRALIA"],
            vertices["EASTERN_AUSTRALIA"],
        ],
        vertices["INDONESIA"]: [
            vertices["NEW_GUINEA"],
            vertices["SIAM"],
            vertices["WESTERN_AUSTRALIA"],
        ],
        vertices["WESTERN_AUSTRALIA"]: [
            vertices["EASTERN_AUSTRALIA"],
            vertices["NEW_GUINEA"],
            vertices["INDONESIA"],
        ],
    }

    return Map(vertices=vertices, edges=edges, continents=continents, continent_names=continent_names, continent_bonuses=continent_bonuses)