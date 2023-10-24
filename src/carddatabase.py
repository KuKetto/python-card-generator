import requests
import json
import os
from containers.card import Card

class CardDataBase:
    def __new__(cls, deck_link: str):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CardDataBase, cls).__new__(cls);
            cls.instance.__deck_link = deck_link;
            
            # not using try-catch -> if the request fails, let it crash
            raw_json = requests.get(cls.instance.__deck_link);
            if raw_json.status_code != 200: raise ValueError("Unexpected error, error code: " + str(raw_json.status_code));
            json_data = json.loads(raw_json.text);

            cls.instance.cards = [];
            for card_data in json_data:
                card = Card();
                card.init_card(card_data);
                cls.instance.cards.append(card);
        return cls.instance;