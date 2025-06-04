from tiles import *
import math

# ------------------------------------------------
# GLOBALS
# ------------------------------------------------

COMMON_MAHJONGKER_COST = 3
UNCOMMON_MAHJONGKER_COST = 8
CONSISTENCY_MAHJONGKER_COST = 8
RARE_MAHJONGKER_COST = 14
COMMON_MAHJONGKER_SELL_VALUE = 1
UNCOMMON_MAHJONGKER_SELL_VALUE = 3
CONSISTENCY_MAHJONGKER_SELL_VALUE = 4
RARE_MAHJONGKER_SELL_VALUE = 5

class Meld:
    typing = "none" # sequence, triplet
    tiles = [] # array of 3-4 Tiles
    suit = "none" # dot, bamboo, character, dragon, wind
    hidden = False

    def __init__(self):
        self.typing = "none"
        self.tiles = []
        self.suit = "none"
        self.hidden = False

    # assumes valid suit meld. sets typing
    def determine_typing(self):
        current_rank = 0 
        for i, tile in enumerate(sorted(self.tiles, key=lambda tile: tile.rank)):
            if i == 0:
                current_rank = tile.rank 
            else:
                if self.typing == "none":
                    if current_rank == tile.rank:
                        self.typing = "triplet"
                    elif current_rank == str(int(tile.rank) - 1):
                        self.typing = "sequence"
                        current_rank = tile.rank
                elif self.typing == "triplet":
                    if current_rank == tile.rank:
                        self.typing = "triplet"
                    else: 
                        self.typing = "none"
                        return
                elif self.typing == "sequence":
                    if current_rank == str(int(tile.rank) - 1):
                        self.typing = "sequence"
                        current_rank = tile.rank
                    else:
                        self.typing = "none"
                        return
        print(f"Meld typing: {self.typing}")

    def determine_suit(self):
        if self.tiles[0].suit == self.tiles[1].suit and self.tiles[0].suit == self.tiles[2].suit:
            self.suit = sorted(self.tiles, key=lambda tile: tile.rank)[0].suit
        else:
            self.suit = "none"
        print(f"Meld suit: {self.suit}")

    def add_tile(self, tile):
        if len(self.tiles) < 4:
            self.tiles.append(tile)
            if len(self.tiles) >= 3:
                self.determine_typing()
                self.determine_suit()
        else:
            print("This meld is full!")

    def __repr__(self):
        return repr(self.tiles)

    def __eq__(self, other):
        if self.suit != other.suit:
            return False
        selfranks = []
        otherranks = []
        for tile in self.tiles:
            selfranks.append(tile.rank)
        for tile in other.tiles:
            otherranks.append(tile.rank)
        while len(selfranks) != 0 and len(otherranks) != 0:
            comp = selfranks[0]
            print(comp)
            if comp in otherranks:
                selfranks.remove(comp)
                otherranks.remove(comp)
                print(selfranks)
                print(otherranks)
            else:
                return False
        print(selfranks)
        print(otherranks)
        if len(selfranks) == 0 and len(otherranks) == 0:
            return True
        else: 
            return False

class Eyes:
    tiles = [] # array of 2 Tiles
    suit = "none"

    def __init__(self):
        self.tiles = []

    def determine_suit(self):
        self.suit = self.tiles[0].suit

    def add_tile(self, tile):
        if len(self.tiles) < 2:
            self.tiles.append(tile)
        else:
            print("This pair of eyes is full!")
        if len(self.tiles) == 2:
            self.determine_suit()

    def __repr__(self):
        return repr(self.tiles)

class Hand:
    melds = [] # array of Melds
    eyes = [] # array of 1 Eyes
    is_sequence = True # sequence, triplet, half-flush, flush
    is_triplet = True
    is_half_flush = True
    is_flush = True

    def __init__(self):
        self.melds = []
        self.eyes = []

    def add_meld(self, meld):
        self.melds.append(meld)
        if len(self.melds) >= 3 and len(self.eyes) >= 1:
            self.determine_typing()

    def add_eyes(self, eyes):
        if len(self.eyes) == 1:
            self.eyes[0] = eyes
        else:
            self.eyes.append(eyes)
        if len(self.melds) >= 3 and len(self.eyes) >= 1:
            self.determine_typing()

    def determine_typing(self):
        # reset
        self.is_sequence = True
        self.is_triplet = True
        self.is_half_flush = True
        self.is_flush = True

        # check sequence hand
        for meld in self.melds:
            if meld.typing == "sequence":
                continue
            elif meld.typing == "triplet":
                if meld.suit == "dragon" or meld.suit == "wind" or meld.suit == "special":
                    continue
                else:
                    self.is_sequence = False
            else:
                self.is_sequence = False
                break

        # check all-in triplet hand
        for meld in self.melds:
            if meld.typing == "triplet":
                continue
            else:
                self.is_triplet = False
                break

        # check flush hands
        current_suit = "none"
        for meld in self.melds:
            if current_suit == "none":
                if meld.suit == "dragon" or meld.suit == "wind" or meld.suit == "special":
                    self.is_flush = False
                else:
                    current_suit = meld.suit
            elif meld.suit == current_suit:
                continue
            elif meld.suit == "dragon" or meld.suit == "wind" or meld.suit == "special":
                self.is_flush = False
            else:
                self.is_flush = False
                self.is_half_flush = False
                break
        if self.is_flush and self.eyes[0].suit != current_suit:
            self.is_flush = False
        if self.is_half_flush and self.eyes[0].suit != "dragon" and self.eyes[0].suit != "wind" and self.eyes[0].suit != "special" and self.eyes[0].suit != current_suit:
            self.is_half_flush = False

        print(f"Sequence: {self.is_sequence}")
        print(f"Triplet: {self.is_triplet}")
        print(f"Half Flush: {self.is_half_flush}")
        print(f"Flush: {self.is_flush}")

    def __repr__(self):
        return repr((self.melds, self.eyes))

class Mahjongker:
    name = "" # for jank reasons the name MUST be the same as the img_src name
    description = ""
    priority = 0 
    cost = 3
    sell_value = 1
    img_src = ""
    # lower priority gets scored first
    # 0 is for validity checking
    # 1 is for tile checking
    # 2 is for meld checking
    # 3 is for eyes checking
    # 4 is for hand type checking
    # 5 is for whole hand
    # 6 is for no interaction 

    def __repr__(self):
        return repr((self.name, self.description, self.priority))

    def __eq__(self, other):
        return self.name == other.name

    def eval_score(self, my_mahjongkers):
        print("I'm a dumb parent score func")
        return 0

# --------------------------------------------------------------------------------------
# MAHJONGKERS
# --------------------------------------------------------------------------------------

# Bamonker
class Bamonker(Mahjongker):
    name = "Bamonker"
    description = "Reveal Bamboo meld: Invest +10 pts.\nActivate: Spend $2 to use Called Shot: Bamboo"
    # priority = 2 
    # cost = COMMON_MAHJONGKER_COST
    # sell_value = COMMON_MAHJONGKER_SELL_VALUE
    # img_src = "/jongker/bamonker.jpg"

    # def eval_score(self, my_mahjongkers, meld):
    #     fluteker = Fluteker()
    #     killtonyker = KillTonyker()
    #     bamynker = Bamynker()
    #     total_score = 0
    #     if meld.suit == "bamboo":
    #         total_score += 15
    #     if meld.suit == "dot" and fluteker in my_mahjongkers:
    #         total_score += 15
    #     if meld.suit == "character" and killtonyker in my_mahjongkers:
    #         total_score += 15
    #     if bamynker in my_mahjongkers:
    #         total_score *= 2
    #     return (total_score, 0)
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bamonker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Donker
class Donker(Mahjongker):
    name = "Donker"
    description = "Reveal Dots meld: Invest +10 pts.\nActivate: Spend $2 to use Called Shot: Dots "
    # priority = 2 
    # cost = COMMON_MAHJONGKER_COST
    # sell_value = COMMON_MAHJONGKER_SELL_VALUE
    # img_src = "/jongker/donker.jpg"

    # def eval_score(self, my_mahjongkers, meld):
    #     fluteker = Fluteker()
    #     iker = Iker()
    #     dynker = Dynker()
    #     total_score = 0
    #     if meld.suit == "dot":
    #         total_score += 15
    #     if meld.suit == "bamboo" and fluteker in my_mahjongkers:
    #         total_score += 15
    #     if meld.suit == "character" and iker in my_mahjongkers:
    #         total_score += 15
    #     if dynker in my_mahjongkers:
    #         total_score *= 2
    #     return (total_score, 0)
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/donker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)


# Chonker
class Chonker(Mahjongker):
    name = "Chonker"
    description = "Reveal Character meld: Invest +10 pts.\nActivate: Spend $2 to use Called Shot: Character"
    # priority = 2 
    # cost = COMMON_MAHJONGKER_COST
    # sell_value = COMMON_MAHJONGKER_SELL_VALUE
    # img_src = "/jongker/chonker.jpg"

    # def eval_score(self, my_mahjongkers, meld):
    #     iker = Iker()
    #     killtonyker = KillTonyker()
    #     chynker = Chynker()
    #     total_score = 0
    #     if meld.suit == "character":
    #         total_score += 15
    #     if meld.suit == "bamboo" and killtonyker in my_mahjongkers:
    #         total_score += 15
    #     if meld.suit == "dot" and iker in my_mahjongkers:
    #         total_score += 15
    #     if chynker in my_mahjongkers:
    #         total_score *= 2
    #     return (total_score, 0)
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/chonker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)


# Dragonker
class Dragonker(Mahjongker):
    name = "Dragonker"
    description = "+20 pts for each dragon meld. Once each turn, you may pay $2 to use Called Shot: Dragon."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dragonker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        score = 20
        hynker = Hynker()
        if hynker in my_mahjongkers:
            score *= 2
        if meld.suit == "dragon":
            return (score, 0)
        else:
            return (0, 0)

# Wonker
class Wonker(Mahjongker):
    name = "Wonker"
    description = "+30 pts for each wind meld. Once each turn, you may pay $2 to use Called Shot: Wind."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/wonker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        score = 30
        hynker = Hynker()
        if hynker in my_mahjongkers:
            score *= 2
        if meld.suit == "wind":
            return (score, 0)
        else:
            return (0, 0)

# Sequencker
class Sequencker(Mahjongker):
    name = "Sequencker"
    description = "+2 mult for sequence hand"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/sequencker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        if hand.is_sequence:
            return (0, 2)
        else:
            return (0, 0)

# MahMahMahjonker
class MahMahMahjonker(Mahjongker):
    name = "MahMahMahjonker"
    description = "+4 mult for all in triplet hand"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/mahmahmahjonker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        if hand.is_triplet:
            return (0, 4)
        else:
            return (0, 0)

# Milwaunker
class Milwaunker(Mahjongker):
    name = "Milwaunker"
    description = "+4 mult for half flush hand"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/milwaunker.jpg"

    # what happens if hand is all honors?
    def eval_score(self, my_mahjongkers, hand):
        if hand.is_half_flush:
            return (0, 4)
        else:
            return (0, 0)

# Kohlker
class Kohlker(Mahjongker):
    name = "Kohlker"
    description = "+7 mult for flush hand"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/kohlker.jpg"

    # what happens if hand is all honors?
    def eval_score(self, my_mahjongkers, hand):
        if hand.is_flush:
            return (0, 7)
        else:
            return (0, 0)

# Windker
class Windker(Mahjongker):
    name = "Windker"
    description = "+0.3 mult for each wind meld. Once per draw phase, you may instead draw the next wind in the deck. Costs $3 per use."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/windker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        if meld.suit == "wind":
            return (0, 0.3)
        else:
            return (0, 0)

# Draker
class Draker(Mahjongker):
    name = "Draker"
    description = "+0.3 mult for each dragon meld. Once per draw phase, you may instead draw the next dragon in the deck. Costs $3 per use."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/draker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        if meld.suit == "dragon":
            return (0, 0.3)
        else:
            return (0, 0)

# Evenker
class Evenker(Mahjongker):
    name = "Evenker"
    description = "Mahjong: Gain +45 pts if your scored hand has more even tiles than odd tiles"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/evenker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        evens = 0
        odds = 0
        for meld in hand.melds:
            for tile in meld.tiles:
                if int(tile.rank) % 2 == 0:
                    evens += 1
                else:
                    odds += 1
        if evens > odds:
            return (45, 0)
        else:
            return (0, 0)

# Oddker
class Oddker(Mahjongker):
    name = "Oddker"
    description = "Mahjong: Gain +45 pts if your scored hand has more odd tiles than even tiles"
    priority = 1 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/oddker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        evens = 0
        odds = 0
        for meld in hand.melds:
            for tile in meld.tiles:
                if int(tile.rank) % 2 == 0:
                    evens += 1
                else:
                    odds += 1
        if odds > evens:
            return (45, 0)
        else:
            return (0, 0)

# AYCker
class AYCker(Mahjongker):
    name = "AYCker"
    description = "Reveal Sequence meld: Invest +10 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/aycker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Pingker
class Pingker(Mahjongker):
    name = "Pingker"
    description = "Reveal Set meld: Invest +10 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/pingker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# KingKongker
class KingKongker(Mahjongker):
    name = "KingKongker"
    description = "Reveal Quad meld: Invest +20 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/kingkongker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Gapker
class Gapker(Mahjongker):
    name = "Gapker"
    description = "Sequences can contain one gap of 1 (124 valid, 246 not valid)"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gapker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# DEIker
class DEIker(Mahjongker):
    name = "DEIker"
    description = "Gain +40 pts for each unique suit in your scored tiles (character, dots, bamboo, honor)."
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/deiker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        suitset = {}
        for meld in hand.melds:
            suitset.add(meld.suit)
        return (len(suitset) * 30, 0)

# SEIquenker
class SEIquenker(Mahjongker):
    name = "SEIquenker"
    description = "Sequences can contain up to two different suits (excluding honors). The suit of this meld is the majority suit of the tiles."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/seiquenker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Siker
class Siker(Mahjongker):
    name = "Siker"
    description = "Your Quads can be Sequences (e.g. 2345)"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/siker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Bourdainker
class Bourdainker(Mahjongker):
    name = "Bourdainker"
    description = "You can Chi from the player across from you"
    priority = 6 
    cost = 5
    sell_value = 2
    img_src = "/jongker/bourdainker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Dollker
class Dollker(Mahjongker):
    name = "Dollker"
    description = "Gain $3 for discarding your seat wind"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dollker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Yenker
class Yenker(Mahjongker):
    name = "Yenker"
    description = "Gain $3 for discarding the table wind"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/yenker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Falchionker
class Falchionker(Mahjongker):
    name = "Falchionker"
    description = "Gain $2 for discarding any dragon"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/falchionker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Neenjaker
class Neenjaker(Mahjongker):
    name = "Neenjaker"
    description = "+30 points for each hidden meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/neenjaker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        if meld.hidden:
            return (30, 0)
        else:
            return (0, 0)

# Gayker
class Gayker(Mahjongker):
    name = "Gayker"
    description = "Sequences can loop (912). Mahjong: Gain +30 pts for each looped sequence"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gayker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        ranks_low = []
        ranks_high = []
        for tile in meld.tiles:
            if tile.suit != "wind" and tile.suit != "dragon" and tile.suit != "special":
                if int(tile.rank) >= 4 and int(tile.rank) <= 6:
                    return (0, 0)
                else:
                    if int(tile.rank) < 4:
                        ranks_low.append(int(tile.rank))
                    else:
                        ranks_high.append(int(tile.rank))
            else:
                return (0, 0)
        if len(ranks_low) > 0 and len(ranks_high) > 0:
            return (20, 0)
        else:
            return (0, 0)

# Bumungker
class Bumungker(Mahjongker):
    name = "Bumungker"
    description = "Mahjong: Gain +25 pts for each Bamboo meld.\nReveal bamboo meld: use Called Shot: Bamboo"
    priority = 2
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bumungker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        bamynker = Bamynker()
        total_score = 0
        if meld.suit == "bamboo":
            total_score += 15
        if meld.suit == "dot" and fluteker in my_mahjongkers:
            total_score += 15
        if meld.suit == "character" and killtonyker in my_mahjongkers:
            total_score += 15
        if bamynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Dungker
class Dungker(Mahjongker):
    name = "Dungker"
    description = "Mahjong: Gain +25 pts for each Dots meld.\nReveal Dots meld: use Called Shot: Dots"
    priority = 2
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dungker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        fluteker = Fluteker()
        iker = Iker()
        dynker = Dynker()
        total_score = 0
        if meld.suit == "dot":
            total_score += 15
        if meld.suit == "bamboo" and fluteker in my_mahjongkers:
            total_score += 15
        if meld.suit == "character" and iker in my_mahjongkers:
            total_score += 15
        if dynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Chungker
class Chungker(Mahjongker):
    name = "Chungker"
    description = "Mahjong: Gain +25 pts for each Character meld. \nReveal Character meld: use Called Shot: Character"
    priority = 2
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/chungker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        iker = Iker()
        killtonyker = KillTonyker()
        chynker = Chynker()
        total_score = 0
        if meld.suit == "character":
            total_score += 15
        if meld.suit == "bamboo" and killtonyker in my_mahjongkers:
            total_score += 15
        if meld.suit == "dot" and iker in my_mahjongkers:
            total_score += 15
        if chynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Dragunker
class Dragunker(Mahjongker):
    name = "Dragunker"
    description = "Gain +30 pts for each dragon meld.  When you reveal a dragon meld, you may use Called Shot: Dragon."
    priority = 2
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dragunker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        iker = Iker()
        killtonyker = KillTonyker()
        hynker = Hynker()
        total_score = 0
        if meld.suit == "dragon":
            total_score += 30
        if hynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Wunker
class Wunker(Mahjongker):
    name = "Wunker"
    description = "Gain +35 pts for each wind meld.  When you reveal a wind meld, you may use Called Shot: Wind."
    priority = 2
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/wunker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        iker = Iker()
        killtonyker = KillTonyker()
        hynker = Hynker()
        total_score = 0
        if meld.suit == "wind":
            total_score += 35
        if hynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Hungker
class Hungker(Mahjongker):
    name = "Hungker"
    description = "Mahjong: Gain +40 pts for each honor meld.\nReveal Honor meld: use Called Shot: Honor"
    priority = 2
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/hungker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        iker = Iker()
        killtonyker = KillTonyker()
        hynker = Hynker()
        total_score = 0
        if meld.suit == "wind" or meld.suit == "dragon" or meld.suit == "special":
            total_score += 30
        if hynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)


# Bimingker
class Bimingker(Mahjongker):
    name = "Bimingker"
    description = "+0.15 mult for each bamboo meld. Once per turn, you may use Called Shot: Bamboo. Costs $2 per use."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bimingker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        if meld.suit == "bamboo":
            return (0, 0.15)
        else:
            return (0, 0)

# Dingker
class Dingker(Mahjongker):
    name = "Dingker"
    description = "+0.15 mult for each dot meld. Once per turn, you may use Called Shot: Dots. Costs $2 per use."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dingker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        if meld.suit == "dot":
            return (0, 0.15)
        else:
            return (0, 0)

# Chingker
class Chingker(Mahjongker):
    name = "Chingker"
    description = "+0.15 mult for each character meld. Once per turn, you may use Called Shot: Character. Costs $2 per use."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/chingker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        if meld.suit == "character":
            return (0, 0.15)
        else:
            return (0, 0)

# Hoardker
class Hoardker(Mahjongker):
    name = "Hoardker"
    description = "When you would gain an item, you gain two items instead of one"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/hoardker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Meldker
class Meldker(Mahjongker):
    name = "Meldker"
    description = "If the last 3 tiles you discarded form a meld, +30 points (stacking) Current: 0"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/meldker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Snakeker
class Snakeker(Mahjongker):
    name = "Snakeker"
    description = "Every turn you may roll 2 d6, if they are snake eyes gain $11"
    priority = 3 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/snakeker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

    # def eval_score(self, my_mahjongkers, eyes):
    #     for tile in eyes.tiles:
    #         if tile.rank != "1":
    #             return (0, 0)
    #     return (111, 0)

# Seeker
class Seeker(Mahjongker):
    name = "Seeker"
    description = "You may pong your eyes at any time."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/seeker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# LeeSinker
class LeeSinker(Mahjongker):
    name = "LeeSinker"
    description = "Your eyes must be 3 tiles.  +1 hand size."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/leesinker.jpg"
    active = False

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# SeeingDoubker
class SeeingDoubker(Mahjongker):
    name = "SeeingDoubker"
    description = "+1 mult if your eyes are rank 2"
    priority = 3 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/seeingdoubker.jpg"

    def eval_score(self, my_mahjongkers, eyes):
        for tile in eyes.tiles:
            if tile.rank != "2":
                return (0, 0)
        return (0, 2)

# Seequenker
class Seequenker(Mahjongker):
    name = "Seequenker"
    description = "Your eyes can be a sequence."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/seequenker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Highker
class Highker(Mahjongker):
    name = "Highker"
    description = "Mahjong: Gain +35 points for melds containing numbered tiles where all Ranks are >= 5"
    priority = 2 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/highker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        bamynker = Bamynker()
        dynker = Dynker()
        chynker = Chynker()
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()
        score = 20
        high = True
        for tile in meld.tiles:
            if tile.suit != "wind" and tile.suit != "dragon" and tile.suit != "special":
                if int(tile.rank) < 5:
                    high = False
                    return (0, 0)
            else:
                return (0, 0)
        if high:
            if bamynker in my_mahjongkers:
                if (tile.suit == "bamboo" or 
                    tile.suit == "dot" and fluteker in my_mahjongkers or 
                    tile.suit == "character" and killtonyker in my_mahjongkers):
                    score += 20
            if chynker in my_mahjongkers:
                if (tile.suit == "character" or 
                    tile.suit == "dot" and iker in my_mahjongkers or 
                    tile.suit == "bamboo" and killtonyker in my_mahjongkers):
                    score += 20
            if dynker in my_mahjongkers:
                if (tile.suit == "dot" or 
                    tile.suit == "character" and iker in my_mahjongkers or 
                    tile.suit == "bamboo" and fluteker in my_mahjongkers):
                    score += 20
            return (score, 0)
        else:
            return (0, 0)

# Lowker
class Lowker(Mahjongker):
    name = "Lowker"
    description = "Mahjong: Gain +35 points for melds containing numbered tiles where all Ranks are <= 5"
    priority = 2 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/lowker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        bamynker = Bamynker()
        dynker = Dynker()
        chynker = Chynker()
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()
        score = 20
        low = True
        for tile in meld.tiles:
            if tile.suit != "wind" and tile.suit != "dragon" and tile.suit != "special":
                if int(tile.rank) > 5:
                    low = False
                    return (0, 0)
            else:
                return (0, 0)
        if low:
            if bamynker in my_mahjongkers:
                if (tile.suit == "bamboo" or 
                    tile.suit == "dot" and fluteker in my_mahjongkers or 
                    tile.suit == "character" and killtonyker in my_mahjongkers):
                    score += 20
            if chynker in my_mahjongkers:
                if (tile.suit == "character" or 
                    tile.suit == "dot" and iker in my_mahjongkers or 
                    tile.suit == "bamboo" and killtonyker in my_mahjongkers):
                    score += 20
            if dynker in my_mahjongkers:
                if (tile.suit == "dot" or 
                    tile.suit == "character" and iker in my_mahjongkers or 
                    tile.suit == "bamboo" and fluteker in my_mahjongkers):
                    score += 20
            return (score, 0)
        else:
            return (0, 0)

# Rainbowker
class Rainbowker(Mahjongker):
    name = "Rainbowker"
    description = "You can form a Rainbow suit meld with all three suits. Mahjong: Gain +15 pts for each Rainbow suit meld"
    priority = 2 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/rainbowker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        seen_suits = []
        for tile in meld.tiles:
            if tile.suit in seen_suits:
                return (0, 0)
            else:
                seen_suits.append(tile.suit)
        return (15, 0)

# Raindraker
class Raindraker(Mahjongker):
    name = "Raindraker"
    description = "You can form a Sequence with the dragons"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/raindraker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Magellker
class Magellker(Mahjongker):
    name = "Magellker"
    description = "You can form a Sequence with the winds"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/magellker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Salarymanker
class Salarymanker(Mahjongker):
    name = "Salarymanker"
    description = "Mahjong: Gain $6"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/salarymanker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 6)

# MealTicker
class MealTicker(Mahjongker):
    name = "MealTicker"
    description = "Chi: Gain $3 "
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/mealticker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# WenGeker
class WenGeker(Mahjongker):
    name = "WenGeker"
    description = "Pong: Gain $3 "
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/wengeker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fourker
class Fourker(Mahjongker):
    name = "Fourker"
    description = "When you Commit a meld, you may Replace a tile in your hand with a Rank 4 tile.\nMahjong: If your scored hand has four Rank 4 tiles, gain +55 pts"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/fourker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        four_count = 0
        for meld in hand.melds:
            for tile in meld.tiles:
                if tile.rank == "4":
                    fourcount += 1
        if (len(hand.eyes) != 0):
            for tile in hand.eyes[0]:
                if tile.rank == "4":
                    fourcount += 1
        if four_count >= 4:
            return (55, 0)
        return (0, 0)


# DOWker
class DOWker(Mahjongker):
    name = "DOWker"
    description = "Mahjong: Roll a D12 for DOWker's sell value"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dowker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Comebacker
class Comebacker(Mahjongker):
    name = "Comebacker"
    description = "Prelude: Gain $10 if you are in last place"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/comebacker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Underdoker
class Underdoker(Mahjongker):
    name = "Underdoker"
    description = "Mahjong: Gain pts equal to half the difference between yours and first place.\nYou cannot sell this mahjongker"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/underdoker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Compensaker
class Compensaker(Mahjongker):
    name = "Compensaker"
    description = "When you Draw an honor tile, gain $1"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/compensaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Gronkowsker
class Gronkowsker(Mahjongker):
    name = "Gronkowsker"
    description = "Prelude: Get a Wild tile"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gronkowsker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Dumpsker
class Dumpsker(Mahjongker):
    name = "Dumpsker"
    description = "Activate: Spend $3 to Exile a tile and draw a tile from the discard or Hell."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dumpsker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Copycatker
class Copycatker(Mahjongker):
    name = "Copycatker"
    description = "At the start of the round, become a copy of another player's mahjongker."
    priority = UNCOMMON_MAHJONGKER_COST
    cost = UNCOMMON_MAHJONGKER_SELL_VALUE
    sell_value = 3
    img_src = "/jongker/copycatker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Boomerangker
class Boomerangker(Mahjongker):
    name = "Boomerangker"
    description = "If this mahjonker is empty: set aside a tile face-up on this card.  After three turns, you must draw this tile during your draw step if able. You may not use this again until the start of your next turn"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/boomerangker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Doraker
class Doraker(Mahjongker):
    name = "Doraker"
    description = "A random tile is always selected from your hand. When you reveal that tile, invest +10 pts"
    priority = 6
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/doraker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers, tile):
        return point_value

# AllforOneker - needs special scoring check
class AllforOneker(Mahjongker):
    name = "AllforOneker"
    description = "All winds are the East wind."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/allforoneker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# OneforAllker
class OneforAllker(Mahjongker):
    name = "OneforAllker"
    description = "All dragons are the Red dragon"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/oneforallker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Pickgker
class Pickgker(Mahjongker):
    name = "Pickgker"
    description = "When you would gain an item, instead draw 5 and pick 1"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/pickgker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Straightker - pretty sure this shit doesn't work lol. test again later
class Straightker(Mahjongker):
    name = "Straightker"
    description = "Mahjong: For every two consecutive sequence melds in your scored hand, gain +35 pts. (e.g. 123, 456)"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/straightker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        # lows = []
        # highs = []
        total_points = 0
        for i, meld in enumerate(hand.melds):
            if meld.typing == "sequence":
                meld.tiles.sort(key=lambda tile: int(tile.rank))
                # lows.append(meld.tiles[0])
                # highs.append(meld.tiles[len(meld.tiles-1)])
                for j in range(i+1, len(hand.melds)):
                    meld2 = hand.melds[j]
                    if meld2.typing == "sequence":
                        meld2.tiles.sort(key=lambda tile: int(tile.rank))
                        if meld.tiles[len(meld)-1].rank == meld2.tiles[0].rank - 1 or meld2.tiles[len(meld)-1].rank == meld.tiles[0].rank - 1:
                            total_points += 35
        # while len(highs) > 0:
        #     for i, high in enumerate(highs):
        #         for low in lows:
        #             if int(high) == int(low) - 1:
        #                 total_points += 35
        #                 highs.remove(high)
        #                 lows.remove(low)
        #                 break
        #             if i == len(high - 1):
        #                 return (total_points, 0)
        return (total_points, 0)

# Arthker
class Arthker(Mahjongker):
    name = "Arthker"
    description = "-1 max hand size.\nReveal meld: Invest +8 pts"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/arthker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        return (9, 0)

# DuckDuckGooseker
class DuckDuckGooseker(Mahjongker):
    name = "DuckDuckGooseker"
    description = "Your triplets may contain one tile with a Rank difference of 1 (112 valid, 113 not valid)"
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/duckduckgooseker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# DebtCollectker
class DebtCollectker(Mahjongker):
    name = "DebtCollectker"
    description = "Pong: Steal $2 from the player that discarded the tile"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/debtcollectker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Quaker
class Quaker(Mahjongker):
    name = "Quaker"
    description = "When you kong, all other players randomly discard a tile, then draw 1."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/quaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Anthonyker
class Anthonyker(Mahjongker):
    name = "Anthonyker"
    description = "You can Chi from the player on your left"
    priority = 6 
    cost = 5
    sell_value = 2
    img_src = "/jongker/anthonyker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Picker
class Picker(Mahjongker):
    name = "Picker"
    description = "Get two free rerolls each round."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/picker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Luckgker
class Luckgker(Mahjongker):
    name = "Luckgker"
    description = "Any time you are affected by anything random, you may randomize again and choose between the outcomes, or instead gain $1."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/luckgker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Buffettker
class Buffettker(Mahjongker):
    name = "Buffettker"
    description = "Mahjong: Gain +10 pts for every $3 you have"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/buffettker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fuckgker
class Fuckgker(Mahjongker):
    name = "Fuckgker"
    description = "When you take a tile from an opponent (chi, pong, kong do NOT count), Invest +13 points"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/fuckgker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Toker
class Toker(Mahjongker):
    name = "Toker"
    description = "Activate: Randomly Exile a tile. Gain $1"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/toker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Emeraldker
class Emeraldker(Mahjongker):
    name = "Emeraldker"
    description = "Once per turn, you may use Controlled Chaos. Costs $3 per use."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/emeraldker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Snipker
class Snipker(Mahjongker):
    name = "Snipker"
    description = "Activate: Spend $1 to use Called Shot: Rank"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/snipker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Grenadeker
class Grenadeker(Mahjongker):
    name = "Grenadeker"
    description = "Activate: Spend $1 to use Called Shot: Suit"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/grenadeker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Stepsisker
class Stepsisker(Mahjongker):
    name = "Stepsisker"
    description = "Each tile taken from an opponent is worth +15 pts when scored. (chi, pong, and kong do NOT count)"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/stepsisker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# LarryEllisker
class LarryEllisker(Mahjongker):
    name = "LarryEllisker"
    description = "Activate: Spend $1 to see the next 2 tiles and Exile any of them"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/larryellisker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Suckgker
class Suckgker(Mahjongker):
    name = "Suckgker"
    description = "When you are targeted by another player, Invest +10 points"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/suckgker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# JosephJoesker
class JosephJoesker(Mahjongker):
    name = "JosephJoesker"
    description = "Before you draw, guess the suit (dots, character, bamboo, honor) of the tile you’re about to draw.  Show it, and if you are right, you gain $1"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/josephjoesker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Riggedker
class Riggedker(Mahjongker):
    name = "Riggedker"
    description = "Nothing affecting you is random. You always select."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/riggedker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fibonaccker
class Fibonaccker(Mahjongker):
    name = "Fibonaccker"
    description = "Mahjong: If your scored hand contains Ranks 1, 2, 3, 5, and 8, gain +60 points"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/fibonaccker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        ranks = {}
        total_points = 0
        for meld in hand.melds:
            for tile in meld.tiles:
                if tile.rank in ranks:
                    ranks[tile.rank] = ranks[tile.rank] + 1
                else:
                    ranks[tile.rank] = 1
        if len(hand.eyes) > 0:           
            for tile in hand.eyes[0].tiles:
                if tile.rank in ranks:
                    ranks[tile.rank] = ranks[tile.rank] + 1
                else:
                    ranks[tile.rank] = 1

        if "1" not in ranks:
            return (0, 0)

        if "2" not in ranks:
            return (0, 0)

        if "3" not in ranks:
            return (0, 0)

        if "5" not in ranks:
            return (0, 0)

        if "8" not in ranks:
            return (0, 0)

        return (60, 0)

# Wokegker
class Wokegker(Mahjongker):
    name = "Wokegker"
    description = "Mahjong: If your melds are of 3 different suits in your scored hand, gain +50 points"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/wokegker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        suits = set()
        total_points = 0
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()

        for meld in hand.melds:
            if meld.suit == "dot" or meld.suit == "bamboo" or meld.suit == "character":
                suits.add(meld.suit)

        if fluteker in my_mahjongkers and iker in my_mahjongkers and killtonyker in my_mahjongkers:
            if len(suits) >= 1:
                return (50, 0)
            else:
                return (0, 0)

        if fluteker in my_mahjongkers and iker in my_mahjongkers:
            if "dot" in suits:
                return (50, 0)
            elif len(suits) >= 2:
                return (50, 0)
            else:
                return (0, 0)

        if fluteker in my_mahjongkers and killtonyker in my_mahjongkers:
            if "bamboo" in suits:
                return (50, 0)
            elif len(suits) >= 2:
                return (50, 0)
            else:
                return (0, 0)

        if iker in my_mahjongkers and killtonyker in my_mahjongkers:
            if "character" in suits:
                return (50, 0)
            elif len(suits) >= 2:
                return (50, 0)
            else:
                return (0, 0)

        if fluteker in my_mahjongkers or iker in my_mahjongkers or killtonyker in my_mahjongkers:
            if len(suits) >= 2:
                return (50, 0)
            else:
                return (0, 0)

        if len(suits) >= 3: 
            return (50, 0)
        else:
            return (0, 0)

# Shardker
class Shardker(Mahjongker):
    name = "Shardker"
    description = "Every 10 turns, Replace a tile in your hand with a random Honor tile"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/shardker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Ponorker
class Ponorker(Mahjongker):
    name = "Ponorker"
    description = "Pong: Draw the next two honor tiles from the living wall. "
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/ponorker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Sonorker
class Sonorker(Mahjongker):
    name = "Sonorker"
    description = "Chi: Draw the next two honor tiles from the living wall. "
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/sonorker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Speedker
class Speedker(Mahjongker):
    name = "Speedker"
    description = "Gain +30 pts if you mahjong first.  Everytime you mahjong first, this value permanently goes up by +15 pts."
    priority = 4
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/speedker.jpg"
    point_value = 30

    def eval_score(self, my_mahjongkers, hand):
        self.point_value = self.point_value + 15
        return (self.point_value, 0)

# Blackjackgker
class Blackjackgker(Mahjongker):
    name = "Blackjackgker"
    description = "You can form a Blackjack type meld with tiles of the same suit that add up to 21"
    priority = 6
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/blackjackgker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Chairker
class Chairker(Mahjongker):
    name = "Chairker"
    description = "Choose an additional seat wind for yourself after drawing your opening hand."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/chairker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# AngelInvesker
class AngelInvesker(Mahjongker):
    name = "AngelInvesker"
    description = "Prelude: Choose a player to give $2 to. Whenever that player earns money, you also gain $1"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/angelinvesker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Triker
class Triker(Mahjongker):
    name = "Triker"
    description = "Trigrams all cost $1 less for you. Trigram rerolls always cost $2."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/triker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Emporerker
class Emporerker(Mahjongker):
    name = "Emporerker"
    description = "Zodiacs all cost $1 less for you. Zodiac rerolls always cost $3."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/emporerker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Empressker
class Empressker(Mahjongker):
    name = "Empressker"
    description = "For every Zodiac you get this gains +9 pts permanently. Current: 0"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/empressker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Laobanker
class Laobanker(Mahjongker):
    name = "Laobanker"
    description = "For every seal you place, this gains +5 pts permanently. Current: 0"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/laobanker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Huntker
class Huntker(Mahjongker):
    name = "Huntker"
    description = "Select a random player. When you target that player with an item or effect, gain $1 and randomly select a new player"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/huntker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Gourmetker
class Gourmetker(Mahjongker):
    name = "Gourmetker"
    description = "A seal is randomly selected each at the start of each round. When you chi a tile, add this seal to it."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gourmetker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Specialker
class Specialker(Mahjongker):
    name = "Specialker"
    description = "Worth +10 pts each time a special tile is scored by ANY player this round."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/specialker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Spoilker
class Spoilker(Mahjongker):
    name = "Spoilker"
    description = "Worth 75 - the number of discarded tiles pts at the end of the round."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/spoilker.jpg"
    point_value = 75

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Harbingker
class Harbingker(Mahjongker):
    name = "Harbingker"
    description = "Whenever an event occurs, instead draw 2 and you pick one to resolve."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/harbingker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# GoGoGaker
class GoGoGaker(Mahjongker):
    name = "GoGoGaker"
    description = "Reveal meld: Gain an item"
    priority = 6 
    cost = 5
    sell_value = 2
    img_src = "/jongker/gogogaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# DejaVuker
class DejaVuker(Mahjongker):
    name = "DejaVuker"
    description = "Your first draw each round is a tile from your previous scored hand. +10 pts when you score this tile."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dejavuker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Coilker
class Coilker(Mahjongker):
    name = "Coilker"
    description = "Whenever a random tile is picked, you may have it randomly pick again up to twice."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/coilker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Donnerker
class Donnerker(Mahjongker):
    name = "Donnerker"
    description = "At the start of each round, choose another mahjongker to eat. This mahjongker permanently gains 15 points."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/donnerker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Trashker
class Trashker(Mahjongker):
    name = "Trashker"
    description = "Activate: Exile a tile, Draw the most recently discarded tile"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/trashker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Trapker
class Trapker(Mahjongker):
    name = "Trapker"
    description = "After drawing your opening hand, name a tile.  The first 2 times another player draws that tile, they MUST discard it for their end of turn."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/trapker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Sprayker
class Sprayker(Mahjongker):
    name = "Sprayker"
    description = "Whenever you use a Called Shot, choose a second player to target"
    priority = 6 
    cost = 6
    sell_value = 2
    img_src = "/jongker/sprayker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Vanillaker
class Vanillaker(Mahjongker):
    name = "Vanillaker"
    description = "If you have a complete and valid hand at the end of the round, +20 pts."
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/vanillaker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        if (len(hand.melds) == 4):
            return (20, 0)     
        return (0, 0)

# NoReservaker
class NoReservaker(Mahjongker):
    name = "NoReservaker"
    description = "You may chi from all players."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/noreservaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Bamanker
class Bamanker(Mahjongker):
    name = "Bamanker"
    description = "Gain +5 pts for each scored bamboo tile."
    priority = 1 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bamanker.jpg"

    def eval_score(self, my_mahjongkers, tile):
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        bamynker = Bamynker()
        total_score = 0
        if tile.suit == "bamboo":
            total_score += 5
        if tile.suit == "dot" and fluteker in my_mahjongkers:
            total_score += 5
        if tile.suit == "character" and killtonyker in my_mahjongkers:
            total_score += 5
        if bamynker in my_mahjongkers:
            total_score *= 2

        return (total_score, 0)

# Danker
class Danker(Mahjongker):
    name = "Danker"
    description = "Gain +5 pts for each scored dots tile."
    priority = 1 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/danker.jpg"

    def eval_score(self, my_mahjongkers, tile):
        fluteker = Fluteker()
        iker = Iker()
        dynker = Dynker()
        total_score = 0

        if tile.suit == "dot":
            total_score += 5
        if tile.suit == "bamboo" and fluteker in my_mahjongkers:
            total_score += 5
        if tile.suit == "character" and iker in my_mahjongkers:
            total_score += 5
        if dynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Chanker
class Chanker(Mahjongker):
    name = "Chanker"
    description = "Gain +5 pts for each scored char tile."
    priority = 1 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/chanker.jpg"

    def eval_score(self, my_mahjongkers, tile):
        iker = Iker()
        killtonyker = KillTonyker()
        chynker = Chynker()
        total_score = 0
        if tile.suit == "character":
            total_score += 5
        if tile.suit == "bamboo" and killtonyker in my_mahjongkers:
            total_score += 5
        if tile.suit == "dot" and iker in my_mahjongkers:
            total_score += 5
        if chynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Miniker
class Miniker(Mahjongker):
    name = "Miniker"
    description = "Mahjong: Gain pts equal to 8x the rank of the lowest rank tile scored"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/miniker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        ranks = []
        for meld in hand.melds:
            if meld.suit != "dragon" and meld.suit != "wind" and meld.suit != "special":
                for tile in meld.tiles:
                    ranks.append(int(tile.rank))
        if hand.eyes and hand.eyes[0].suit != "dragon" and hand.eyes[0].suit != "wind" and hand.eyes[0].suit != "special":
            for tile in hand.eyes[0]:
                ranks.append(int(tile.rank))
        ranks.sort()
        if len(ranks) > 0:
            return (ranks[0] * 5, 0)
        else:
            return (0, 0)

# Honker
class Honker(Mahjongker):
    name = "Honker"
    description = "Mahjong: Gain +20 pts for each honor meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/honker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        hynker = Hynker()
        if meld.suit == "dragon" or meld.suit == "wind" or meld.suit == "special":
            if hynker in my_mahjongkers:
                return (30, 0)
            return (15, 0)
        return (0, 0)

# Eatker
class Eatker(Mahjongker):
    name = "Eatker"
    description = "Mahjong: Gain +12 pts for each sequence meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/eatker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        bamynker = Bamynker()
        dynker = Dynker()
        chynker = Chynker()
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()
        score = 10
        if meld.typing == "sequence":
            if bamynker in my_mahjongkers:
                if (meld.suit == "bamboo" or 
                    meld.suit == "dot" and fluteker in my_mahjongkers or 
                    meld.suit == "character" and killtonyker in my_mahjongkers):
                    score += 10
            if chynker in my_mahjongkers:
                if (meld.suit == "character" or 
                    meld.suit == "dot" and iker in my_mahjongkers or 
                    meld.suit == "bamboo" and killtonyker in my_mahjongkers):
                    score += 10
            if dynker in my_mahjongkers:
                if (meld.suit == "dot" or 
                    meld.suit == "character" and iker in my_mahjongkers or 
                    meld.suit == "bamboo" and fluteker in my_mahjongkers):
                    score += 10
            return (score, 0)
        return (0, 0)

# Sameker
class Sameker(Mahjongker):
    name = "Sameker"
    description = "Mahjong: Gain +10 pts for each set meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/sameker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        bamynker = Bamynker()
        dynker = Dynker()
        chynker = Chynker()
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()
        score = 10
        if meld.typing == "triplet":
            if bamynker in my_mahjongkers:
                if (meld.suit == "bamboo" or 
                    meld.suit == "dot" and fluteker in my_mahjongkers or 
                    meld.suit == "character" and killtonyker in my_mahjongkers):
                    score += 10
            if chynker in my_mahjongkers:
                if (meld.suit == "character" or 
                    meld.suit == "dot" and iker in my_mahjongkers or 
                    meld.suit == "bamboo" and killtonyker in my_mahjongkers):
                    score += 10
            if dynker in my_mahjongkers:
                if (meld.suit == "dot" or 
                    meld.suit == "character" and iker in my_mahjongkers or 
                    meld.suit == "bamboo" and fluteker in my_mahjongkers):
                    score += 10
            return (score, 0)
        return (0, 0)

# Odiumker
class Odiumker(Mahjongker):
    name = "Odiumker"
    description = "Invest +5 pts when you discard an honor tile."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/odiumker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Bamenker
class Bamenker(Mahjongker):
    name = "Bamenker"
    description = "This mahjongker permanently gains +7 pts each time you score a bamboo meld. Current: 0"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bamenker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Denker
class Denker(Mahjongker):
    name = "Denker"
    description = "This mahjongker permanently gains +7 pts each time you score a dots meld. Current: 0"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/denker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Chenker
class Chenker(Mahjongker):
    name = "Chenker"
    description = "This mahjongker permanently gains +7 pts each time you score a char meld. Current: 0"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/chenker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Tanavastker
class Tanavastker(Mahjongker):
    name = "Tanavastker"
    description = "Reveal honor meld: Invest +15 pts.\nActivate: Spend $2 to use Called Shot: Honor"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/tanavastker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Recykler
class Recykler(Mahjongker):
    name = "Recykler"
    description = "Self-reveal meld: Draw the most recently discarded honor tile"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/recykler.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fardker
class Fardker(Mahjongker):
    name = "Fardker"
    description = "All winds are worth 10 pts for you. Do not score bonus points for the table wind"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/fardker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fluteker
class Fluteker(Mahjongker):
    name = "Fluteker"
    description = "During scoring, bamboos are also considered dots, and vice versa."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/fluteker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# i-ker
class Iker(Mahjongker):
    name = "iker"
    description = "During scoring, dots are also considered characters, and vice versa."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/iker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# KillTonyker
class KillTonyker(Mahjongker):
    name = "KillTonyker"
    description = "During scoring, characters are also considered bamboo, and vice versa."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/killtonyker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Doldrumker
class Doldrumker(Mahjongker):
    name = "Doldrumker"
    description = "Gain $2 for discarding any wind"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/doldrumker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Discombobuker
class Discombobuker(Mahjongker):
    name = "Discombobuker"
    description = "Randomize your other mahjongkers. You cannot sell this mahjongker.\nPrelude: Re-randomize\nMahjong: Gain +100 pts"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/discombobuker.jpg"

    def eval_score(self, my_mahjongkers):
        return (40, 0)

# Pivotker
class Pivotker(Mahjongker):
    name = "Pivotker"
    description = "Gain +5 pts for every tile you score that is not from your opening hand."
    priority = 1
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/pivotker.jpg"

    def eval_score(self, my_mahjongkers, tile):
        return (0, 0)

# Spanker
class Spanker(Mahjongker):
    name = "Spanker"
    description = "1-5-9 is now a valid sequence meld.  +15 pts for 1-5-9 melds."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/spanker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        bamynker = Bamynker()
        dynker = Dynker()
        chynker = Chynker()
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()
        ranks = []
        score = 15
        for tile in meld.tiles:
            ranks.append(tile.rank)

        if "1" in ranks and "5" in ranks and "9" in ranks:
            if bamynker in my_mahjongkers:
                if (meld.suit == "bamboo" or 
                    meld.suit == "dot" and fluteker in my_mahjongkers or 
                    meld.suit == "character" and killtonyker in my_mahjongkers):
                    score += 15
            if chynker in my_mahjongkers:
                if (meld.suit == "character" or 
                    meld.suit == "dot" and iker in my_mahjongkers or 
                    meld.suit == "bamboo" and killtonyker in my_mahjongkers):
                    score += 15
            if dynker in my_mahjongkers:
                if (meld.suit == "dot" or 
                    meld.suit == "character" and iker in my_mahjongkers or 
                    meld.suit == "bamboo" and fluteker in my_mahjongkers):
                    score += 15
            return (score, 0)
        return (0, 0)

# JackBlackgker
class JackBlackgker(Mahjongker):
    name = "JackBlackgker"
    description = "You have a counter starting at 21.  When you discard a tile, decrease the counter by the rank of the tile (honors are 10). If the counter is at 0, Invest +10 pts. If you go negative, Invest -5 pts. Then reset the counter"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/jackblackgker.jpg"
    point_value = 0

    def eval_score(self, my_mahjongkers):
        return (self.point_value, 0)

# Recruitker
class Recruitker(Mahjongker):
    name = "Recruitker"
    description = "Mahjong: The next mahjongker you buy is discounted by $8."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/recruitker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Squadker
class Squadker(Mahjongker):
    name = "Squadker"
    description = "Activate: Spend $2 and gain one random common mahjongker"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/squadker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Goalker
class Goalker(Mahjongker):
    name = "Goalker"
    description = "Selected: (flush, sequence, set)\nMahjong: If your scored hand is of the selected type, gain +50 pts\nPrelude: Reselect the hand type"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/goalker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Doubker
class Doubker(Mahjongker):
    name = "Doubker"
    description = "The first meld you lock in scores twice."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/doubker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# DoubDoubker
class DoubDoubker(Mahjongker):
    name = "DoubDoubker"
    description = "Mahjong: If you have two of the same meld in your scored hand, gain +50 pts."
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/doubdoubker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        if len(hand.melds) <= 1: return (0, 0)
        if len(hand.melds) == 2:
            if (hand.melds[0] == hand.melds[1]):
                return (50, 0)
            else:
                return (0, 0)
        if len(hand.melds) == 3:
            if hand.melds[0] == hand.melds[1]:
                return (50, 0)
            elif hand.melds[0] == hand.melds[2]:
                return (50, 0)
            elif hand.melds[1] == hand.melds[2]:
                return (50, 0)
            else:
                return (0, 0)
        return (0, 0)

# Jeaucoeur
class Jeaucoeur(Mahjongker):
    name = "Jeaucoeur"
    description = "Chi: Shuffle and redraw up to 3 tiles"
    priority = 3 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/jeaucoeur.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Unbumungker
class Unbumungker(Mahjongker):
    name = "Unbumungker"
    description = "When you discard a Bamboo tile, Store +20 pts."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/unbumungker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Undungker
class Undungker(Mahjongker):
    name = "Undungker"
    description = "When you discard a Dots tile, Store +20 pts."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/undungker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Unchungker
class Unchungker(Mahjongker):
    name = "Unchungker"
    description = "When you discard a Characater tile, Store +20 pts."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/unchungker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Ranker
class Ranker(Mahjongker):
    name = "Ranker"
    description = "Mahjong: Gain +13 pts for each unique rank in your scored hand."
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/ranker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        rankset = {}
        for meld in hand.melds:
            for tile in meld.tiles:
                rankset.add(tile.rank)
        if (len(hand.eyes) != 0):
            for tile in hand.eyes[0]:
                rankset.add(tile.rank)
        return (len(rankset) * 12, 0)

# DoubleDownker
class DoubleDownker(Mahjongker):
    name = "DoubleDownker"
    description = "All pot rewards are doubled for you."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/doubledownker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Diffker
class Diffker(Mahjongker):
    name = "Diffker"
    description = "Prelude: Gain a Re: Suitbaru.\nMahjong: Gain +110 pts if each of your melds in your scored hand is a different suit. (Chracter, Dots, Bamboo, Honor, etc.)"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/diffker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        suitset = {}
        for meld in hand.melds:
            if meld.suit in suitset:
                return (0, 0)
            else:
                suitset.add(meld.suit)
        return (110, 0)

# Numbermanker
class Numbermanker(Mahjongker):
    name = "Numbermanker"
    description = "Selected: (#, #, #)\nMahjong: If your scored hand has ALL 3 ranks, gain +80 pts\nPrelude: Reselect the Ranks"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/numbermanker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Consolaker
class Consolaker(Mahjongker):
    name = "Consolaker"
    description = "Prelude: If you have the least amount of points, destroy this mahjongker and gain +50 pts and +$3"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/consolaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# GumGumker
class GumGumker(Mahjongker):
    name = "GumGumker"
    description = "When you are targeted by another player's effect, copy the effect and target another player."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gumgumker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Conqker
class Conqker(Mahjongker):
    name = "Conqker"
    description = "Mahjong: Gain points equivalent to the total combined rank of your scored hand (honors are 1)"
    priority = 5 
    cost = 6
    sell_value = 2
    img_src = "/jongker/conqker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        rank_total = 0
        for meld in hand.melds:
            for tile in meld.tiles:
                if tile.suit != "wind" and tile.suit != "dragon" and tile.suit != "special":
                    rank_total += int(tile.rank)
                else:
                    rank_total += 1
        return (rank_total, 0)

# Bingoker
class Bingoker(Mahjongker):
    name = "Bingoker"
    description = "This mahjongker is a bingo sheet with 1 through 9.\nReveal meld: For each Rank in the meld, cross off that Rank from this sheet\nMahjong: If all Ranks are crossed off, gain +70 pts and destroy this mahjongker."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bingoker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Bamynker
class Bamynker(Mahjongker):
    name = "Bamynker"
    description = "Bamboo tiles and melds are scored twice."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bamynker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Dynker
class Dynker(Mahjongker):
    name = "Dynker"
    description = "Dots tiles and melds are scored twice."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dynker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Chynker
class Chynker(Mahjongker):
    name = "Chynker"
    description = "Char tiles and melds are scored twice."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/chynker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Hynker
class Hynker(Mahjongker):
    name = "Hynker"
    description = "Honor tiles and melds are scored twice."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/hynker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Worldker
class Worldker(Mahjongker):
    name = "Worldker"
    description = "Selected suit: (bamboo, character, dots).\nMahjong: For each tile of this suit in your scored hand, gain +8 pts.\nPrelude: Reselect the suit."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/worldker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Preciseker
class Preciseker(Mahjongker):
    name = "Preciseker"
    description = "Selected ranks: (#, #, #)\nMahjong: For each tile of these ranks in your scored hand, gain +8 pts.\n Prelude: Reselect the ranks."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/preciseker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Symbioker
class Symbioker(Mahjongker):
    name = "Symbioker"
    description = "Each time you gain money, Store +10 pts"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/symbioker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Warrenker
class Warrenker(Mahjongker):
    name = "Warrenker"
    description = "Prelude: Set your money to 0. Gain +10 points for every $1 lost."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/warrenker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Crescendker
class Crescendker(Mahjongker):
    name = "Crescendker"
    description = "The meld in your final slot is scored three additional times."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/crescendker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# DWker
class DWker(Mahjongker):
    name = "DWker"
    description = "-2 hand size. +50 pts."
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dwker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        if (len(hand.melds) >= 4):
            return (50, 0)
        return (0, 0)

# Fuseker
class Fuseker(Mahjongker):
    name = "Fuseker"
    description = "At the start of the round, destroy this and two other random mahjongkers, and then gain a random rare mahjongker."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/fuseker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# BlackBlackgker
class BlackBlackgker(Mahjongker):
    name = "BlackBlackgker"
    description = "Counter starts at 0. For every tile you discard, the counter increases by the rank (honors 10). Gain $2 when it hits or exceeds 21. Then reset the counter."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/blackblackgkerker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)
    
# Arodker
class Arodker(Mahjongker):
    name = "Arodker"
    description = "Selected ranks: (#, #)\nWhen you discard a tile of these ranks, gain $1.\nPrelude: Reselect ranks."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/arodker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Spaghettiker
class Spaghettiker(Mahjongker):
    name = "Spaghettiker"
    description = "Always score all the individual tiles in your hand at the end of the round."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/spaghettiker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Tricker
class Tricker(Mahjongker):
    name = "Tricker"
    description = "When you lock in a meld slot, for each player that has a meld in that slot with matching suit OR type, steal 15 pts from them."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/tricker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Eggker
class Eggker(Mahjongker):
    name = "Eggker"
    description = "When you reveal a non-valid hand, score it, move those tiles to the discard, gain +1 temporary max hand size, and redraw to your max hand size"
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/eggker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# DEIKongker
class DEIKongker(Mahjongker):
    name = "DEIKongker"
    description = "Quads can contain one tile of a different suit."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/deikongker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# GapKongker
class GapKongker(Mahjongker):
    name = "GapKongker"
    description = "Quads can contain a rank difference 1 (e.g. 1112)"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gapkongker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fourecloseker
class Fourecloseker(Mahjongker):
    name = "Fourecloseker"
    description = "Kong: Steal $3 from that player. Gain $1\nSelf-Reveal quad: Steal $1 from all players. Gain $1"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/fourecloseker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Greedker
class Greedker(Mahjongker):
    name = "Greedker"
    description = "Mahjong: Gain +1 pt for each tile scored. +25 pts instead, for each tile past 12 scored tiles."
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/greedker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        num_tiles = 0
        for meld in hand.melds:
            num_tiles += len(meld.tiles)
        return (12 + (num_tiles - 12) * 20, 0)

# Absorbker
class Absorbker(Mahjongker):
    name = "Absorbker"
    description = "Reveal quad: Steal +10 pts from all other players"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/absorbker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Foursiker
class Foursiker(Mahjongker):
    name = "Foursiker"
    description = "When you draw from the dead wall from creating a quad, you may draw ANY tile from the dead wall"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/foursiker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Donkeyker
class Donkeyker(Mahjongker):
    name = "Donkeyker"
    description = "Mahjong: Gain +30 pts for each quad meld."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/donkeyker.jpg"

    def eval_score(self, my_mahjongkers, meld):
        bamynker = Bamynker()
        dynker = Dynker()
        chynker = Chynker()
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()
        score = 25
        if len(meld) == 4:
            if bamynker in my_mahjongkers:
                if (meld.suit == "bamboo" or 
                    meld.suit == "dot" and fluteker in my_mahjongkers or 
                    meld.suit == "character" and killtonyker in my_mahjongkers):
                    score += 25
            if chynker in my_mahjongkers:
                if (meld.suit == "character" or 
                    meld.suit == "dot" and iker in my_mahjongkers or 
                    meld.suit == "bamboo" and killtonyker in my_mahjongkers):
                    score += 25
            if dynker in my_mahjongkers:
                if (meld.suit == "dot" or 
                    meld.suit == "character" and iker in my_mahjongkers or 
                    meld.suit == "bamboo" and fluteker in my_mahjongkers):
                    score += 25
            return (score, 0)
        return (0, 0)

# OneFourAllker
class OneFourAllker(Mahjongker):
    name = "OneFourAllker"
    description = "A tile of Rank 4 can be used to complete any quad"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/onefourallker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fourtnightker
class Fourtnightker(Mahjongker):
    name = "Fourtnightker"
    description = "Reveal quad: Gain $7"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/fourtnightker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# HighNoonker
class HighNoonker(Mahjongker):
    name = "HighNoonker"
    description = "Reveal quad: Called Shot on each other player"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/highnoonker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Stevenker
class Stevenker(Mahjongker):
    name = "Stevenker"
    description = "You can Self-Reveal a quad of of any combination of even tiles of the same suit (e.g. 2268)"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/stevenker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# BigkerTheCat
class BigkerTheCat(Mahjongker):
    name = "BigkerTheCat"
    description = "You can Self-Reveal a quad of any combination of tiles > rank 5 of the same suit (e.g. 7799)"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bigkerthecat.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# WageGapker
class WageGapker(Mahjongker):
    name = "WageGapker"
    description = "Mahjong: Gain $(total combined rank of your scored hand  / 10) (honors are worth 10)"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/wagegapker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        rank_total = 0
        for meld in hand.melds:
            for tile in meld.tiles:
                if tile.suit != "wind" and tile.suit != "dragon" and tile.suit != "special":
                    rank_total += int(tile.rank)
                else:
                    rank_total += 1
        return (0, math.floor(rank_total / 10))

# Assassinker
class Assassinker(Mahjongker):
    name = "Assassinker"
    description = "Activate: If you have no Commited melds, Exile a tile. Draw 1 tile from the living wall"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/assassinker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Phoenixker
class Phoenixker(Mahjongker):
    name = "Phoenixker"
    description = "Reveal meld: You may take a tile from the discard or Hell and make it a quad if possible"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/phoenixker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# TheHundredker
class TheHundredker(Mahjongker):
    name = "TheHundredker"
    description = "Mahjong: If the total rank of your scored hand (honors are worth 10) is at least 100, gain +110 pts. "
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/thehundredker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        rank_total = 0
        for meld in hand.melds:
            for tile in meld.tiles:
                if tile.suit != "wind" and tile.suit != "dragon" and tile.suit != "special":
                    rank_total += int(tile.rank)
                else:
                    rank_total += 1
        if (rank_total >= 100):
            return (110, 0)
        else:
            return (0, 0)
        
# Obelisker
class Obelisker(Mahjongker):
    name = "Obelisker"
    description = "Whenever you use a different action from your last (Pong, Chi, Kong, Self-Reveal), Store +15 pts."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/obelisker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Reservaker
class Reservaker(Mahjongker):
    name = "Reservaker"
    description = "You may set aside one jongker in the shop.  Only you may purchase it, and when you do, destroy this jongker."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/reservaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Uniqler
class Uniqler(Mahjongker):
    name = "Uniqler"
    description = "Gain +10 pts for every unique tile in your scored hand."
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/uniqler.jpg"

    def eval_score(self, my_mahjongkers, hand):
        unique_tiles = []
        for meld in hand.melds:
            for tile in meld.tiles:
                if tile not in unique_tiles:
                    unique_tiles.append(tile)
        return (len(unique_tiles) * 10, 0)

# Loanker
class Loanker(Mahjongker):
    name = "Loanker"
    description = "Gain $10. You cannot sell this mahjongker. You gain $1 less every time you gain money."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/loanker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# MusicalChairker
class MusicalChairker(Mahjongker):
    name = "MusicalChairker"
    description = "Reveal wind meld: If this meld is another player's seat wind, Steal $3 from them."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/musicalchairker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Worshipker
class Worshipker(Mahjongker):
    name = "Worshipker"
    description = "Honor tiles are worth 5 pts. In your scored hand, for each honor meld, score your other melds again."
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/worshipker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        # rank_total = 0
        # for meld in hand.melds:
        #     for tile in meld.tiles:
        #         if tile.suit != "wind" and tile.suit != "dragon" and tile.suit != "special":
        #             rank_total += int(tile.rank)
        #         else:
        #             rank_total += 1
        # if (rank_total >= 100):
        #     return (100, 0)
        # else:
        return (0, 0)           

# Thermomeker
class Thermomeker(Mahjongker):
    name = "Thermomeker"
    description = "If you Fevered at least 3 melds before you Mahjong, gain +50 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/thermomeker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Suitker
class Suitker(Mahjongker):
    name = "Suitker"
    description = "Mahjong: If all your melds in your scored hand are the same suit, gain +100 pts"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/suitker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        if hand.is_flush:
            return (100, 0)
        return (0, 0)

# Mimicgker
class Mimicgker(Mahjongker):
    name = "Mimicgker"
    description = "Prelude: choose a player. When you or that player use an item, you may use a copy"
    priority = 6 
    cost = 6
    sell_value = 2
    img_src = "/jongker/mimicgker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Reuseker
class Reuseker(Mahjongker):
    name = "Reuseker"
    description = "Reveal meld: Replace a tile with one of the meld's tiles"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/reuseker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Reduceker
class Reduceker(Mahjongker):
    name = "Reduceker"
    description = "When you create a fever meld, you may keep one of the meld's tiles."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/reduceker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Invertker
class Invertker(Mahjongker):
    name = "Invertker"
    description = "Fever meld: score and Store the point value of the meld"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/invertker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Purgeker
class Purgeker(Mahjongker):
    name = "Purgeker"
    description = "Selected suit: (Bamboo, Character, Dots, Honor)\nMahjong: If you do not have any of this suit in your scored hand and current hand, gain +100 pts.\nPrelude: Reselect the suit"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/purgeker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Cookgker
class Cookgker(Mahjongker):
    name = "Cookgker"
    description = "Any player can Chi tiles that you discard regardless of your position.  If they do, gain +20 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/cookgker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Speedker
class Speedker(Mahjongker):
    name = "Speedker"
    description = "You may mahjong with 1 less meld."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/speedker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# IHWSHker
class IHWSHker(Mahjongker):
    name = "IHWSHker"
    description = "Mahjong: If your scored hand has the same suit or type as the last scored hand of the player on your right, gain +100 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/IHWSHker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Eggker
class Eggker(Mahjongker):
    name = "Eggker"
    description = "Reveal meld: Gain $1"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/eggker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Donaldker
class Donaldker(Mahjongker):
    name = "Donaldker"
    description = "-2 hand size.\nOn your draw phase, instead draw 2 and shuffle 1"
    priority = 6 
    cost = 4
    sell_value = 1
    img_src = "/jongker/donaldker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Grabker
class Grabker(Mahjongker):
    name = "Grabker"
    description = "Hand size +1"
    priority = 6 
    cost = 5
    sell_value = 2
    img_src = "/jongker/grabker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fevker
class Fevker(Mahjongker):
    name = "Fevker"
    description = "Fever meld: Invest +15 pts\n Commit meld: Invest -5 pts"
    priority = 6 
    cost = 5
    sell_value = 2
    img_src = "/jongker/fevker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)    

# Everstormker
class Everstormker(Mahjongker):
    name = "Everstormker"
    description = "Reveal wind meld: Add 1 of each wind tile to the deck. Invest +10 pts"
    priority = 6 
    cost = 5
    sell_value = 2
    img_src = "/jongker/everstormker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)    

# --------------------------------------------------------------------------------------
# MAHJONGKER LIST
# --------------------------------------------------------------------------------------
all_mahjongkers_list = []
all_mahjongkers_list.append(Bamonker())
all_mahjongkers_list.append(Donker())
all_mahjongkers_list.append(Chonker())
# all_mahjongkers_list.append(Dragonker())
# all_mahjongkers_list.append(Wonker())
# all_mahjongkers_list.append(Sequencker())
# all_mahjongkers_list.append(MahMahMahjonker())
# all_mahjongkers_list.append(Milwaunker())
# all_mahjongkers_list.append(Kohlker())
# all_mahjongkers_list.append(Windker())
# all_mahjongkers_list.append(Draker())
all_mahjongkers_list.append(Evenker())
all_mahjongkers_list.append(Oddker())
all_mahjongkers_list.append(AYCker())
all_mahjongkers_list.append(Pingker())
all_mahjongkers_list.append(KingKongker())
all_mahjongkers_list.append(Gapker())
# all_mahjongkers_list.append(DEIker())
# all_mahjongkers_list.append(SEIquenker())
all_mahjongkers_list.append(Siker())
all_mahjongkers_list.append(Bourdainker())
all_mahjongkers_list.append(Dollker())
all_mahjongkers_list.append(Yenker())
all_mahjongkers_list.append(Falchionker())
# all_mahjongkers_list.append(Neenjaker())
all_mahjongkers_list.append(Gayker())
all_mahjongkers_list.append(Bumungker())
all_mahjongkers_list.append(Dungker())
all_mahjongkers_list.append(Chungker())
all_mahjongkers_list.append(Hungker())
# all_mahjongkers_list.append(Bimingker())
# all_mahjongkers_list.append(Dingker())
# all_mahjongkers_list.append(Chingker())
all_mahjongkers_list.append(Hoardker())
# all_mahjongkers_list.append(Meldker())
# all_mahjongkers_list.append(Snakeker())
# all_mahjongkers_list.append(Seeker())
# all_mahjongkers_list.append(LeeSinker())
# all_mahjongkers_list.append(SeeingDoubker())
# all_mahjongkers_list.append(Seequenker())
all_mahjongkers_list.append(Highker())
all_mahjongkers_list.append(Lowker())
all_mahjongkers_list.append(Rainbowker())
all_mahjongkers_list.append(Raindraker())
all_mahjongkers_list.append(Magellker())
all_mahjongkers_list.append(Salarymanker())
all_mahjongkers_list.append(MealTicker())
all_mahjongkers_list.append(WenGeker())
all_mahjongkers_list.append(Fourker())
all_mahjongkers_list.append(DOWker())
all_mahjongkers_list.append(Comebacker())
all_mahjongkers_list.append(Underdoker())
all_mahjongkers_list.append(Compensaker())
all_mahjongkers_list.append(Gronkowsker())
all_mahjongkers_list.append(Dumpsker())
all_mahjongkers_list.append(Copycatker())
# all_mahjongkers_list.append(Boomerangker())
all_mahjongkers_list.append(Doraker())
all_mahjongkers_list.append(AllforOneker())
all_mahjongkers_list.append(OneforAllker())
all_mahjongkers_list.append(Pickgker())
all_mahjongkers_list.append(Straightker())
all_mahjongkers_list.append(Arthker())
# all_mahjongkers_list.append(DuckDuckGooseker())
all_mahjongkers_list.append(DebtCollectker())
# all_mahjongkers_list.append(Quaker())
all_mahjongkers_list.append(Anthonyker())
# all_mahjongkers_list.append(Picker())
all_mahjongkers_list.append(Luckgker())
all_mahjongkers_list.append(Buffettker())
all_mahjongkers_list.append(Fuckgker())
all_mahjongkers_list.append(Toker())
# all_mahjongkers_list.append(Emeraldker())
all_mahjongkers_list.append(Snipker())
all_mahjongkers_list.append(Grenadeker())
all_mahjongkers_list.append(Stepsisker())
all_mahjongkers_list.append(LarryEllisker())
all_mahjongkers_list.append(Suckgker())
# all_mahjongkers_list.append(Oracker())
# all_mahjongkers_list.append(Riggedker())
all_mahjongkers_list.append(JosephJoesker())
all_mahjongkers_list.append(Fibonaccker())
all_mahjongkers_list.append(Wokegker())
all_mahjongkers_list.append(Shardker())
all_mahjongkers_list.append(Ponorker())
all_mahjongkers_list.append(Sonorker())
# all_mahjongkers_list.append(Speedker())
all_mahjongkers_list.append(Blackjackgker())
# all_mahjongkers_list.append(Chairker())
all_mahjongkers_list.append(AngelInvesker())
# all_mahjongkers_list.append(Triker())
# all_mahjongkers_list.append(Emporerker())
# all_mahjongkers_list.append(Empressker())
# all_mahjongkers_list.append(Laobanker())
all_mahjongkers_list.append(Huntker())
# all_mahjongkers_list.append(Gourmetker())
# all_mahjongkers_list.append(Specialker())
# all_mahjongkers_list.append(Spoilker())
# all_mahjongkers_list.append(Harbingker())
all_mahjongkers_list.append(GoGoGaker())
# all_mahjongkers_list.append(DejaVuker())
# all_mahjongkers_list.append(Coilker())
# all_mahjongkers_list.append(Donnerker())
all_mahjongkers_list.append(Trashker())
# all_mahjongkers_list.append(Trapker())
all_mahjongkers_list.append(Sprayker())
# all_mahjongkers_list.append(Vanillaker())
# all_mahjongkers_list.append(NoReservaker())
# all_mahjongkers_list.append(Bamanker())
# all_mahjongkers_list.append(Danker())
# all_mahjongkers_list.append(Chanker())
all_mahjongkers_list.append(Miniker())
all_mahjongkers_list.append(Honker())
all_mahjongkers_list.append(Eatker())
all_mahjongkers_list.append(Sameker())
all_mahjongkers_list.append(Odiumker())
# all_mahjongkers_list.append(Bamenker())
# all_mahjongkers_list.append(Denker())
# all_mahjongkers_list.append(Chenker())
all_mahjongkers_list.append(Tanavastker())
all_mahjongkers_list.append(Recykler())
all_mahjongkers_list.append(Fardker())
# all_mahjongkers_list.append(Fluteker())
# all_mahjongkers_list.append(Iker())
# all_mahjongkers_list.append(KillTonyker())
all_mahjongkers_list.append(Doldrumker())
all_mahjongkers_list.append(Discombobuker())
# all_mahjongkers_list.append(Pivotker())
# all_mahjongkers_list.append(Spanker())
all_mahjongkers_list.append(JackBlackgker())
all_mahjongkers_list.append(Recruitker())
all_mahjongkers_list.append(Squadker())
all_mahjongkers_list.append(Goalker())
# all_mahjongkers_list.append(Doubker())
all_mahjongkers_list.append(DoubDoubker())
all_mahjongkers_list.append(Jeaucoeur())
all_mahjongkers_list.append(Unbumungker())
all_mahjongkers_list.append(Undungker())
all_mahjongkers_list.append(Unchungker())
all_mahjongkers_list.append(Ranker())
# all_mahjongkers_list.append(DoubleDownker())
all_mahjongkers_list.append(Diffker())
all_mahjongkers_list.append(Numbermanker())
all_mahjongkers_list.append(Consolaker())
all_mahjongkers_list.append(GumGumker())
all_mahjongkers_list.append(Conqker())
all_mahjongkers_list.append(Bingoker())
# all_mahjongkers_list.append(Bamynker())
# all_mahjongkers_list.append(Dynker())
# all_mahjongkers_list.append(Chynker())
# all_mahjongkers_list.append(Hynker())
all_mahjongkers_list.append(Worldker())
all_mahjongkers_list.append(Preciseker())
all_mahjongkers_list.append(Symbioker())
all_mahjongkers_list.append(Warrenker())
# all_mahjongkers_list.append(Crescendker())
# all_mahjongkers_list.append(DWker())
# all_mahjongkers_list.append(Fuseker())
all_mahjongkers_list.append(BlackBlackgker())
all_mahjongkers_list.append(Arodker())
# all_mahjongkers_list.append(Spaghettiker())
all_mahjongkers_list.append(Tricker())
# all_mahjongkers_list.append(Eggker())
all_mahjongkers_list.append(DEIKongker())
all_mahjongkers_list.append(GapKongker())
all_mahjongkers_list.append(Fourecloseker())
all_mahjongkers_list.append(Greedker())
all_mahjongkers_list.append(Absorbker())
# all_mahjongkers_list.append(Foursiker())
all_mahjongkers_list.append(Donkeyker())
all_mahjongkers_list.append(OneFourAllker())
all_mahjongkers_list.append(Fourtnightker())
all_mahjongkers_list.append(HighNoonker())
all_mahjongkers_list.append(Stevenker())
all_mahjongkers_list.append(BigkerTheCat())
all_mahjongkers_list.append(WageGapker())
all_mahjongkers_list.append(Assassinker())
all_mahjongkers_list.append(Phoenixker())
all_mahjongkers_list.append(TheHundredker())
all_mahjongkers_list.append(Obelisker())
# all_mahjongkers_list.append(Reservaker())
# all_mahjongkers_list.append(Uniqler())
all_mahjongkers_list.append(Loanker())
all_mahjongkers_list.append(MusicalChairker())
# all_mahjongkers_list.append(Worshipker())
all_mahjongkers_list.append(Thermomeker())
all_mahjongkers_list.append(Suitker())
all_mahjongkers_list.append(Reuseker())
# all_mahjongkers_list.append(Reduceker())
all_mahjongkers_list.append(Invertker())
all_mahjongkers_list.append(Purgeker())
all_mahjongkers_list.append(Cookgker())
all_mahjongkers_list.append(Speedker())
all_mahjongkers_list.append(IHWSHker())
all_mahjongkers_list.append(Eggker())
all_mahjongkers_list.append(Donaldker())
all_mahjongkers_list.append(Grabker())
all_mahjongkers_list.append(Fevker())
all_mahjongkers_list.append(Everstormker())

# --------------------------------------------------------------------------------------
# MAHJONGKER DICT
# --------------------------------------------------------------------------------------
all_mahjongkers_dict = {}
all_mahjongkers_dict["bamonker"] = Bamonker()
all_mahjongkers_dict["donker"] = Donker()
all_mahjongkers_dict["chonker"] = Chonker()
all_mahjongkers_dict["dragonker"] = Dragonker()
all_mahjongkers_dict["wonker"] = Wonker()
all_mahjongkers_dict["sequencker"] = Sequencker()
all_mahjongkers_dict["mahmahmahjonker"] = MahMahMahjonker()
all_mahjongkers_dict["milwaunker"] = Milwaunker()
all_mahjongkers_dict["kohlker"] = Kohlker()
all_mahjongkers_dict["windker"] = Windker()
all_mahjongkers_dict["draker"] = Draker()
all_mahjongkers_dict["evenker"] = Evenker()
all_mahjongkers_dict["oddker"] = Oddker()
all_mahjongkers_dict["aycker"] = AYCker()
all_mahjongkers_dict["pingker"] = Pingker()
all_mahjongkers_dict["kingkongker"] = KingKongker()
all_mahjongkers_dict["gapker"] = Gapker()
all_mahjongkers_dict["deiker"] = DEIker()
all_mahjongkers_dict["seiquenker"] = SEIquenker()
all_mahjongkers_dict["siker"] = Siker()
all_mahjongkers_dict["bourdainker"] = Bourdainker()
all_mahjongkers_dict["dollker"] = Dollker()
all_mahjongkers_dict["yenker"] = Yenker()
all_mahjongkers_dict["falchionker"] = Falchionker()
all_mahjongkers_dict["neenjaker"] = Neenjaker()
all_mahjongkers_dict["gayker"] = Gayker()
all_mahjongkers_dict["bumungker"] = Bumungker()
all_mahjongkers_dict["dungker"] = Dungker()
all_mahjongkers_dict["chungker"] = Chungker()
all_mahjongkers_dict["hungker"] = Hungker()
all_mahjongkers_dict["bimingker"] = Bimingker()
all_mahjongkers_dict["dingker"] = Dingker()
all_mahjongkers_dict["chingker"] = Chingker()
all_mahjongkers_dict["hoardker"] = Hoardker()
all_mahjongkers_dict["meldker"] = Meldker()
all_mahjongkers_dict["snakeker"] = Snakeker()
all_mahjongkers_dict["seeker"] = Seeker()
all_mahjongkers_dict["leesinker"] = LeeSinker()
all_mahjongkers_dict["seeingdoubker"] = SeeingDoubker()
all_mahjongkers_dict["seequenker"] = Seequenker()
all_mahjongkers_dict["highker"] = Highker()
all_mahjongkers_dict["lowker"] = Lowker()
all_mahjongkers_dict["rainbowker"] = Rainbowker()
all_mahjongkers_dict["raindraker"] = Raindraker()
all_mahjongkers_dict["magellker"] = Magellker()
all_mahjongkers_dict["salarymanker"] = Salarymanker()
all_mahjongkers_dict["mealticker"] = MealTicker()
all_mahjongkers_dict["wengeker"] = WenGeker()
all_mahjongkers_dict["fourker"] = Fourker()
all_mahjongkers_dict["dowker"] = DOWker()
all_mahjongkers_dict["comebacker"] = Comebacker()
all_mahjongkers_dict["underdoker"] = Underdoker()
all_mahjongkers_dict["compensaker"] = Compensaker()
all_mahjongkers_dict["gronkowsker"] = Gronkowsker()
all_mahjongkers_dict["dumpsker"] = Dumpsker()
all_mahjongkers_dict["copycatker"] = Copycatker()
all_mahjongkers_dict["boomerangker"] = Boomerangker()
all_mahjongkers_dict["doraker"] = Doraker()
all_mahjongkers_dict["allforoneker"] = AllforOneker()
all_mahjongkers_dict["oneforallker"] = OneforAllker()
all_mahjongkers_dict["pickgker"] = Pickgker()
all_mahjongkers_dict["straightker"] = Straightker()
all_mahjongkers_dict["arthker"] = Arthker()
all_mahjongkers_dict["duckduckgooseker"] = DuckDuckGooseker()
all_mahjongkers_dict["debtcollectker"] = DebtCollectker()
all_mahjongkers_dict["quaker"] = Quaker()
all_mahjongkers_dict["anthonyker"] = Anthonyker()
all_mahjongkers_dict["picker"] = Picker()
all_mahjongkers_dict["luckgker"] = Luckgker()
all_mahjongkers_dict["buffettker"] = Buffettker()
all_mahjongkers_dict["fuckgker"] = Fuckgker()
all_mahjongkers_dict["toker"] = Toker()
all_mahjongkers_dict["emeraldker"] = Emeraldker()
all_mahjongkers_dict["snipker"] = Snipker()
all_mahjongkers_dict["grenadeker"] = Grenadeker()
all_mahjongkers_dict["stepsisker"] = Stepsisker()
all_mahjongkers_dict["larryellisker"] = LarryEllisker()
all_mahjongkers_dict["suckgker"] = Suckgker()
all_mahjongkers_dict["riggedker"] = Riggedker()
all_mahjongkers_dict["josephjoesker"] = JosephJoesker()
all_mahjongkers_dict["fibonaccker"] = Fibonaccker()
all_mahjongkers_dict["wokegker"] = Wokegker()
all_mahjongkers_dict["shardker"] = Shardker()
all_mahjongkers_dict["ponorker"] = Ponorker()
all_mahjongkers_dict["sonorker"] = Sonorker()
all_mahjongkers_dict["speedker"] = Speedker()
all_mahjongkers_dict["blackjackgker"] = Blackjackgker()
all_mahjongkers_dict["chairker"] = Chairker()
all_mahjongkers_dict["angelinvesker"] = AngelInvesker()
all_mahjongkers_dict["triker"] = Triker()
all_mahjongkers_dict["emporerker"] = Emporerker()
all_mahjongkers_dict["empressker"] = Empressker()
all_mahjongkers_dict["laobanker"] = Laobanker()
all_mahjongkers_dict["huntker"] = Huntker()
all_mahjongkers_dict["gourmetker"] = Gourmetker()
all_mahjongkers_dict["specialker"] = Specialker()
all_mahjongkers_dict["spoilker"] = Spoilker()
all_mahjongkers_dict["harbingker"] = Harbingker()
all_mahjongkers_dict["gogogaker"] = GoGoGaker()
all_mahjongkers_dict["dejavuker"] = DejaVuker()
all_mahjongkers_dict["coilker"] = Coilker()
all_mahjongkers_dict["donnerker"] = Donnerker()
all_mahjongkers_dict["trashker"] = Trashker()
all_mahjongkers_dict["trapker"] = Trapker()
all_mahjongkers_dict["sprayker"] = Sprayker()
all_mahjongkers_dict["vanillaker"] = Vanillaker()
all_mahjongkers_dict["noreservaker"] = NoReservaker()
all_mahjongkers_dict["bamanker"] = Bamanker()
all_mahjongkers_dict["danker"] = Danker()
all_mahjongkers_dict["chanker"] = Chanker()
all_mahjongkers_dict["miniker"] = Miniker()
all_mahjongkers_dict["honker"] = Honker()
all_mahjongkers_dict["eatker"] = Eatker()
all_mahjongkers_dict["sameker"] = Sameker()
all_mahjongkers_dict["odiumker"] = Odiumker()
all_mahjongkers_dict["bamenker"] = Bamenker()
all_mahjongkers_dict["denker"] = Denker()
all_mahjongkers_dict["chenker"] = Chenker()
all_mahjongkers_dict["tanavastker"] = Tanavastker()
all_mahjongkers_dict["recykler"] = Recykler()
all_mahjongkers_dict["fardker"] = Fardker()
all_mahjongkers_dict["fluteker"] = Fluteker()
all_mahjongkers_dict["iker"] = Iker()
all_mahjongkers_dict["killtonyker"] = KillTonyker()
all_mahjongkers_dict["doldrumker"] = Doldrumker()
all_mahjongkers_dict["discombobuker"] = Discombobuker()
all_mahjongkers_dict["pivotker"] = Pivotker()
all_mahjongkers_dict["spanker"] = Spanker()
all_mahjongkers_dict["jackblackgker"] = JackBlackgker()
all_mahjongkers_dict["recruitker"] = Recruitker()
all_mahjongkers_dict["squadker"] = Squadker()
all_mahjongkers_dict["goalker"] = Goalker()
all_mahjongkers_dict["doubker"] = Doubker()
all_mahjongkers_dict["doubdoubker"] = DoubDoubker()
all_mahjongkers_dict["jeaucoeur"] = Jeaucoeur()
all_mahjongkers_dict["unbumungker"] = Unbumungker()
all_mahjongkers_dict["undungker"] = Undungker()
all_mahjongkers_dict["unchungker"] = Unchungker()
all_mahjongkers_dict["ranker"] = Ranker()
all_mahjongkers_dict["doubledownker"] = DoubleDownker()
all_mahjongkers_dict["diffker"] = Diffker()
all_mahjongkers_dict["numbermanker"] = Numbermanker()
all_mahjongkers_dict["consolaker"] = Consolaker()
all_mahjongkers_dict["gumgumker"] = GumGumker()
all_mahjongkers_dict["conqker"] = Conqker()
all_mahjongkers_dict["bingoker"] = Bingoker()
all_mahjongkers_dict["bamynker"] = Bamynker()
all_mahjongkers_dict["dynker"] = Dynker()
all_mahjongkers_dict["chynker"] = Chynker()
all_mahjongkers_dict["hynker"] = Hynker()
all_mahjongkers_dict["worldker"] = Worldker()
all_mahjongkers_dict["preciseker"] = Preciseker()
all_mahjongkers_dict["symbioker"] = Symbioker()
all_mahjongkers_dict["warrenker"] = Warrenker()
all_mahjongkers_dict["crescendker"] = Crescendker()
all_mahjongkers_dict["dwker"] = DWker()
all_mahjongkers_dict["fuseker"] = Fuseker()
all_mahjongkers_dict["blackblackgker"] = BlackBlackgker()
all_mahjongkers_dict["arodker"] = Arodker()
all_mahjongkers_dict["spaghettiker"] = Spaghettiker()
all_mahjongkers_dict["tricker"] = Tricker()
all_mahjongkers_dict["eggker"] = Eggker()
all_mahjongkers_dict["deikongker"] = DEIKongker()
all_mahjongkers_dict["gapkongker"] = GapKongker()
all_mahjongkers_dict["fourecloseker"] = Fourecloseker()
all_mahjongkers_dict["greedker"] = Greedker()
all_mahjongkers_dict["absorbker"] = Absorbker()
all_mahjongkers_dict["foursiker"] = Foursiker()
all_mahjongkers_dict["donkeyker"] = Donkeyker()
all_mahjongkers_dict["onefourallker"] = OneFourAllker()
all_mahjongkers_dict["fourtnightker"] = Fourtnightker()
all_mahjongkers_dict["highnoonker"] = HighNoonker()
all_mahjongkers_dict["stevenker"] = Stevenker()
all_mahjongkers_dict["bigkerthecat"] = BigkerTheCat()
all_mahjongkers_dict["wagegapker"] = WageGapker()
all_mahjongkers_dict["assassinker"] = Assassinker()
all_mahjongkers_dict["phoenixker"] = Phoenixker()
all_mahjongkers_dict["thehundredker"] = TheHundredker()
all_mahjongkers_dict["obelisker"] = Obelisker()
all_mahjongkers_dict["reservaker"] = Reservaker()
all_mahjongkers_dict["uniqler"] = Uniqler()
all_mahjongkers_dict["loanker"] = Loanker()
all_mahjongkers_dict["musicalchairker"] = MusicalChairker()
all_mahjongkers_dict["worshipker"] = Worshipker()
all_mahjongkers_dict["thermomeker"] = Thermomeker()
all_mahjongkers_dict["suitker"] = Suitker()
all_mahjongkers_dict["reuseker"] = Reuseker()
all_mahjongkers_dict["reduceker"] = Reduceker()
all_mahjongkers_dict["invertker"] = Invertker()
all_mahjongkers_dict["purgeker"] = Purgeker()
all_mahjongkers_dict["cookgker"] = Cookgker()
all_mahjongkers_dict["speedker"] = Speedker()
all_mahjongkers_dict["IHWSHker"] = IHWSHker()
all_mahjongkers_dict["eggker"] = Eggker()
all_mahjongkers_dict["donaldker"] = Donaldker()
all_mahjongkers_dict["grabker"] = Grabker()
all_mahjongkers_dict["fevker"] = Fevker()
all_mahjongkers_dict["everstormker"] = Everstormker()


# ----------------------------------------------

# --------------------------------------------------------------------------------------
# COMMON MAHJONGKER LIST
# --------------------------------------------------------------------------------------
common_mahjongkers_list = []
for mahjongker in all_mahjongkers_list:
    if mahjongker.cost == COMMON_MAHJONGKER_COST or mahjongker.cost == 4 or mahjongker.cost == 5:
        common_mahjongkers_list.append(mahjongker)

# --------------------------------------------------------------------------------------
# UNCOMMON MAHJONGKER LIST
# --------------------------------------------------------------------------------------
uncommon_mahjongkers_list = []
for mahjongker in all_mahjongkers_list:
    if mahjongker.cost == UNCOMMON_MAHJONGKER_COST or mahjongker.cost == 6:
        uncommon_mahjongkers_list.append(mahjongker)

# --------------------------------------------------------------------------------------
# RARE MAHJONGKER LIST
# --------------------------------------------------------------------------------------
rare_mahjongkers_list = []
for mahjongker in all_mahjongkers_list:
    if mahjongker.cost == RARE_MAHJONGKER_COST or mahjongker.cost == 10:
        rare_mahjongkers_list.append(mahjongker)

# --------------------------------------------------------------------------------------
# INITIAL MAHJONGKER LIST
# --------------------------------------------------------------------------------------
initial_mahjongkers_list = []
initial_mahjongkers_list.append(Bamonker())
initial_mahjongkers_list.append(Donker())
initial_mahjongkers_list.append(Chonker())
initial_mahjongkers_list.append(Evenker())
initial_mahjongkers_list.append(Oddker())
initial_mahjongkers_list.append(Dollker())
initial_mahjongkers_list.append(Yenker())
initial_mahjongkers_list.append(Falchionker())
initial_mahjongkers_list.append(Salarymanker())
initial_mahjongkers_list.append(MealTicker())
initial_mahjongkers_list.append(WenGeker())
initial_mahjongkers_list.append(Fourker())
initial_mahjongkers_list.append(Doraker())
initial_mahjongkers_list.append(Straightker())
initial_mahjongkers_list.append(Arthker())
initial_mahjongkers_list.append(DebtCollectker())
initial_mahjongkers_list.append(Fibonaccker())
initial_mahjongkers_list.append(AYCker())
initial_mahjongkers_list.append(Pingker())
initial_mahjongkers_list.append(Fuckgker())
initial_mahjongkers_list.append(Wokegker())
initial_mahjongkers_list.append(Shardker())
initial_mahjongkers_list.append(Ponorker())
initial_mahjongkers_list.append(Sonorker())
initial_mahjongkers_list.append(Blackjackgker())
initial_mahjongkers_list.append(Huntker())
initial_mahjongkers_list.append(Miniker())
initial_mahjongkers_list.append(Honker())
initial_mahjongkers_list.append(Eatker())
initial_mahjongkers_list.append(Sameker())
initial_mahjongkers_list.append(Odiumker())
initial_mahjongkers_list.append(Recykler())
initial_mahjongkers_list.append(Tanavastker())
initial_mahjongkers_list.append(Pivotker())
initial_mahjongkers_list.append(JackBlackgker())
initial_mahjongkers_list.append(Recruitker())
initial_mahjongkers_list.append(Goalker())
initial_mahjongkers_list.append(DoubDoubker())
initial_mahjongkers_list.append(Jeaucoeur())
initial_mahjongkers_list.append(BlackBlackgker())
initial_mahjongkers_list.append(Arodker())
initial_mahjongkers_list.append(DEIKongker())
initial_mahjongkers_list.append(GapKongker())
initial_mahjongkers_list.append(WageGapker())
initial_mahjongkers_list.append(Phoenixker())
initial_mahjongkers_list.append(Obelisker())
initial_mahjongkers_list.append(MusicalChairker())
initial_mahjongkers_list.append(Thermomeker())
initial_mahjongkers_list.append(Eggker())
initial_mahjongkers_list.append(Fevker())
initial_mahjongkers_list.append(Everstormker())
