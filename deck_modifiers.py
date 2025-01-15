class Zodiac:
    name = ""
    description = ""
    img_src = ""
    cost = 3

    def __repr__(self):
        return repr((self.name, self.description))

    def __eq__(self, other):
        return self.name == other.name

class Trigram:
    name = ""
    description = ""
    img_src = ""
    cost = 3

    def __repr__(self):
        return repr((self.name, self.description))

    def __eq__(self, other):
        return self.name == other.name

# --------------------------------------------------------------------------------------
# ZODIACS
# --------------------------------------------------------------------------------------

class Zodiac_Rat(Zodiac):
    name = "Rat"
    description = "Decrease 4 tiles rank by 1."
    img_src = "/zodiac/rat.jpg"

class Zodiac_Ox(Zodiac):
    name = "Ox"
    description = "Increase 4 tiles rank by 1."
    img_src = "/zodiac/ox.jpg"

class Zodiac_Tiger(Zodiac):
    name = "Tiger"
    description = "Add 1 wild tile to the deck."
    img_src = "/zodiac/tiger.jpg"

class Zodiac_Rabbit(Zodiac):
    name = "Rabbit"
    description = "Duplicate a tile."
    img_src = "/zodiac/rabbit.jpg"

class Zodiac_Dragon(Zodiac):
    name = "Dragon"
    description = "Add 4 different honor tiles of your choice to the deck."
    img_src = "/zodiac/dragon.jpg"

class Zodiac_Snake(Zodiac):
    name = "Snake"
    description = "Remove 2 tiles from the game."
    img_src = "/zodiac/snake.jpg"

class Zodiac_Horse(Zodiac):
    name = "Horse"
    description = "Change 4 suited tiles to Characters."
    img_src = "/zodiac/horse.jpg"

class Zodiac_Goat(Zodiac):
    name = "Goat"
    description = "Smear an honor tile."
    img_src = "/zodiac/goat.jpg"

class Zodiac_Monkey(Zodiac):
    name = "Monkey"
    description = "Change 4 suited tiles to Bamboo."
    img_src = "/zodiac/monkey.jpg"

class Zodiac_Rooster(Zodiac):
    name = "Rooster"
    description = "Smear the rank of a tile."
    img_src = "/zodiac/rooster.jpg"

class Zodiac_Dog(Zodiac):
    name = "Dog"
    description = "Change 4 suited tiles to Dots."
    img_src = "/zodiac/dog.jpg"

class Zodiac_Pig(Zodiac):
    name = "Pig"
    description = "Smear the suit of a tile."
    img_src = "/zodiac/pig.jpg"

class Zodiac_Cat(Zodiac):
    name = "Cat"
    description = "Goldify 2 tiles. A gold tile grants a player that scores it $5."
    img_src = "/zodiac/cat.jpg"


# --------------------------------------------------------------------------------------
# TRIGRAMS
# --------------------------------------------------------------------------------------

class Trigram_Sky(Trigram):
    name = "Sky"
    description = "[Seal] This tile can never be locked in. This tile is worth +15 points when scored."
    img_src = "/trigram/sky.jpg"

class Trigram_Lake(Trigram):
    name = "Lake"
    description = "[Seal] When a player draws this tile, they must give this to its owner. The owner gives a tile of their choice back."
    img_src = "/trigram/lake.jpg"

class Trigram_Fire(Trigram):
    name = "Fire"
    description = "[Seal] When this tile is drawn, you may create a copy of it for this round by discarding another tile from your hand."
    img_src = "/trigram/fire.jpg"

class Trigram_Thunder(Trigram):
    name = "Thunder"
    description = "[Seal] This tile scores twice. If not scored by owner, the owner scores this tile as well."
    img_src = "/trigram/thunder.jpg"

class Trigram_Wind(Trigram):
    name = "Wind"
    description = "[Seal] When this tile is drawn, its owner's turn is next."
    img_src = "/trigram/wind.jpg"

class Trigram_Water(Trigram):
    name = "Water"
    description = "[Seal] When this tile is drawn, you pay its owner $2."
    img_src = "/trigram/water.jpg"

class Trigram_Mountain(Trigram):
    name = "Mountain"
    description = "[Seal] This tile cannot be discarded. This tile is worth +15 points when scored."
    img_src = "/trigram/mountain.jpg"

class Trigram_Earth(Trigram):
    name = "Earth"
    description = "[Seal] Place a deed of ownership on a tile. Whenever a player scores this tile, they give the owner $5 at the next shop phase."
    img_src = "/trigram/earth.jpg"

# --------------------------------------------------------------------------------------
# ALL ZODIACS LIST
# --------------------------------------------------------------------------------------

all_zodiacs_list = []
all_zodiacs_list.append(Zodiac_Rat())
all_zodiacs_list.append(Zodiac_Ox())
all_zodiacs_list.append(Zodiac_Tiger())
all_zodiacs_list.append(Zodiac_Rabbit())
all_zodiacs_list.append(Zodiac_Dragon())
all_zodiacs_list.append(Zodiac_Snake())
all_zodiacs_list.append(Zodiac_Horse())
all_zodiacs_list.append(Zodiac_Goat())
all_zodiacs_list.append(Zodiac_Monkey())
all_zodiacs_list.append(Zodiac_Rooster())
all_zodiacs_list.append(Zodiac_Dog())
all_zodiacs_list.append(Zodiac_Pig())
all_zodiacs_list.append(Zodiac_Cat())

# --------------------------------------------------------------------------------------
# ZODIACS DICT
# --------------------------------------------------------------------------------------
all_zodiacs_dict = {}
all_zodiacs_dict["rat"] = Zodiac_Rat()
all_zodiacs_dict["ox"] = Zodiac_Ox()
all_zodiacs_dict["tiger"] = Zodiac_Tiger()
all_zodiacs_dict["rabbit"] = Zodiac_Rabbit()
all_zodiacs_dict["dragon"] = Zodiac_Dragon()
all_zodiacs_dict["snake"] = Zodiac_Snake()
all_zodiacs_dict["horse"] = Zodiac_Horse()
all_zodiacs_dict["goat"] = Zodiac_Goat()
all_zodiacs_dict["monkey"] = Zodiac_Monkey()
all_zodiacs_dict["rooster"] = Zodiac_Rooster()
all_zodiacs_dict["dog"] = Zodiac_Dog()
all_zodiacs_dict["pig"] = Zodiac_Pig()
all_zodiacs_dict["cat"] = Zodiac_Cat()

# --------------------------------------------------------------------------------------
# ALL TRIGRAMS LIST
# --------------------------------------------------------------------------------------
all_trigrams_list = []
all_trigrams_list.append(Trigram_Sky())
all_trigrams_list.append(Trigram_Lake())
all_trigrams_list.append(Trigram_Fire())
all_trigrams_list.append(Trigram_Thunder())
all_trigrams_list.append(Trigram_Wind())
all_trigrams_list.append(Trigram_Water())
all_trigrams_list.append(Trigram_Mountain())
all_trigrams_list.append(Trigram_Earth())

# --------------------------------------------------------------------------------------
# TRIGRAMS DICT
# --------------------------------------------------------------------------------------
all_trigrams_dict = {}
all_trigrams_dict["sky"] = Trigram_Sky()
all_trigrams_dict["lake"] = Trigram_Lake()
all_trigrams_dict["fire"] = Trigram_Fire()
all_trigrams_dict["thunder"] = Trigram_Thunder()
all_trigrams_dict["wind"] = Trigram_Wind()
all_trigrams_dict["water"] = Trigram_Water()
all_trigrams_dict["mountain"] = Trigram_Mountain()
all_trigrams_dict["earth"] = Trigram_Earth()
