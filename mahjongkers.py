from tiles import *

# ------------------------------------------------
# GLOBALS
# ------------------------------------------------

COMMON_MAHJONGKER_COST = 3
UNCOMMON_MAHJONGKER_COST = 6
RARE_MAHJONGKER_COST = 10



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

    def determine_suit(self):
        self.suit = sorted(self.tiles, key=lambda tile: tile.rank)[0].suit

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
        # check sequence hand
        for meld in self.melds:
            if meld.typing == "sequence":
                continue
            elif meld.typing == "triplet":
                if meld.suit == "dragon" or meld.suit == "wind":
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
                if meld.suit == "dragon" or meld.suit == "wind":
                    self.is_flush = False
                else:
                    current_suit = meld.suit
            elif meld.suit == current_suit:
                continue
            elif meld.suit == "dragon" or meld.suit == "wind":
                self.is_flush = False
            else:
                self.is_flush = False
                self.is_half_flush = False
                break
        if self.is_flush and self.eyes[0].suit != current_suit:
            self.is_flush = False
        if self.is_half_flush and self.eyes[0].suit != "dragon" and self.eyes[0].suit != "wind" and self.eyes[0].suit != current_suit:
            self.is_half_flush = False

    def __repr__(self):
        return repr((self.melds, self.eyes))

class Mahjongker:
    name = "" # for jank reasons the name MUST be the same as the img_src name
    description = ""
    priority = 0 
    cost = 2
    img_src = ""
    # lower priority gets scored first
    # 0 is for validity checking
    # 1 is for tile checking
    # 2 is for meld checking
    # 3 is for eyes checking
    # 4 is for hand checking
    # 5 is for no interaction 

    def __repr__(self):
        return repr((self.name, self.description, self.priority))

    def __eq__(self, other):
        return self.name == other.name

    def eval_score(self):
        print("I'm a dumb parent score func")
        return 0

# --------------------------------------------------------------------------------------
# MAHJONGKERS
# --------------------------------------------------------------------------------------

# Bamonker
class Bamonker(Mahjongker):
    name = "Bamonker"
    description = "+15 pts for each bamboo meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/bamonker.jpg"

    def eval_score(self, meld):
        if meld.suit == "bamboo":
            return (15, 0)
        else:
            return (0, 0)

# Donker
class Donker(Mahjongker):
    name = "Donker"
    description = "+15 pts for each dot meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/donker.jpg"

    def eval_score(self, meld):
        if meld.suit == "dot":
            return (15, 0)
        else:
            return (0, 0)

# Chonker
class Chonker(Mahjongker):
    name = "Chonker"
    description = "+15 pts for each character meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/chonker.jpg"

    def eval_score(self, meld):
        if meld.suit == "character":
            return (15, 0)
        else:
            return (0, 0)

# Dragonker
class Dragonker(Mahjongker):
    name = "Dragonker"
    description = "+45 pts for each dragon meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/dragonker.jpg"

    def eval_score(self, meld):
        if meld.suit == "dragon":
            return (45, 0)
        else:
            return (0, 0)

# Winker
class Winker(Mahjongker):
    name = "Winker"
    description = "+30 pts for each wind meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/winker.jpg"

    def eval_score(self, meld):
        if meld.suit == "wind":
            return (30, 0)
        else:
            return (0, 0)

# Sequencker
class Sequencker(Mahjongker):
    name = "Sequencker"
    description = "+2 mult for sequence hand"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/sequencker.jpg"

    def eval_score(self, hand):
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
    img_src = "/jongker/mahmahmahjonker.jpg"

    def eval_score(self, hand):
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
    img_src = "/jongker/milwaunker.jpg"

    # what happens if hand is all honors?
    def eval_score(self, hand):
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
    img_src = "/jongker/kohlker.jpg"

    # what happens if hand is all honors?
    def eval_score(self, hand):
        if hand.is_flush:
            return (0, 7)
        else:
            return (0, 0)

# Windker
class Windker(Mahjongker):
    name = "Windker"
    description = "+0.6 mult for each wind meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/windker.jpg"

    def eval_score(self, meld):
        if meld.suit == "wind":
            return (0, 0.6)
        else:
            return (0, 0)

# Draker
class Draker(Mahjongker):
    name = "Draker"
    description = "+0.5 mult for each dragon meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/draker.jpg"

    def eval_score(self, meld):
        if meld.suit == "dragon":
            return (0, 0.5)
        else:
            return (0, 0)


# Evenker
class Evenker(Mahjongker):
    name = "Evenker"
    description = "+5 pts for each even tile"
    priority = 1 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/evenker.jpg"

    def eval_score(self, tile):
        if tile.suit == "bamboo" or tile.suit == "dot" or tile.suit == "character":
            if int(tile.rank) % 2 == 0:
                return (5, 0)
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
    img_src = "/jongker/oddker.jpg"

    def eval_score(self, tile):
        if tile.suit == "bamboo" or tile.suit == "dot" or tile.suit == "character":
            if int(tile.rank) % 1 == 0:
                return (5, 0)
            else:
                return (0, 0)
        else:
            return (0, 0)

# AYCker
class AYCker(Mahjongker):
    name = "AYCker"
    description = "This Mahjongker gains +15 pts on chi (stacking) Current: 0"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/aycker.jpg"
    point_value = 0

    def eval_score(self):
        return (self.point_value, 0)

# Pingker
class Pingker(Mahjongker):
    name = "Pingker"
    description = "This Mahjongker gains +20 pts on pong (stacking) Current: 0"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/pingker.jpg"
    point_value = 0

    def eval_score(self):
        return (self.point_value, 0)

# KingKongker
class KingKongker(Mahjongker):
    name = "KingKongker"
    description = "This Mahjongker gains +40 pts on kong (stacking) Current: 0"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/kingkongker.jpg"
    point_value = 0

    def eval_score(self):
        return (self.point_value, 0)

# Gapker
class Gapker(Mahjongker):
    name = "Gapker"
    description = "Sequences may contain one gap of 1 (1-2-4 valid, 2-4-6 not valid)"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/gapker.jpg"

    def eval_score(self):
        return (0, 0)

# DEIker
class DEIker(Mahjongker):
    name = "DEIker"
    description = "Triplets may contain up to two different suits (honors excluded)"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/deiker.jpg"

    def eval_score(self):
        return (0, 0)

# Siker
class Siker(Mahjongker):
    name = "Siker"
    description = "You may form a kong with a sequence (chi only, 3456)"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/siker.jpg"

    def eval_score(self):
        return (0, 0)

# Bourdainker
class Bourdainker(Mahjongker):
    name = "Bourdainker"
    description = "You may chi from the player across from you"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/bourdainker.jpg"

    def eval_score(self):
        return (0, 0)

# Dollker
class Dollker(Mahjongker):
    name = "Dollker"
    description = "+$5 for discarding your seat wind"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/dollker.jpg"

    def eval_score(self):
        return (0, 0)

# Yenker
class Yenker(Mahjongker):
    name = "Yenker"
    description = "+$5 for discarding the table wind"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/yenker.jpg"

    def eval_score(self):
        return (0, 0)

# Falchionker
class Falchionker(Mahjongker):
    name = "Falchionker"
    description = "+$3 for discarding any dragon"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/falchionker.jpg"

    def eval_score(self):
        return (0, 0)

# Neenjaker
class Neenjaker(Mahjongker):
    name = "Neenjaker"
    description = "+15 points for each hidden meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/neenjaker.jpg"

    def eval_score(self, meld):
        if meld.hidden:
            return (15, 0)
        else:
            return (0, 0)

# Gayker
class Gayker(Mahjongker):
    name = "Gayker"
    description = "Sequences can loop (912)"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/gayker.jpg"

    def eval_score(self):
        return (0, 0)

# Bumungker
class Bumungker(Mahjongker):
    name = "Bumungker"
    description = "+30 pts for a hand with only bamboos (excluding honors)"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/bumungker.jpg"

    def eval_score(self, hand):
        all_bamboos = True
        for meld in hand:
            if meld.suit != "bamboo" and meld.suit != "dragon" and meld.suit != "wind":
                all_bamboos = False
        if all_bamboos:
            return (30, 0)
        else:
            return (0, 0)

# Dungker
class Dungker(Mahjongker):
    name = "Dungker"
    description = "+30 pts for a hand with only dots (excluding honors)"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/dungker.jpg"

    def eval_score(self, hand):
        all_dots = True
        for meld in hand:
            if meld.suit != "dot" and meld.suit != "dragon" and meld.suit != "wind":
                all_dots = False
        if all_dots:
            return (30, 0)
        else:
            return (0, 0)

# Chungker
class Chungker(Mahjongker):
    name = "Chungker"
    description = "+30 pts for a hand with only characters (excluding honors)"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/chungker.jpg"

    def eval_score(self, hand):
        all_chars = True
        for meld in hand:
            if meld.suit != "character" and meld.suit != "dragon" and meld.suit != "wind":
                all_chars = False
        if all_chars:
            return (30, 0)
        else:
            return (0, 0)

# Bimingker
class Bimingker(Mahjongker):
    name = "Bimingker"
    description = "+0.4 mult for each bamboo meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/bimingker.jpg"

    def eval_score(self, meld):
        if meld.suit == "bamboo":
            return (0, 0.4)
        else:
            return (0, 0)

# Dingker
class Dingker(Mahjongker):
    name = "Dingker"
    description = "+0.4 mult for each dot meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/dingker.jpg"

    def eval_score(self, meld):
        if meld.suit == "dot":
            return (0, 0.4)
        else:
            return (0, 0)

# Chingker
class Chingker(Mahjongker):
    name = "Chingker"
    description = "+0.4 mult for each character meld"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/chingker.jpg"

    def eval_score(self, meld):
        if meld.suit == "character":
            return (0, 0.4)
        else:
            return (0, 0)

# Hoardker
class Hoardker(Mahjongker):
    name = "Hoardker"
    description = "Whenever a pretty is drawn, you may discard a tile at random and you gain two items. Draw to replace the discarded tile"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/hoardker.jpg"

    def eval_score(self):
        return (0, 0)

# Meldker
class Meldker(Mahjongker):
    name = "Meldker"
    description = "If the last 3 tiles you discarded form a meld, +30 points (stacking) Current: 0"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/meldker.jpg"
    point_value = 0

    def eval_score(self):
        return (self.point_value, 0)

# Snakeker
class Snakeker(Mahjongker):
    name = "Snakeker"
    description = "+111 pts if your eyes are rank 1"
    priority = 3 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/snakeker.jpg"

    def eval_score(self, eyes):
        for tile in eyes.tiles:
            if tile.rank != "1":
                return (0, 0)
        if rank_1:
            return (111, 0)
        return (0, 0)

# Seeker
class Seeker(Mahjongker):
    name = "Seeker"
    description = "You may pong your eyes at any time"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/seeker.jpg"

    def eval_score(self):
        return (0, 0)

# LeeSinker
class LeeSinker(Mahjongker):
    name = "LeeSinker"
    description = "You can mahjong without eyes.  The eye tiles are not considered for determining your hand type. -100 base points if you mahjong this way"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/leesinker.jpg"
    active = False

    def eval_score(self):
        if active:
            return (-100, 0)
        else:
            return (0, 0)

# SeeingDoubker
class SeeingDoubker(Mahjongker):
    name = "SeeingDoubker"
    description = "+2 mult if your eyes are rank 2"
    priority = 3 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/seeingdoubker.jpg"

    def eval_score(self, eyes):
        rank_2 = True
        for tile in eyes.tiles:
            if tile.rank != "2":
                rank_2 = False
                return (0, 0)
        if rank_2:
            (0, 2)
        else:
            (0, 0)

# Seequenker
class Seequenker(Mahjongker):
    name = "Seequenker"
    description = "Your eyes can be a sequence"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/seequenker.jpg"

    def eval_score(self):
        return (0, 0)

# Highker
class Highker(Mahjongker):
    name = "Highker"
    description = "+15 points for each meld containing numbered tiles where all rank > 5"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/highker.jpg"

    def eval_score(self, meld):
        high = True
        for tile in meld:
            if tile.rank <= 5:
                high = False
                return (0, 0)
        if high:
            return (15, 0)
        else:
            return (0, 0)

# Lowker
class Lowker(Mahjongker):
    name = "Lowker"
    description = "+15 points for each meld containing numbered tiles where all rank < 5"
    priority = 2 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/lowker.jpg"

    def eval_score(self, meld):
        low = True
        for tile in meld:
            if tile.rank >= 5:
                low = False
                return (0, 0)
        if low:
            return (15, 0)
        else:
            return (0, 0)

# Rainbowker
class Rainbowker(Mahjongker):
    name = "Rainbowker"
    description = "You can form a meld with all three suits. You cannot do this via chi or pong. +15 points for each of these melds"
    priority = 2 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/rainbowker.jpg"

    def eval_score(self, meld):
        seen_suits = []
        for tile in meld:
            if tile.suit in seen_suits:
                return (0, 0)
            else:
                seen_suits.append(tile.suit)
        return (15, 0)

# Raindraker
class Raindraker(Mahjongker):
    name = "Raindraker"
    description = "You can form a sequence with the three dragon suits"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/raindraker.jpg"

    def eval_score(self):
        return (0, 0)

# Magellker
class Magellker(Mahjongker):
    name = "Magellker"
    description = "You can form a sequence with the winds. They are ordered dong (E) -> xi (S) -> nan (W) -> bei (N)"
    priority = 5 
    cost = UNCOMMON_MAHJONGKER_COST
    img_src = "/jongker/magellker.jpg"

    def eval_score(self):
        return (0, 0)

# Salarymanker
class Salarymanker(Mahjongker):
    name = "Salarymanker"
    description = "+$4 at the end of the round"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/salarymanker.jpg"

    def eval_score(self):
        return (0, 0)

# MealTicker
class MealTicker(Mahjongker):
    name = "MealTicker"
    description = "+$4 each time you chi"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/mealticker.jpg"

    def eval_score(self):
        return (0, 0)

# WenGeker
class WenGeker(Mahjongker):
    name = "WenGeker"
    description = "+$4 each time you pong"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/wengeker.jpg"

    def eval_score(self):
        return (0, 0)

# Fourker
class Fourker(Mahjongker):
    name = "Fourker"
    description = "+$8 each time you kong"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/fourker.jpg"

    def eval_score(self):
        return (0, 0)

# DOWker
class DOWker(Mahjongker):
    name = "DOWker"
    description = "At the start of the next shop, you may give this to another player.  They must give you back $5"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/DOWker.jpg"

    def eval_score(self):
        return (0, 0)

# Comebacker
class Comebacker(Mahjongker):
    name = "Comebacker"
    description = "+$10 at the start of shop phase if you are in last place for total points"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/comebacker.jpg"

    def eval_score(self):
        return (0, 0)

# Underdoker
class Underdoker(Mahjongker):
    name = "Underdoker"
    description = "+$5 whenever you place last in a round"
    priority = 5 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/underdoker.jpg"

    def eval_score(self):
        return (0, 0)

# Compensaker
class Compensaker(Mahjongker):
    name = "Compensaker"
    description = "When you would draw 1 on your draw phase, instead draw 2"
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    img_src = "/jongker/compensaker.jpg"

    def eval_score(self):
        return (0, 0)

# Gronkowsker
class Gronkowsker(Mahjongker):
    name = "Gronkowsker"
    description = "On your first turn each round, add a wild tile of your choice to your hand instead of drawing"
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    img_src = "/jongker/gronkowsker.jpg"

    def eval_score(self):
        return (0, 0)

# Dumpsker
class Dumpsker(Mahjongker):
    name = "Dumpsker"
    description = "Once per round: when you would draw on your draw step, you may draw from the discard pile instead of the living wall"
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    img_src = "/jongker/dumpsker.jpg"

    def eval_score(self):
        return (0, 0)

# Copycatker
class Copycatker(Mahjongker):
    name = "Copycatker"
    description = "During scoring: choose one of your melds to become an exact copy of another player's meld"
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    img_src = "/jongker/copycatker.jpg"

    def eval_score(self):
        return (0, 0)

# Boomerangker
class Boomerangker(Mahjongker):
    name = "Boomerangker"
    description = "If this mahjonker is empty: set aside a tile face-up on this card.  After three turns, you must draw this tile during your draw step if able. You may not use this again until the start of your next turn"
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    img_src = "/jongker/boomerangker.jpg"

    def eval_score(self):
        return (0, 0)

# Doraker
class Doraker(Mahjongker):
    name = "Doraker"
    description = "At the start of the round, a random tile is selected. That tile is worth an additional 20 points when scored"
    priority = 1 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/doraker.jpg"
    selected_tile = []

    def eval_score(self, tile):
        if tile.suit == selected_tile.suit and tile.rank == selected_tile.rank:
            return (20, 0)
        else:
            return (0, 0)

# AllforOneker - needs special scoring check
class AllforOneker(Mahjongker):
    name = "AllforOneker"
    description = "All winds are your seat wind"
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    img_src = "/jongker/allforoneker.jpg"

    def eval_score(self):
        return (0, 0)

# OneforAllker
class OneforAllker(Mahjongker):
    name = "OneforAllker"
    description = "All dragons are the same dragon"
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    img_src = "/jongker/oneforallker.jpg"

    def eval_score(self):
        return (0, 0)

# Pickgker
class Pickgker(Mahjongker):
    name = "Pickgker"
    description = "When you would gain an item, instead draw 3 and pick 1"
    priority = 5 
    cost = RARE_MAHJONGKER_COST
    img_src = "/jongker/pickgker.jpg"

    def eval_score(self):
        return (0, 0)

# Straightker - pretty sure this shit doesn't work lol. test again later
class Straightker(Mahjongker):
    name = "Straightker"
    description = "+60 pts for every two sequence melds that are in sequence (1-2-3, 4-5-6)"
    priority = 4 
    cost = COMMON_MAHJONGKER_COST
    img_src = "/jongker/straightker.jpg"

    def eval_score(self, hand):
        lows = []
        highs = []
        total_points = 0
        for meld in hand.melds:
            if meld.typing == "sequence":
                meld.tiles.sort(key=lambda tile: tile.rank)
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

# --------------------------------------------------------------------------------------
# MAHJONGKER LIST
# --------------------------------------------------------------------------------------
all_mahjongkers_list = []
all_mahjongkers_list.append(Bamonker())
all_mahjongkers_list.append(Donker())
all_mahjongkers_list.append(Chonker())
all_mahjongkers_list.append(Dragonker())
all_mahjongkers_list.append(Winker())
all_mahjongkers_list.append(Sequencker())
all_mahjongkers_list.append(MahMahMahjonker())
all_mahjongkers_list.append(Milwaunker())
all_mahjongkers_list.append(Kohlker())
all_mahjongkers_list.append(Windker())
all_mahjongkers_list.append(Draker())
all_mahjongkers_list.append(Evenker())
all_mahjongkers_list.append(Oddker())
all_mahjongkers_list.append(AYCker())
all_mahjongkers_list.append(Pingker())
all_mahjongkers_list.append(KingKongker())
all_mahjongkers_list.append(Gapker())
all_mahjongkers_list.append(DEIker())
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
all_mahjongkers_list.append(Bimingker())
all_mahjongkers_list.append(Dingker())
all_mahjongkers_list.append(Chingker())
all_mahjongkers_list.append(Hoardker())
all_mahjongkers_list.append(Meldker())
all_mahjongkers_list.append(Snakeker())
all_mahjongkers_list.append(Seeker())
all_mahjongkers_list.append(LeeSinker())
all_mahjongkers_list.append(SeeingDoubker())
all_mahjongkers_list.append(Seequenker())
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
# --------------------------------------------------------------------------------------
# MAHJONGKER DICT
# --------------------------------------------------------------------------------------
all_mahjongkers_dict = {}
all_mahjongkers_dict["bamonker"] = Bamonker()
all_mahjongkers_dict["donker"] = Donker()
all_mahjongkers_dict["chonker"] = Chonker()
all_mahjongkers_dict["dragonker"] = Dragonker()
all_mahjongkers_dict["winker"] = Winker()
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