class CardsSeen:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CardsSeen, cls).__new__(cls);
        
            cls.cards: list[str] = [];
        return cls.instance;

    def WasCardSeen(self, cardID: str) -> bool: return cardID in self.cards;
    def AddCardAsSeen(self, cardID: str) -> None: self.cards.append(cardID);