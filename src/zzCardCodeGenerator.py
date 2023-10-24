from typing import Literal, Dict, Union, Any;
from io import TextIOWrapper;
from containers.card import Card;
from containers.cardsSeen import CardsSeen;
from typings.result import Result;

def OutputResult(result: Result, file_path: str) -> None:
    file = open(file_path, "w");
    file.write("<?php\n\n");

    WriteKeyValuePairs(file, result["cardType"], "CardType", "AA");
    WriteKeyValuePairs(file, result["attackValue"], "AttackValue", 0);
    WriteKeyValuePairs(file, result["blockValue"], "BlockValue", 3);
    WriteKeyValuePairs(file, result["cardName"], "CardName", "");
    WriteKeyValuePairs(file, result["pitchValue"], "PitchValue", 1);
    WriteKeyValuePairs(file, result["cardCost"], "CardCost", 0);
    WriteKeyValuePairs(file, result["cardSubtype"], "CardSubtype", "");
    WriteKeyValuePairs(file, result["cardClass"], "CardClass", "NONE");
    WriteKeyValuePairs(file, result["cardTalent"], "CardTalent", "NONE");
    WriteKeyValuePairs(file, result["characterHealth"], "CharacterHealth", 20);
    WriteKeyValuePairs(file, result["rarity"], "Rarity", "C");
    WriteKeyValuePairs(file, result["is1H"], "Is1H", False);

    file.write("?>");
    file.close();

def WriteKeyValuePairs(file: TextIOWrapper, result_dict: Dict[str, Any], specifier: str, default_value: Any) -> None:
    file.write("$" + specifier + "Dict = array(\n");
    is_first_loop = True;
    for key, value in result_dict.items():
        if value is None: continue;
        if is_first_loop: is_first_loop = False;
        else: file.write(",\n");
        file.write("\t'" + key + "' => ");
        if isinstance(value, str): file.write("'" + value.replace("'", "\\'") + "'");
        else: file.write(str(value));
    file.write("\n);\n\n");
    file.write("function Generated" + specifier + "2($cardID) {\n");
    file.write("\tglobal $" + specifier + "Dict;")
    file.write("\tif (strlen($cardID) < 6) return \"\";\n");
    file.write("\tif (is_int($cardID)) return \"\";\n");
    file.write("\treturn $" + specifier + "Dict[$cardID] ?? ");
    if isinstance(default_value, str): file.write("'" + default_value + "'");
    else: file.write(str(default_value));
    file.write(";\n}\n\n");

def GetCardData(card: Card, result: Result) -> None:
    parsedPrinting: list[str] = [];
    for printing in card.printings:
        cardID = printing["id"];
        set = printing["id"][0:3];
        cardNumber = int(printing["id"][3:6]);
        if not IsValidCard(set, cardNumber): continue;
        if printing.get("double_sided_card_info") is not None:
            if printing["double_sided_card_info"][0]["is_front"] and card.rarity == "T":
                cardNumber += 400;
                cardID = set + str(cardNumber);
        elif printing["id"] in parsedPrinting or CardsSeen().WasCardSeen(printing["id"]): continue;
        CardsSeen().AddCardAsSeen(printing["id"]);
        parsedPrinting.append(printing["id"]);
        ParseCard(card, result, cardID, cardNumber);
        if ShouldDuplicate(card): ParseCard(card, result, set + str(cardNumber + 400), cardNumber + 400);

def ParseCard(card: Card, result: Result, cardID: str, cardNumber: int) -> None:
    GetCardTypes(card, result["cardType"], cardID, cardNumber);
    GetCardAttackValue(card, result["attackValue"], cardID);
    GetCardBlockValue(card, result["blockValue"], cardID);
    GetCardName(card, result["cardName"], cardID);
    GetCardPitchValue(card, result["pitchValue"], cardID);
    GetCardCost(card, result["cardCost"], cardID);
    ParseCardTypes(card, result["cardSubtype"], result["cardClass"], result["cardTalent"], cardID);
    GetCharacterHealth(card, result["characterHealth"], cardID);
    GetCardRarity(card, result["rarity"], cardID);
    Is1H(card, result["is1H"], cardID);
    
def GetCardTypes(card: Card, cardType: Dict[str, str], cardID: str, cardNumber: int) -> None:
    type = MapType(card.types, cardNumber);
    if not IsTermEmpty(type, "AA"): cardType[cardID] = type;

def GetCardAttackValue(card: Card, attackValue: Dict[str, int], cardID: str) -> None:
    attackValue[cardID] = card.power;

def GetCardBlockValue(card: Card, blockValue: Dict[str, int], cardID: str) -> None:
    if card.defense is not None: blockValue[cardID] = card.defense;
    else: blockValue[cardID] = -1;

def GetCardName(card: Card, cardName: Dict[str, str], cardID: str) -> None:
    cardName[cardID] = card.name;

def GetCardPitchValue(card: Card, pitchValue: Dict[str, int], cardID: str) -> None:
    if card.pitch is not None: pitchValue[cardID] = card.pitch;
    else: pitchValue[cardID] = 0;

def GetCardCost(card: Card, cardCost: Dict[str, int], cardID: str) -> None:
    if isinstance(card.cost, str) or card.cost is None: cardCost[cardID] = 0;
    else: cardCost[cardID] = card.cost;

def ParseCardTypes(card: Card, cardSubtype: Dict[str, str], cardClass: Dict[str, str], cardTalent: Dict[str, str], cardID: str) -> None:
    subtypes = "";
    classes = "";
    talents = "";
    for term in card.types:
        if IsTalent(term):
            if talents != "": talents += ",";
            talents += term;
        elif IsClass(term):
            if classes != "": classes += ",";
            classes += term;
        else: 
            if not IsCardType(term) and not IsHandEquipment(term):
                if subtypes != "": subtypes += ",";
                subtypes += term;
    if not IsTermEmpty(subtypes, ""): cardSubtype[cardID] = subtypes;
    if not IsTermEmpty(classes, "NONE"): cardClass[cardID] = classes;
    if not IsTermEmpty(talents, "NONE"): cardTalent[cardID] = talents;

def GetCharacterHealth(card: Card, characterHealth: Dict[str, int], cardID: str) -> None:
    if isinstance(card.health, int): characterHealth[cardID] = card.health;

def GetCardRarity(card: Card, rarity: Dict[str, str], cardID: str) -> None:
    rarity[cardID] = card.rarity;

def Is1H(card: Card, is1H: Dict[str, bool], cardID: str) -> None:
    if "1H" in card.types: is1H[cardID] = True;

def MapType(cardTypes: list[str], cardNumber: int) -> Literal['DR', 'AR', 'W', 'C', 'E', 'T', 'R', 'M', 'ALLY', 'D', 'B', 'AA', 'A', 'I', '-']:
    hasAction = False;
    hasAttack = False;
    hasInstant = False;
    if "Action" in cardTypes: hasAction = True;
    if "Attack" in cardTypes: hasAttack = True;
    if "Defense Reaction" in cardTypes: return "DR";
    if "Attack Reaction" in cardTypes: return "AR";
    if "Weapon" in cardTypes: return "W";
    if "Hero" in cardTypes: return "C";
    if "Instant" in cardTypes: hasInstant = True;
    if "Equipment" in cardTypes and (cardNumber >= 400 or (not hasAction and not hasInstant)): return "E";
    if "Token" in cardTypes: return "T";
    if "Resource" in cardTypes: return "R";
    if "Mentor" in cardTypes: return "M";
    if "Ally" in cardTypes: return "ALLY";
    if "Demi-Hero" in cardTypes: return "D";
    if "Block" in cardTypes: return "B";
    if hasAttack and hasAction: return "AA";
    if hasAction: return "A";
    if hasInstant: return "I";
    return "-";

def IsValidCard(set: str, cardNumber: int) -> bool:
    if set not in ["WTR", "ARC", "CRU", "MON", "ELE", "EVR", "UPR", "DYN", "OUT", "DVR", "RVD", "DTD", "LGS", "HER", "FAB", "TCC", "EVO"]: return False;
    if set == "LGS" and cardNumber < 156: return False;
    if set == "HER" and cardNumber < 84: return False;
    if set == "FAB" and cardNumber < 161: return False;
    return True;

def IsTermEmpty(term: Union[str, Any], defaultValue: Any) -> bool:
    if term == "" or term == "-" or term == "*" or term == defaultValue: return True;
    return False;

def IsCardType(term: str) -> bool:
    if term in ["Action", "Attack", "Defense Reaction", "Attack Reaction", "Instant", "Weapon", "Hero", "Equipment", "Token", "Resource", "Mentor"]: return True;
    return False;

def IsClass(term: str) -> bool:
    if term in ["Generic", "Warrior", "Ninja", "Brute", "Guardian", "Wizard", "Mechanologist", "Ranger", "Runeblade", "Illusionist", "Assassin", "Shapeshifter", "Merchant", "Arbiter", "Bard"]: return True;
    return False;

def IsTalent(term: str) -> bool:
    if term in ["Elemental", "Light", "Shadow", "Draconic", "Ice", "Lightning", "Earth"]: return True;
    return False;

def IsHandEquipment(term: str) -> bool:
    if term in ["1H", "2H"]: return True;
    return False;

def ShouldDuplicate(card: Card) -> bool:
    return ("Action" in card.types or "Instant" in card.types) and "Equipment" in card.types;