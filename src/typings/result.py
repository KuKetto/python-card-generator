from typing import TypedDict, Dict

class Result(TypedDict):
    cardType: Dict[str, str]
    attackValue: Dict[str, int]
    blockValue: Dict[str, int]
    cardName: Dict[str, str]
    pitchValue: Dict[str, int]
    cardCost: Dict[str, int]
    cardSubtype: Dict[str, str]
    characterHealth: Dict[str, int]
    rarity: Dict[str, str]
    is1H: Dict[str, bool]
    cardClass: Dict[str, str]
    cardTalent: Dict[str, str]