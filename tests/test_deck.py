"""測試牌組載入與抽牌邏輯。"""

from arcanavision.cards.deck import draw_cards, load_deck


def test_load_deck_has_78_cards():
    deck = load_deck()
    assert len(deck) == 78


def test_load_deck_major_arcana_count():
    deck = load_deck()
    majors = [c for c in deck if c.arcana == "major"]
    assert len(majors) == 22


def test_load_deck_minor_arcana_count():
    deck = load_deck()
    minors = [c for c in deck if c.arcana == "minor"]
    assert len(minors) == 56


def test_load_deck_suits():
    deck = load_deck()
    for suit in ("wands", "cups", "swords", "pentacles"):
        cards = [c for c in deck if c.suit == suit]
        assert len(cards) == 14, f"{suit} should have 14 cards, got {len(cards)}"


def test_load_deck_unique_ids():
    deck = load_deck()
    ids = [c.id for c in deck]
    assert len(ids) == len(set(ids)), "Card IDs must be unique"


def test_load_deck_all_fields_present():
    deck = load_deck()
    for card in deck:
        assert card.id
        assert card.name_en
        assert card.name_zh
        assert card.arcana in ("major", "minor")
        assert len(card.upright_keywords) == 5
        assert len(card.reversed_keywords) == 5
        assert card.upright_meaning
        assert card.reversed_meaning
        assert card.symbolism
        assert card.image_prompt_seed


def test_draw_cards_correct_count():
    deck = load_deck()
    drawn = draw_cards(deck, 3)
    assert len(drawn) == 3


def test_draw_cards_no_duplicates():
    deck = load_deck()
    drawn = draw_cards(deck, 10)
    ids = [d.card.id for d in drawn]
    assert len(ids) == len(set(ids))


def test_draw_cards_has_reversed():
    """多次抽牌後應該有正位和逆位。"""
    deck = load_deck()
    all_reversed = []
    for _ in range(20):
        drawn = draw_cards(deck, 10)
        all_reversed.extend(d.is_reversed for d in drawn)
    assert any(all_reversed), "Should have some reversed cards"
    assert not all(all_reversed), "Should have some upright cards"
