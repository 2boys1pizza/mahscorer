from tiles import *
from mahjongkers import *

def score(hand, table_wind, seat_wind, my_mahjongkers, sequence_hand_mult, triplet_hand_mult, half_flush_hand_mult, flush_hand_mult):
    points = 0
    mult = 1

    # score melds
    for meld in hand.melds: 
        if meld.typing != "none":
            kong_mult = 1;
            if len(meld.tiles) == 4:
                kong_mult = 2;
            for tile in meld.tiles:
                if tile.suit == "wind":
                    if tile.rank == table_wind.rank:
                        points += tile.points * kong_mult
                    if tile.rank == seat_wind.rank:
                        points += tile.points * kong_mult
                else:
                    points += tile.points * kong_mult
                # prio 1, tile jongkers
                for mahjongker in my_mahjongkers:
                    if mahjongker.priority == 1:
                        evaluated_score = mahjongker.eval_score(tile)
                        points += evaluated_score[0] * kong_mult
                        mult += evaluated_score[1] * kong_mult
            # prio 2, meld jongkers
            for mahjongker in my_mahjongkers:
                if mahjongker.priority == 2:
                    evaluated_score = mahjongker.eval_score(meld)
                    points += evaluated_score[0]
                    mult += evaluated_score[1]

    # score eyes if at least 3 melds. Mahjong needs to be checked
    if len(hand.melds) >= 3 and hand.eyes:
        for tile in hand.eyes[0].tiles:
            if tile.suit == "wind":
                if tile.rank == table_wind.rank:
                    points += tile.points
                if tile.rank == seat_wind.rank:
                    points += tile.points
            else:
                points += tile.points
        # prio 3, eyes jongkers
        for mahjongker in my_mahjongkers:
            if mahjongker.priority == 3:
                evaluated_score = mahjongker.eval_score(hand.eyes[0])
                points += evaluated_score[0]
                mult += evaluated_score[1]

    # score hand.. needs some ordering to pick best hand? or do hands stack?
    if len(hand.melds) >= 3 and len(hand.eyes) >= 1:
        if hand.is_sequence:
            mult = sequence_hand_mult
        if hand.is_triplet:
            mult = triplet_hand_mult
        if hand.is_flush:
            mult = half_flush_hand_mult
        elif hand.is_half_flush:
            mult = flush_hand_mult

        # prio 4, hand jongkers
        for mahjongker in my_mahjongkers:
            if mahjongker.priority == 4:
                evaluated_score = mahjongker.eval_score(hand)
                points += evaluated_score[0]
                mult += evaluated_score[1]

    # prio 5, non-interative jongkers
    for mahjongker in my_mahjongkers:
        if mahjongker.priority == 5:
            evaluated_score = mahjongker.eval_score()
            points += evaluated_score[0]
            mult += evaluated_score[1]

    return (points, mult)

# my_hand = Hand()
# meld1 = Meld()
# meld1.add_tile(all_tiles["bamboo"]["1"])
# meld1.add_tile(all_tiles["bamboo"]["1"])
# meld1.add_tile(all_tiles["bamboo"]["1"])
# print(meld1.typing)
# print(meld1.suit)
# meld2 = Meld()
# meld2.add_tile(all_tiles["bamboo"]["1"])
# meld2.add_tile(all_tiles["bamboo"]["2"])
# meld2.add_tile(all_tiles["bamboo"]["3"])
# print(meld2.typing)
# print(meld2.suit)
# meld3 = Meld()
# meld3.add_tile(all_tiles["bamboo"]["5"])
# meld3.add_tile(all_tiles["bamboo"]["5"])
# meld3.add_tile(all_tiles["bamboo"]["5"])
# print(meld3.typing)
# print(meld3.suit)
# eyes = Eyes()
# eyes.add_tile(all_tiles["bamboo"]["6"])
# eyes.add_tile(all_tiles["bamboo"]["6"])
# my_hand.add_meld(meld1)
# my_hand.add_meld(meld2)
# my_hand.add_meld(meld3)
# my_hand.add_eyes(eyes)

# print(my_hand.is_sequence)
# print(my_hand.is_triplet)
# print(my_hand.is_half_flush)
# print(my_hand.is_flush)

# score(my_hand, "west", "west")