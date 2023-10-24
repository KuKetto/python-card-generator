from typing import TypedDict

class DoubleSidedCardInfo(TypedDict):
    other_face_unique_id: str
    is_front: bool
    is_DFC: bool

class Printings(TypedDict):
    unique_id: str
    set_printing_unique_id: str
    id: str
    set_id: str
    edition: str
    foiling: str
    rarity: str
    artist: str
    art_variation: str
    flavor_text: str
    flavor_text_plain: str
    image_url: str
    tcgplayer_product_id: str
    tcgplayer_url: str
    double_sided_card_info: list[DoubleSidedCardInfo]