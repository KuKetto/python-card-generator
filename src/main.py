import os;
from zzCardCodeGenerator import *;
from carddatabase import CardDataBase;

def main():
    FABCube_database_raw_json = "https://raw.githubusercontent.com/the-fab-cube/flesh-and-blood-cards/develop/json/english/card.json";
    cardDataBase = CardDataBase(FABCube_database_raw_json);
    result: Result = {
        'cardType': {},
        'attackValue': {},
        'blockValue': {},
        'cardName': {},
        'pitchValue': {},
        'cardCost': {},
        'cardSubtype': {},
        'characterHealth': {},
        'rarity': {},
        'is1H': {},
        'cardClass': {},
        'cardTalent': {},
    };

    for card in cardDataBase.instance.cards: GetCardData(card, result);
    current_dir = os.path.dirname(os.path.abspath(__file__));
    output_path = os.path.join(current_dir, '..', 'output', 'experimental.php');
    OutputResult(result, output_path);

if __name__ == "__main__":
    main()