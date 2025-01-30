from tiles import *
from mahjongkers import *
from math import *

def score(hand, table_wind, seat_wind, my_mahjongkers, mahjong_pts, mahjong_money):
    points = mahjong_pts
    money = mahjong_money

    # score hand.. needs some ordering to pick best hand? or do hands stack?
    # if len(hand.melds) >= 3 and len(hand.eyes) >= 1:
    #     if hand.is_sequence:
    #         mult = max(mult, sequence_hand_mult)
    #     if hand.is_triplet:
    #         mult = max(mult, triplet_hand_mult)
    #     if hand.is_half_flush:
    #         mult = max(mult, half_flush_hand_mult)
    #     if hand.is_flush:
    #         mult = max(mult, flush_hand_mult)
            
    # score melds
    for meld in hand.melds: 
        if meld.typing != "none":
            kong = False
            thunder_mult = 1
            if len(meld.tiles) == 4:
                kong_mult = True
            for tile in meld.tiles:
                if tile.seal == "thunder":
                    thunder_mult = 2
                if tile.modifier == "gold":
                    money += 5 * thunder_mult
                if tile.suit == "wind":
                    if tile.rank == table_wind.rank:
                        points += tile.points * thunder_mult
                    if tile.rank == seat_wind.rank:
                        points += tile.points * thunder_mult
                else:
                    points += tile.points * thunder_mult
                # prio 1, tile jongkers
                for mahjongker in my_mahjongkers:
                    if mahjongker.priority == 1:
                        evaluated_score = mahjongker.eval_score(tile)
                        if kong:
                            points += evaluated_score[0] * thunder_mult * 2
                        else:
                            points += evaluated_score[0] * thunder_mult

                thunder_mult = 1
            # prio 2, meld jongkers
            for mahjongker in my_mahjongkers:
                if mahjongker.priority == 2:
                    evaluated_score = mahjongker.eval_score(meld)
                    if kong:
                        points += evaluated_score[0] * 2
                        
                    else:
                        points += evaluated_score[0]
                        

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
            # prio 1, tile jongkers in eyes
            for mahjongker in my_mahjongkers:
                if mahjongker.priority == 1:
                    evaluated_score = mahjongker.eval_score(tile)
                    points += evaluated_score[0]
                    
        # prio 3, eyes jongkers
        for mahjongker in my_mahjongkers:
            if mahjongker.priority == 3:
                evaluated_score = mahjongker.eval_score(hand.eyes[0])
                points += evaluated_score[0]
                

        # prio 4, hand type jongkers
        for mahjongker in my_mahjongkers:
            if mahjongker.priority == 4:
                evaluated_score = mahjongker.eval_score(hand)
                points += evaluated_score[0]
                

    # prio 5, whole hand jongkers            
    for mahjongker in my_mahjongkers:
        if mahjongker.priority == 5:
            evaluated_score = mahjongker.eval_score(hand)
            points += evaluated_score[0]
            

    # prio 6, non-interative jongkers
    for mahjongker in my_mahjongkers:
        if mahjongker.priority == 6:
            evaluated_score = mahjongker.eval_score()
            points += evaluated_score[0]
            
            if len(evaluated_score) > 2:
                money += evaluated_score[2]

    return (points, money)

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