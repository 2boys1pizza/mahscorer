from tiles import *

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
    description = "+15 pts for each bamboo meld."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bamonker.jpg"

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

# Donker
class Donker(Mahjongker):
    name = "Donker"
    description = "+15 pts for each dot meld."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/donker.jpg"

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

# Chonker
class Chonker(Mahjongker):
    name = "Chonker"
    description = "+15 pts for each character meld."
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/chonker.jpg"

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

# Dragonker
class Dragonker(Mahjongker):
    name = "Dragonker"
    description = "+20 pts for each dragon meld."
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
    description = "+30 pts for each wind meld."
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
    description = "+5 pts for each even tile"
    priority = 1 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/evenker.jpg"

    def eval_score(self, my_mahjongkers, tile):
        bamynker = Bamynker()
        dynker = Dynker()
        chynker = Chynker()
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()
        score = 5
        if tile.suit == "bamboo" or tile.suit == "dot" or tile.suit == "character":
            if int(tile.rank) % 2 == 0:
                if bamynker in my_mahjongkers:
                    if (tile.suit == "bamboo" or 
                        tile.suit == "dot" and fluteker in my_mahjongkers or 
                        tile.suit == "character" and killtonyker in my_mahjongkers):
                        score += 5
                if chynker in my_mahjongkers:
                    if (tile.suit == "character" or 
                        tile.suit == "dot" and iker in my_mahjongkers or 
                        tile.suit == "bamboo" and killtonyker in my_mahjongkers):
                        score += 5
                if dynker in my_mahjongkers:
                    if (tile.suit == "dot" or 
                        tile.suit == "character" and iker in my_mahjongkers or 
                        tile.suit == "bamboo" and fluteker in my_mahjongkers):
                        score += 5
                return (score, 0)
            else:
                return (0, 0)
        else:
            return (0, 0)

# Oddker
class Oddker(Mahjongker):
    name = "Oddker"
    description = "+5 pts for each odd tile"
    priority = 1 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/oddker.jpg"

    def eval_score(self, my_mahjongkers, tile):
        bamynker = Bamynker()
        dynker = Dynker()
        chynker = Chynker()
        fluteker = Fluteker()
        killtonyker = KillTonyker()
        iker = Iker()
        score = 5
        if tile.suit == "bamboo" or tile.suit == "dot" or tile.suit == "character":
            if int(tile.rank) % 2 == 1:
                if bamynker in my_mahjongkers:
                    if (tile.suit == "bamboo" or 
                        tile.suit == "dot" and fluteker in my_mahjongkers or 
                        tile.suit == "character" and killtonyker in my_mahjongkers):
                        score += 5
                if chynker in my_mahjongkers:
                    if (tile.suit == "character" or 
                        tile.suit == "dot" and iker in my_mahjongkers or 
                        tile.suit == "bamboo" and killtonyker in my_mahjongkers):
                        score += 5
                if dynker in my_mahjongkers:
                    if (tile.suit == "dot" or 
                        tile.suit == "character" and iker in my_mahjongkers or 
                        tile.suit == "bamboo" and fluteker in my_mahjongkers):
                        score += 5
                return (score, 0)
            else:
                return (0, 0)
        else:
            return (0, 0)

# AYCker
class AYCker(Mahjongker):
    name = "AYCker"
    description = "This Mahjongker gains +7 pts on chi (stacking) Current: 0"
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
    description = "This Mahjongker gains +7 pts on pong (stacking) Current: 0"
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
    description = "This Mahjongker gains +20 pts on kong (stacking) Current: 0"
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
    description = "Sequences may contain one gap of 1 (1-2-4 valid, 2-4-6 not valid)"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gapker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# DEIker
class DEIker(Mahjongker):
    name = "DEIker"
    description = "Gain +30 pts for each unique suit in your scored tiles (character, dots, bamboo, honor)."
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
    description = "You may form a kong with a sequence (chi only, 3456)"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/siker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Bourdainker
class Bourdainker(Mahjongker):
    name = "Bourdainker"
    description = "You may chi from the player across from you"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/bourdainker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Dollker
class Dollker(Mahjongker):
    name = "Dollker"
    description = "+$5 for discarding your seat wind"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dollker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Yenker
class Yenker(Mahjongker):
    name = "Yenker"
    description = "+$5 for discarding the table wind"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/yenker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Falchionker
class Falchionker(Mahjongker):
    name = "Falchionker"
    description = "+$3 for discarding any dragon"
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
    description = "Sequences can loop (912). +15 pts for a looped sequence."
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
            return (15, 0)
        else:
            return (0, 0)

# Bumungker
class Bumungker(Mahjongker):
    name = "Bumungker"
    description = "Gain +25 pts for each bamboo meld.  Once each turn, you may pay $2 to use Called Shot: Bamboo."
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
            total_score += 25
        if meld.suit == "dot" and fluteker in my_mahjongkers:
            total_score += 25
        if meld.suit == "character" and killtonyker in my_mahjongkers:
            total_score += 25
        if bamynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Dungker
class Dungker(Mahjongker):
    name = "Dungker"
    description = "Gain +25 pts for each bamboo meld.  Once each turn, you may pay $2 to use Called Shot: Dot."
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
            total_score += 25
        if meld.suit == "bamboo" and fluteker in my_mahjongkers:
            total_score += 25
        if meld.suit == "character" and iker in my_mahjongkers:
            total_score += 25
        if dynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Chungker
class Chungker(Mahjongker):
    name = "Chungker"
    description = "Gain +25 pts for each bamboo meld.  Once each turn, you may pay $2 to use Called Shot: Character."
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
            total_score += 25
        if meld.suit == "bamboo" and killtonyker in my_mahjongkers:
            total_score += 25
        if meld.suit == "dot" and iker in my_mahjongkers:
            total_score += 25
        if chynker in my_mahjongkers:
            total_score *= 2
        return (total_score, 0)

# Dragunker
class Dragunker(Mahjongker):
    name = "Dragunker"
    description = "Gain +30 pts for each dragon meld.  Once each turn, you may pay $2 to use Called Shot: Dragon."
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
    description = "Gain +35 pts for each wind meld.  Once each turn, you may pay $2 to use Called Shot: Wind."
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
    description = "Whenever a pretty is drawn, you may discard a tile at random and you gain two items. Draw to replace the discarded tile."
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
    description = "+40 points for each meld containing numbered tiles where all rank >= 5"
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
        score = 40
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
                    score += 40
            if chynker in my_mahjongkers:
                if (tile.suit == "character" or 
                    tile.suit == "dot" and iker in my_mahjongkers or 
                    tile.suit == "bamboo" and killtonyker in my_mahjongkers):
                    score += 40
            if dynker in my_mahjongkers:
                if (tile.suit == "dot" or 
                    tile.suit == "character" and iker in my_mahjongkers or 
                    tile.suit == "bamboo" and fluteker in my_mahjongkers):
                    score += 40
            return (score, 0)
        else:
            return (0, 0)

# Lowker
class Lowker(Mahjongker):
    name = "Lowker"
    description = "+40 points for each meld containing numbered tiles where all rank < 5"
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
        score = 40
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
                    score += 40
            if chynker in my_mahjongkers:
                if (tile.suit == "character" or 
                    tile.suit == "dot" and iker in my_mahjongkers or 
                    tile.suit == "bamboo" and killtonyker in my_mahjongkers):
                    score += 40
            if dynker in my_mahjongkers:
                if (tile.suit == "dot" or 
                    tile.suit == "character" and iker in my_mahjongkers or 
                    tile.suit == "bamboo" and fluteker in my_mahjongkers):
                    score += 40
            return (score, 0)
        else:
            return (0, 0)

# Rainbowker
class Rainbowker(Mahjongker):
    name = "Rainbowker"
    description = "You can form a rainbow suit meld with all three suits.  Gain +15 points for each of these melds."
    priority = 2 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
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
    description = "You can form a sequence with the three dragon suits"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/raindraker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Magellker
class Magellker(Mahjongker):
    name = "Magellker"
    description = "You can form a sequence with the winds. They are ordered dong (E) -> xi (S) -> nan (W) -> bei (N)"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/magellker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Salarymanker
class Salarymanker(Mahjongker):
    name = "Salarymanker"
    description = "+$4 at the end of the round"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/salarymanker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0, 4)

# MealTicker
class MealTicker(Mahjongker):
    name = "MealTicker"
    description = "+$4 each time you chi"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/mealticker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# WenGeker
class WenGeker(Mahjongker):
    name = "WenGeker"
    description = "+$4 each time you pong"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/wengeker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fourker
class Fourker(Mahjongker):
    name = "Fourker"
    description = "Whenever you lock in a meld, you may randomly replace a tile in your hand with a rank 4 tile.  If your scored hand has four rank 4 tiles, gain +40 pts"
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
            return (40, 0)
        return (0, 0)


# DOWker
class DOWker(Mahjongker):
    name = "DOWker"
    description = "At the start of the next shop, you may give this to another player.  They must give you back $5"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dowker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Comebacker
class Comebacker(Mahjongker):
    name = "Comebacker"
    description = "+$10 at the start of shop phase if you are in last place for total points"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/comebacker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Underdoker
class Underdoker(Mahjongker):
    name = "Underdoker"
    description = "+$5 whenever you place last in a round"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/underdoker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Compensaker
class Compensaker(Mahjongker):
    name = "Compensaker"
    description = "When you would draw 1 on your draw phase, instead draw 2"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/compensaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Gronkowsker
class Gronkowsker(Mahjongker):
    name = "Gronkowsker"
    description = "On your first turn each round, add a tile of your choice to your hand instead of drawing"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gronkowsker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Dumpsker
class Dumpsker(Mahjongker):
    name = "Dumpsker"
    description = "Once per round: when you would draw on your draw step, you may pay $3 to draw from the discard pile instead of the living wall"
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
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/copycatker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Boomerangker
class Boomerangker(Mahjongker):
    name = "Boomerangker"
    description = "If this mahjonker is empty: set aside a tile face-up on this card.  After three turns, you must draw this tile during your draw step if able. You may not use this again until the start of your next turn"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/boomerangker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Doraker
class Doraker(Mahjongker):
    name = "Doraker"
    description = "At the start of the round, a random tile from your hand is selected.  This mahjongker permanently gains +15 pts if you score this tile this round. Currently: 0"
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
    description = "All winds are the east wind."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/allforoneker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# OneforAllker
class OneforAllker(Mahjongker):
    name = "OneforAllker"
    description = "All dragons are the same dragon"
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/oneforallker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Pickgker
class Pickgker(Mahjongker):
    name = "Pickgker"
    description = "When you would gain an item, instead draw 3 and pick 1"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/pickgker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Straightker - pretty sure this shit doesn't work lol. test again later
class Straightker(Mahjongker):
    name = "Straightker"
    description = "+30 pts for every two sequence melds that are in sequence (1-2-3, 4-5-6)"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/straightker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        lows = []
        highs = []
        total_points = 0
        for meld in hand.melds:
            if meld.typing == "sequence":
                meld.tiles.sort(key=lambda tile: int(tile.rank))
                lows.append(meld.tiles[0])
                highs.append(meld.tiles[len(meld.tiles-1)])
        while len(highs) > 0:
            for i, high in enumerate(highs):
                for low in lows:
                    if int(high) == int(low) - 1:
                        total_points += 60
                        highs.remove(high)
                        lows.remove(low)
                        break
                    if i == len(high - 1):
                        return (total_points, 0)
        return (total_points, 0)

# Arthker
class Arthker(Mahjongker):
    name = "Arthker"
    description = "-1 max hand size. +30 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/arthker.jpg"

    def eval_score(self, my_mahjongkers):
        return (30, 0)

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
    description = "When you pong, take $2 from that player."
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
    description = "Chi from player that goes after you."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/anthonyker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Picker
class Picker(Mahjongker):
    name = "Picker"
    description = "Gain a free reroll each shop phase."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/picker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Luckgker
class Luckgker(Mahjongker):
    name = "Luckgker"
    description = "Any time you would roll a dice, you may roll 2 and pick one to keep."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/luckgker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Buffettker
class Buffettker(Mahjongker):
    name = "Buffettker"
    description = "For every $3 you have, +10 pts."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/buffettker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fuckgker
class Fuckgker(Mahjongker):
    name = "Fuckgker"
    description = "Whenever you take a tile from an opponent, this permanently gains +5 points. Current: 0"
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
    description = "Once per your turn, you may randomly discard a tile from your hand, and draw 1 tile. Gain $1."
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
    description = "Once per turn, you may use Called Shot: Rank. Costs $3 per use."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/snipker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Grenadeker
class Grenadeker(Mahjongker):
    name = "Grenadeker"
    description = "Once per turn, you may use Called Shot: Suit. Costs $3 per use."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/grenadeker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Stepsisker
class Stepsisker(Mahjongker):
    name = "Stepsisker"
    description = "Each tile taken from an opponent is worth +10 pts when scored. (chi, pong, and kong do NOT count)"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/stepsisker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# LarryEllisker
class LarryEllisker(Mahjongker):
    name = "LarryEllisker"
    description = "Up to once per turn you may pay $2 to scry 2."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/larryellisker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Suckgker
class Suckgker(Mahjongker):
    name = "Suckgker"
    description = "Every time you are targeted by another player this mahjongker permanently gains +5 points. Current: 0"
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
    description = "Each turn before you draw, guess the suit of the tile you’re about to draw.  If you get it right, gain $1."
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
    description = "If your hand contains 1, 2, 3, 5, and 8, +50 points."
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

        return (50, 0)

# Wokegker
class Wokegker(Mahjongker):
    name = "Wokegker"
    description = "Gain +50 points if your melds are of 3 different suits in your scored hand, excluding honors."
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
    description = "Each round, your opening hand will have 2 honors innately."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/shardker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Ponorker
class Ponorker(Mahjongker):
    name = "Ponorker"
    description = "When you pong, draw the next two honor tiles from the living wall. Discard 2 tiles."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/ponorker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Sonorker
class Sonorker(Mahjongker):
    name = "Sonorker"
    description = "When you chi, draw the next two honor tiles from the living wall. Discard 2 tiles."
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
    description = "You may form a blackjack type meld with tiles of the same suit that add up to 21."
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
    description = "At the start of the round, choose a player to give $3 to. Any time that player earns money this round, you also gain $2."
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
    description = "For every Zodiac you get this gains +7 pts permanently. Current: 0"
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
    description = "Randomly select another player at the start of each round.  Each time you target that player with an item or effect, get $1."
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
    description = "Worth 50 - the number of discarded tiles pts at first Mahjong."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/spoilker.jpg"
    point_value = 50

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
    description = "Whenever you chi, pong, or kong you get a random item."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gogogaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# DejaVuker
class DejaVuker(Mahjongker):
    name = "DejaVuker"
    description = "You must start each round with one random tile from each meld you scored last round."
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
    description = "When you would draw from the living wall, you may instead draw the most recently discarded tile."
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
    description = "Whenever you use a Called Shot, you may choose a second player to target."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
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
    description = "Worth 5x pts of the rank of the lowest rank tile scored."
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
    description = "Gain +15 pts for each honor meld."
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
    description = "Gain +15 pts for each sequence meld."
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
        score = 15
        if meld.typing == "sequence":
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

# Sameker
class Sameker(Mahjongker):
    name = "Sameker"
    description = "Gain +15 pts for each triplet meld."
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
        score = 15
        if meld.typing == "triplet":
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

# Odiumker
class Odiumker(Mahjongker):
    name = "Odiumker"
    description = "Once per turn, this mahjongker permanently gains +3 pts when you discard an honor tile. Currently: 0"
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
    description = "This mahjongker permanently gains +7 pts each time you score an honor meld. Current: 0"
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
    description = "When you manually reveal a meld, draw the most recently discarded honor tile."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/recykler.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Fardker
class Fardker(Mahjongker):
    name = "Fardker"
    description = "All winds score for you. Do not score bonus points for the table wind."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
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
    description = "All of your other mahjongkers are randomized (in their rarity category) at the start of each round.  Gain +40 pts at the end of the round."
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
    description = "Counter starts at 21.  Whenever you discard a tile, decrease the counter by the rank of the tile, honors are 10.  If the counter is at 0, this permanently gains +10 pts.  Else if you go negative, this permanently loses 5 pts.  Then reset the counter in either case."
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
    description = "The first mahjongker you buy each shop phase is free."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/recruitker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Squadker
class Squadker(Mahjongker):
    name = "Squadker"
    description = "At the start of each round, create 2 random common mahjongkers."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/squadker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Goalker
class Goalker(Mahjongker):
    name = "Goalker"
    description = "Randomly select a hand type (flush, sequence, set) at the start of the round.  Completing a mahjong hand of that type grants +30 pts."
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
    description = "Having two of the exact same meld gives +40 pts."
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/doubdoubker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        if len(hand.melds) <= 1: return (0, 0)
        if len(hand.melds) == 2:
            if (hand.melds[0] == hand.melds[1]):
                return (40, 0)
            else:
                return (0, 0)
        if len(hand.melds) == 3:
            if hand.melds[0] == hand.melds[1]:
                return (40, 0)
            elif hand.melds[0] == hand.melds[2]:
                return (40, 0)
            elif hand.melds[1] == hand.melds[2]:
                return (40, 0)
            else:
                return (0, 0)
        return (0, 0)

# Jeaucoeur
class Jeaucoeur(Mahjongker):
    name = "Jeaucoeur"
    description = "When you chi you may shuffle and redraw up to 3 tiles in your hand."
    priority = 3 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/jeaucoeur.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Unbumungker
class Unbumungker(Mahjongker):
    name = "Unbumungker"
    description = "Gain +5 pts for every bamboo tile that you discard."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/unbumungker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Undungker
class Undungker(Mahjongker):
    name = "Undungker"
    description = "Gain +5 pts for every dots tile that you discard."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/undungker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Unchungker
class Unchungker(Mahjongker):
    name = "Unchungker"
    description = "Gain +5 pts for every char tile that you discard."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/unchungker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Ranker
class Ranker(Mahjongker):
    name = "Ranker"
    description = "Gain +10 pts for every unique rank in your scored hand."
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
        return (len(rankset) * 10, 0)

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
    description = "Round Start: Gain a Re: Suitbaru. Gain +100 pts if ALL your melds have a different suit. (Chracter, Dots, Bamboo, Honor, etc.)"
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
        return (100, 0)

# Numbermanker
class Numbermanker(Mahjongker):
    name = "Numbermanker"
    description = "Round Start: Gain a Re: Surrection and select 3 random ranks.  If your scored hand has ALL 3 ranks, you gain +60 pts"
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/numbermanker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Consolaker
class Consolaker(Mahjongker):
    name = "Consolaker"
    description = "If you have scored the LEAST points in a round, destroy this jongker and gain +40 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/consolaker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# GumGumker
class GumGumker(Mahjongker):
    name = "GumGumker"
    description = "If you have scored the LEAST points in a round, destroy this jongker and gain +40 pts"
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/gumgumker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Conqker
class Conqker(Mahjongker):
    name = "Conqker"
    description = "At round end compare the total rank of each player's scored hands (honors are worth 10).  For EACH player that has a lower total rank than yours, gain +25 pts."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/conqker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Bingoker
class Bingoker(Mahjongker):
    name = "Bingoker"
    description = "This joker is a bingo sheet with 1 through 9.  When you score a tile with a rank, permanently cross off that number.  When all numbers are crossed off, gain +100 pts and destroy this joker."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
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
    description = "Roll a suit (bamboo, character, dots) at the start of the round. Each tile of this suit is worth +10 pts."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/worldker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Preciseker
class Preciseker(Mahjongker):
    name = "Preciseker"
    description = "Roll three ranks at the start of the round. Each tile of these ranks is worth +10 pts."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/preciseker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Symbioker
class Symbioker(Mahjongker):
    name = "Symbioker"
    description = "Each time you gain money, also gain +10 pts."
    priority = 6 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/symbioker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)

# Warrenker
class Warrenker(Mahjongker):
    name = "Warrenker"
    description = "At the end of the shop phase and after the final round, set your money to 0.  Gain 10 points for every $1."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
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
    description = "-2 hand size. If you mahjong, +75 pts."
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    sell_value = UNCOMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/dwker.jpg"

    def eval_score(self, my_mahjongkers, hand):
        if (len(hand.melds) >= 4):
            return (75, 0)
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

# Saveker
class Saveker(Mahjongker):
    name = "Saveker"
    description = "Counter at 0 each round. For every tile you discard, the counter increases by the rank (honors 10). Gain $1 for every 20 count at the end of the round."
    priority = 6 
    cost = COMMON_MAHJONGKER_COST
    sell_value = COMMON_MAHJONGKER_SELL_VALUE
    img_src = "/jongker/saveker.jpg"

    def eval_score(self, my_mahjongkers):
        return (0, 0)
    
# Arodker
class Arodker(Mahjongker):
    name = "Arodker"
    description = "At the start of a round, two random ranks are selected. Any tiles of this rank discarded will earn you $1."
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
    description = "When you lock in a meld slot, for each player that has a meld in that slot with matching suit OR type, take 10 pts from them."
    priority = 6 
    cost = RARE_MAHJONGKER_COST
    sell_value = RARE_MAHJONGKER_SELL_VALUE
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

# --------------------------------------------------------------------------------------
# MAHJONGKER LIST
# --------------------------------------------------------------------------------------
all_mahjongkers_list = []
all_mahjongkers_list.append(Bamonker())
all_mahjongkers_list.append(Donker())
all_mahjongkers_list.append(Chonker())
all_mahjongkers_list.append(Dragonker())
all_mahjongkers_list.append(Wonker())
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
all_mahjongkers_list.append(DEIker())
# all_mahjongkers_list.append(SEIquenker())
all_mahjongkers_list.append(Siker())
all_mahjongkers_list.append(Bourdainker())
all_mahjongkers_list.append(Dollker())
all_mahjongkers_list.append(Yenker())
all_mahjongkers_list.append(Falchionker())
all_mahjongkers_list.append(Neenjaker())
all_mahjongkers_list.append(Gayker())
all_mahjongkers_list.append(Bumungker())
all_mahjongkers_list.append(Dungker())
all_mahjongkers_list.append(Chungker())
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
all_mahjongkers_list.append(Boomerangker())
all_mahjongkers_list.append(Doraker())
all_mahjongkers_list.append(AllforOneker())
all_mahjongkers_list.append(OneforAllker())
all_mahjongkers_list.append(Pickgker())
all_mahjongkers_list.append(Straightker())
all_mahjongkers_list.append(Arthker())
# all_mahjongkers_list.append(DuckDuckGooseker())
all_mahjongkers_list.append(DebtCollectker())
all_mahjongkers_list.append(Quaker())
all_mahjongkers_list.append(Anthonyker())
all_mahjongkers_list.append(Picker())
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
all_mahjongkers_list.append(Riggedker())
all_mahjongkers_list.append(JosephJoesker())
all_mahjongkers_list.append(Fibonaccker())
all_mahjongkers_list.append(Wokegker())
all_mahjongkers_list.append(Shardker())
all_mahjongkers_list.append(Ponorker())
all_mahjongkers_list.append(Sonorker())
# all_mahjongkers_list.append(Speedker())
all_mahjongkers_list.append(Blackjackgker())
all_mahjongkers_list.append(Chairker())
all_mahjongkers_list.append(AngelInvesker())
# all_mahjongkers_list.append(Triker())
# all_mahjongkers_list.append(Emporerker())
# all_mahjongkers_list.append(Empressker())
# all_mahjongkers_list.append(Laobanker())
all_mahjongkers_list.append(Huntker())
# all_mahjongkers_list.append(Gourmetker())
# all_mahjongkers_list.append(Specialker())
all_mahjongkers_list.append(Spoilker())
all_mahjongkers_list.append(Harbingker())
all_mahjongkers_list.append(GoGoGaker())
all_mahjongkers_list.append(DejaVuker())
# all_mahjongkers_list.append(Coilker())
all_mahjongkers_list.append(Donnerker())
all_mahjongkers_list.append(Trashker())
# all_mahjongkers_list.append(Trapker())
all_mahjongkers_list.append(Sprayker())
all_mahjongkers_list.append(Vanillaker())
all_mahjongkers_list.append(NoReservaker())
all_mahjongkers_list.append(Bamanker())
all_mahjongkers_list.append(Danker())
all_mahjongkers_list.append(Chanker())
all_mahjongkers_list.append(Miniker())
all_mahjongkers_list.append(Honker())
all_mahjongkers_list.append(Eatker())
all_mahjongkers_list.append(Sameker())
all_mahjongkers_list.append(Odiumker())
all_mahjongkers_list.append(Bamenker())
all_mahjongkers_list.append(Denker())
all_mahjongkers_list.append(Chenker())
all_mahjongkers_list.append(Tanavastker())
all_mahjongkers_list.append(Recykler())
all_mahjongkers_list.append(Fardker())
all_mahjongkers_list.append(Fluteker())
all_mahjongkers_list.append(Iker())
all_mahjongkers_list.append(KillTonyker())
all_mahjongkers_list.append(Doldrumker())
all_mahjongkers_list.append(Discombobuker())
all_mahjongkers_list.append(Pivotker())
all_mahjongkers_list.append(Spanker())
all_mahjongkers_list.append(JackBlackgker())
all_mahjongkers_list.append(Recruitker())
all_mahjongkers_list.append(Squadker())
all_mahjongkers_list.append(Goalker())
all_mahjongkers_list.append(Doubker())
all_mahjongkers_list.append(DoubDoubker())
all_mahjongkers_list.append(Jeaucoeur())
all_mahjongkers_list.append(Unbumungker())
all_mahjongkers_list.append(Undungker())
all_mahjongkers_list.append(Unchungker())
all_mahjongkers_list.append(Ranker())
all_mahjongkers_list.append(DoubleDownker())
all_mahjongkers_list.append(Diffker())
all_mahjongkers_list.append(Numbermanker())
all_mahjongkers_list.append(Consolaker())
all_mahjongkers_list.append(GumGumker())
all_mahjongkers_list.append(Conqker())
all_mahjongkers_list.append(Bingoker())
all_mahjongkers_list.append(Bamynker())
all_mahjongkers_list.append(Dynker())
all_mahjongkers_list.append(Chynker())
all_mahjongkers_list.append(Hynker())
all_mahjongkers_list.append(Worldker())
all_mahjongkers_list.append(Preciseker())
all_mahjongkers_list.append(Symbioker())
all_mahjongkers_list.append(Warrenker())
all_mahjongkers_list.append(Crescendker())
all_mahjongkers_list.append(DWker())
all_mahjongkers_list.append(Fuseker())
all_mahjongkers_list.append(Saveker())
all_mahjongkers_list.append(Arodker())
all_mahjongkers_list.append(Spaghettiker())
all_mahjongkers_list.append(Tricker())
all_mahjongkers_list.append(Eggker())

# --------------------------------------------------------------------------------------
# MAHJONGKER DICT
# --------------------------------------------------------------------------------------
all_mahjongkers_dict = {}
all_mahjongkers_dict["bamonker"] = Bamonker()
all_mahjongkers_dict["donker"] = Donker()
all_mahjongkers_dict["chonker"] = Chonker()
all_mahjongkers_dict["dragonker"] = Dragonker()
all_mahjongkers_dict["wonker"] = Wonker()
# all_mahjongkers_dict["sequencker"] = Sequencker()
# all_mahjongkers_dict["mahmahmahjonker"] = MahMahMahjonker()
# all_mahjongkers_dict["milwaunker"] = Milwaunker()
# all_mahjongkers_dict["kohlker"] = Kohlker()
# all_mahjongkers_dict["windker"] = Windker()
# all_mahjongkers_dict["draker"] = Draker()
all_mahjongkers_dict["evenker"] = Evenker()
all_mahjongkers_dict["oddker"] = Oddker()
all_mahjongkers_dict["aycker"] = AYCker()
all_mahjongkers_dict["pingker"] = Pingker()
all_mahjongkers_dict["kingkongker"] = KingKongker()
all_mahjongkers_dict["gapker"] = Gapker()
all_mahjongkers_dict["deiker"] = DEIker()
# all_mahjongkers_dict["seiquenker"] = SEIquenker()
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
# all_mahjongkers_dict["bimingker"] = Bimingker()
# all_mahjongkers_dict["dingker"] = Dingker()
# all_mahjongkers_dict["chingker"] = Chingker()
all_mahjongkers_dict["hoardker"] = Hoardker()
# all_mahjongkers_dict["meldker"] = Meldker()
# all_mahjongkers_dict["snakeker"] = Snakeker()
# all_mahjongkers_dict["seeker"] = Seeker()
# all_mahjongkers_dict["leesinker"] = LeeSinker()
# all_mahjongkers_dict["seeingdoubker"] = SeeingDoubker()
# all_mahjongkers_dict["seequenker"] = Seequenker()
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
# all_mahjongkers_dict["duckduckgooseker"] = DuckDuckGooseker()
all_mahjongkers_dict["debtcollectker"] = DebtCollectker()
all_mahjongkers_dict["quaker"] = Quaker()
all_mahjongkers_dict["anthonyker"] = Anthonyker()
all_mahjongkers_dict["picker"] = Picker()
all_mahjongkers_dict["luckgker"] = Luckgker()
all_mahjongkers_dict["buffettker"] = Buffettker()
all_mahjongkers_dict["fuckgker"] = Fuckgker()
all_mahjongkers_dict["toker"] = Toker()
# all_mahjongkers_dict["emeraldker"] = Emeraldker()
all_mahjongkers_dict["snipker"] = Snipker()
all_mahjongkers_dict["grenadeker"] = Grenadeker()
all_mahjongkers_dict["stepsisker"] = Stepsisker()
all_mahjongkers_dict["larryellisker"] = LarryEllisker()
all_mahjongkers_dict["suckgker"] = Suckgker()
# all_mahjongkers_dict["oracker"] = Oracker()
all_mahjongkers_dict["riggedker"] = Riggedker()
all_mahjongkers_dict["josephjoesker"] = JosephJoesker()
all_mahjongkers_dict["fibonaccker"] = Fibonaccker()
all_mahjongkers_dict["wokegker"] = Wokegker()
all_mahjongkers_dict["shardker"] = Shardker()
all_mahjongkers_dict["ponorker"] = Ponorker()
all_mahjongkers_dict["sonorker"] = Sonorker()
# all_mahjongkers_dict["speedker"] = Speedker()
all_mahjongkers_dict["blackjackgker"] = Blackjackgker()
all_mahjongkers_dict["chairker"] = Chairker()
all_mahjongkers_dict["angelinvesker"] = AngelInvesker()
# all_mahjongkers_dict["triker"] = Triker()
# all_mahjongkers_dict["emporerker"] = Emporerker()
# all_mahjongkers_dict["empressker"] = Empressker()
# all_mahjongkers_dict["laobanker"] = Laobanker()
all_mahjongkers_dict["huntker"] = Huntker()
# all_mahjongkers_dict["gourmetker"] = Gourmetker()
# all_mahjongkers_dict["specialker"] = Specialker()
all_mahjongkers_dict["spoilker"] = Spoilker()
all_mahjongkers_dict["harbingker"] = Harbingker()
all_mahjongkers_dict["gogogaker"] = GoGoGaker()
all_mahjongkers_dict["dejavuker"] = DejaVuker()
# all_mahjongkers_dict["coilker"] = Coilker()
all_mahjongkers_dict["donnerker"] = Donnerker()
all_mahjongkers_dict["trashker"] = Trashker()
# all_mahjongkers_dict["trapker"] = Trapker()
all_mahjongkers_dict["sprayker"] = Sprayker()
all_mahjongkers_dict["vanillaker"] = Vanillaker()
# all_mahjongkers_dict["noreservaker"] = NoReservaker()
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
all_mahjongkers_dict["saveker"] = Saveker()
all_mahjongkers_dict["arodker"] = Arodker()
all_mahjongkers_dict["spaghettiker"] = Spaghettiker()
all_mahjongkers_dict["tricker"] = Tricker()
all_mahjongkers_dict["eggker"] = Eggker()

# ----------------------------------------------

# --------------------------------------------------------------------------------------
# COMMON MAHJONGKER LIST
# --------------------------------------------------------------------------------------
common_mahjongkers_list = []
for mahjongker in all_mahjongkers_list:
    if mahjongker.cost == COMMON_MAHJONGKER_COST:
        common_mahjongkers_list.append(mahjongker)

# --------------------------------------------------------------------------------------
# UNCOMMON MAHJONGKER LIST
# --------------------------------------------------------------------------------------
uncommon_mahjongkers_list = []
for mahjongker in all_mahjongkers_list:
    if mahjongker.cost == UNCOMMON_MAHJONGKER_COST:
        uncommon_mahjongkers_list.append(mahjongker)

# --------------------------------------------------------------------------------------
# RARE MAHJONGKER LIST
# --------------------------------------------------------------------------------------
rare_mahjongkers_list = []
for mahjongker in all_mahjongkers_list:
    if mahjongker.cost == RARE_MAHJONGKER_COST:
        rare_mahjongkers_list.append(mahjongker)

# --------------------------------------------------------------------------------------
# INITIAL MAHJONGKER LIST
# --------------------------------------------------------------------------------------
initial_mahjongkers_list = []
initial_mahjongkers_list.append(Bamonker())
initial_mahjongkers_list.append(Donker())
initial_mahjongkers_list.append(Chonker())
initial_mahjongkers_list.append(Dragonker())
initial_mahjongkers_list.append(Wonker())
initial_mahjongkers_list.append(Evenker())
initial_mahjongkers_list.append(Oddker())
initial_mahjongkers_list.append(AYCker())
initial_mahjongkers_list.append(Pingker())
initial_mahjongkers_list.append(KingKongker())
initial_mahjongkers_list.append(Dollker())
initial_mahjongkers_list.append(Yenker())
initial_mahjongkers_list.append(Falchionker())
initial_mahjongkers_list.append(Neenjaker())
initial_mahjongkers_list.append(Highker())
initial_mahjongkers_list.append(Lowker())
initial_mahjongkers_list.append(Salarymanker())
initial_mahjongkers_list.append(MealTicker())
initial_mahjongkers_list.append(WenGeker())
initial_mahjongkers_list.append(Fourker())
initial_mahjongkers_list.append(Underdoker())
initial_mahjongkers_list.append(Doraker())
initial_mahjongkers_list.append(Pickgker())
initial_mahjongkers_list.append(Straightker())
initial_mahjongkers_list.append(DebtCollectker())
initial_mahjongkers_list.append(Picker())
initial_mahjongkers_list.append(Fuckgker())
initial_mahjongkers_list.append(JosephJoesker())
initial_mahjongkers_list.append(Fibonaccker())
initial_mahjongkers_list.append(Wokegker())
initial_mahjongkers_list.append(Shardker())
initial_mahjongkers_list.append(Ponorker())
initial_mahjongkers_list.append(Sonorker())
initial_mahjongkers_list.append(Blackjackgker())
initial_mahjongkers_list.append(Chairker())
initial_mahjongkers_list.append(Huntker())
initial_mahjongkers_list.append(Spoilker())
initial_mahjongkers_list.append(Vanillaker())
initial_mahjongkers_list.append(Bamanker())
initial_mahjongkers_list.append(Danker())
initial_mahjongkers_list.append(Chanker())
initial_mahjongkers_list.append(Miniker())
initial_mahjongkers_list.append(Honker())
initial_mahjongkers_list.append(Eatker())
initial_mahjongkers_list.append(Sameker())
initial_mahjongkers_list.append(Odiumker())
initial_mahjongkers_list.append(Bamenker())
initial_mahjongkers_list.append(Denker())
initial_mahjongkers_list.append(Chenker())
initial_mahjongkers_list.append(Tanavastker())
initial_mahjongkers_list.append(Recykler())
initial_mahjongkers_list.append(Doldrumker())
initial_mahjongkers_list.append(Pivotker())
initial_mahjongkers_list.append(Spanker())
initial_mahjongkers_list.append(JackBlackgker())
initial_mahjongkers_list.append(Recruitker())
initial_mahjongkers_list.append(Goalker())
initial_mahjongkers_list.append(Doubker())
initial_mahjongkers_list.append(DoubDoubker())
initial_mahjongkers_list.append(Jeaucoeur())