from typing import Union
from typings.containers import Printings

class Card:
    def __init__(self) -> None:
        self.unique_id: str = "";
        self.name: str = "";
        self.pitch: Union[int, str, None] = None;
        self.cost: Union[int, str, None] = None;
        self.power: Union[int, str, None] = None;
        self.defense: Union[int, str, None] = None;
        self.health: Union[int, str, None] = None;
        self.intelligence: Union[int, str, None] = None;
        self.types: list[str] = [];
        self.card_keywords: list[str] = [];
        self.abilities_and_effects: list[str] = [];
        self.ability_and_effect_keywords: list[str] = [];
        self.granted_keywords: list[str] = [];
        self.removed_keywords: list[str] = [];
        self.interacts_with_keywords: list[str] = [];
        self.functional_text: str = "";
        self.functional_text_plain: str = "";
        self.type_text: str = "";
        self.played_horizontally: bool = False;
        self.blitz_legal: bool = False;
        self.cc_legal: bool = False;
        self.commoner_legal: bool = False;
        self.blitz_living_legend: bool = False;
        self.blitz_living_legend_start: Union[str, None] = None;
        self.cc_living_legend: bool = False;
        self.cc_living_legend_start: Union[str, None] = None;
        self.blitz_banned: bool = False;
        self.blitz_banned_start: Union[str, None] = None;
        self.cc_banned: bool = False;
        self.cc_banned_start: Union[str, None] = None;
        self.commoner_banned: bool = False;
        self.commoner_banned_start: Union[str, None] = None;
        self.upf_banned: bool = False;
        self.upf_banned_start: Union[str, None] = None;
        self.blitz_suspended: bool = False;
        self.blitz_suspended_start: Union[str, None] = None;
        self.blitz_suspended_end: Union[str, None] = None;
        self.cc_suspended: bool = False;
        self.cc_suspended_start: Union[str, None] = None;
        self.cc_suspended_end: Union[str, None] = None;
        self.commoner_suspended: bool = False;
        self.commoner_suspended_start: Union[str, None] = None;
        self.commoner_suspended_end: Union[str, None] = None;
        self.referenced_cards: Union[list[str], None] = None;
        self.cards_referenced_by: Union[list[str], None] = None;
        self.printings: list[Printings] = [];
        self.rarity: str = "NA";

    def init_card(self, json_data: dict):
        ''' Parsing based on json schema
            - if pitch, cost, power, defense, health, and intelligence exist they get converted to int
                ValueError means the value is specific, either * or X then the original str value is kept
            - if a value does not exists (not required by the json schema) it's skipped and it
                keeps it's original None value
        '''
        self.unique_id = json_data["unique_id"];
        self.name = json_data["name"];
        if json_data["pitch"] != "": 
            try:
                self.pitch = int(json_data["pitch"]);
            except ValueError:
                self.pitch = json_data["pitch"];
        if json_data["cost"] != "": 
            try:
                self.cost = int(json_data["cost"]);
            except ValueError:
                self.cost = json_data["cost"];
        if json_data["power"] != "":
            try:
                self.power = int(json_data["power"]);
            except ValueError:
                self.power = json_data["power"];
        if json_data["defense"] != "":
            try:
                self.defense = int(json_data["defense"]);
            except ValueError:
                self.defense = json_data["defense"];
        if json_data["health"] != "":
            try:
                self.health = int(json_data["health"]);
            except ValueError:
                self.health = json_data["health"];
        if json_data["intelligence"] != "":
            try:
                self.intelligence = int(json_data["intelligence"]);
            except ValueError:
                self.intelligence = json_data["intelligence"];
        self.types = json_data["types"];
        self.card_keywords = json_data["card_keywords"];
        self.abilities_and_effects = json_data["abilities_and_effects"];
        self.ability_and_effect_keywords = json_data["ability_and_effect_keywords"];
        self.granted_keywords = json_data["granted_keywords"];
        self.removed_keywords = json_data["removed_keywords"];
        self.interacts_with_keywords = json_data["interacts_with_keywords"];
        self.functional_text = json_data["functional_text"];
        self.functional_text_plain = json_data["functional_text_plain"];
        self.type_text = json_data["type_text"];
        self.played_horizontally = json_data["played_horizontally"];
        self.blitz_legal = json_data["blitz_legal"];
        self.cc_legal = json_data["cc_legal"];
        self.commoner_legal = json_data["commoner_legal"];
        self.blitz_living_legend = json_data["blitz_living_legend"];
        if "blitz_living_legend_start" in json_data and json_data["blitz_living_legend_start"] is not None:
            self.blitz_living_legend_start = json_data["blitz_living_legend_start"];
        self.cc_living_legend = json_data["cc_living_legend"];
        if "cc_living_legend_start" in json_data and json_data["cc_living_legend_start"] is not None:
            self.cc_living_legend_start = json_data["cc_living_legend_start"];
        self.blitz_banned = json_data["blitz_banned"];
        if "blitz_banned_start" in json_data and json_data["blitz_banned_start"] is not None:
            self.blitz_banned_start = json_data["blitz_banned_start"];
        self.cc_banned = json_data["cc_banned"];
        if "cc_banned_start" in json_data and json_data["cc_banned_start"] is not None:
            self.cc_banned_start = json_data["cc_banned_start"];
        self.commoner_banned = json_data["commoner_banned"];
        if "commoner_banned_start" in json_data and json_data["commoner_banned_start"] is not None:
            self.commoner_banned_start = json_data["commoner_banned_start"];
        self.upf_banned = json_data["upf_banned"];
        if "upf_banned_start" in json_data and json_data["upf_banned_start"] is not None:
            self.upf_banned_start = json_data["upf_banned_start"];
        self.blitz_suspended = json_data["blitz_suspended"];
        if "blitz_suspended_start" in json_data and json_data["blitz_suspended_start"] is not None:
            self.blitz_suspended_start = json_data["blitz_suspended_start"];
        if "blitz_suspended_end" in json_data and json_data["blitz_suspended_end"] is not None:
            self.blitz_suspended_end = json_data["blitz_suspended_end"];
        self.cc_suspended = json_data["cc_suspended"];
        if "cc_suspended_start" in json_data and json_data["cc_suspended_start"] is not None:
            self.cc_suspended_start = json_data["cc_suspended_start"];
        if "cc_suspended_end" in json_data and json_data["cc_suspended_end"] is not None:
            self.cc_suspended_end = json_data["cc_suspended_end"];
        self.commoner_suspended = json_data["commoner_suspended"];
        if "commoner_suspended_start" in json_data and json_data["commoner_suspended_start"] is not None:
            self.commoner_suspended_start = json_data["commoner_suspended_start"];
        if "commoner_suspended_end" in json_data and json_data["commoner_suspended_end"] is not None:
            self.commoner_suspended_end = json_data["commoner_suspended_end"];
        if "referenced_cards" in json_data and json_data["referenced_cards"] is not None:
            self.referenced_cards = json_data["referenced_cards"];
        if "cards_referenced_by" in json_data and json_data["cards_referenced_by"] is not None:
            self.cards_referenced_by = json_data["cards_referenced_by"];
        self.printings = json_data["printings"];
        if len(self.printings) > 0: self.rarity = self.printings[0]["rarity"];