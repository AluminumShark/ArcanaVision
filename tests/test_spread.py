"""測試牌陣引擎。"""

import pytest

from arcanavision.cards.deck import draw_cards, load_deck
from arcanavision.spreads.engine import assign_positions, list_spreads, load_spread


def test_load_spread_three_card():
    spread = load_spread("three_card")
    assert spread.name_zh == "聖三角"
    assert spread.card_count == 3
    assert len(spread.positions) == 3


def test_load_spread_celtic_cross():
    spread = load_spread("celtic_cross")
    assert spread.card_count == 10
    assert len(spread.positions) == 10


def test_load_spread_not_found():
    with pytest.raises(FileNotFoundError):
        load_spread("nonexistent")


def test_list_spreads_returns_all():
    spreads = list_spreads()
    assert len(spreads) == 6
    ids = {s.id for s in spreads}
    assert ids == {
        "daily_draw",
        "three_card",
        "timeline",
        "four_elements",
        "relationship",
        "celtic_cross",
    }


def test_assign_positions():
    deck = load_deck()
    spread = load_spread("three_card")
    drawn = draw_cards(deck, spread.card_count)
    assigned = assign_positions(drawn, spread)

    assert assigned[0].position_name == "過去"
    assert assigned[1].position_name == "現在"
    assert assigned[2].position_name == "未來"


def test_assign_positions_mismatch():
    deck = load_deck()
    spread = load_spread("three_card")
    drawn = draw_cards(deck, 5)  # wrong count
    with pytest.raises(ValueError):
        assign_positions(drawn, spread)


def test_all_spreads_card_count_matches_positions():
    for spread in list_spreads():
        assert spread.card_count == len(spread.positions), (
            f"{spread.id}: card_count={spread.card_count} != positions={len(spread.positions)}"
        )
