class Zodiac:
    name = ""
    description = ""
    img_src = ""

    def __repr__(self):
        return repr((self.name, self.description))

    def __eq__(self, other):
        return self.name == other.name

class Trigram:
    name = ""
    description = ""
    img_src = ""

    def __repr__(self):
        return repr((self.name, self.description))

    def __eq__(self, other):
        return self.name == other.name

# --------------------------------------------------------------------------------------
# ZODIACS
# --------------------------------------------------------------------------------------

class Zodiac_Rat(Zodiac):
    name = "Rat"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/rat.jpg"

class Zodiac_Ox(Zodiac):
    name = "Ox"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/ox.jpg"

class Zodiac_Tiger(Zodiac):
    name = "Tiger"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/tiger.jpg"

class Zodiac_Rabbit(Zodiac):
    name = "Rabbit"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/rabbit.jpg"

class Zodiac_Dragon(Zodiac):
    name = "Dragon"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/dragon.jpg"

class Zodiac_Snake(Zodiac):
    name = "Snake"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/snake.jpg"

class Zodiac_Horse(Zodiac):
    name = "Horse"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/horse.jpg"

class Zodiac_Goat(Zodiac):
    name = "Goat"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/goat.jpg"

class Zodiac_Monkey(Zodiac):
    name = "Monkey"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/monkey.jpg"

class Zodiac_Rooster(Zodiac):
    name = "Rooster"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/rooster.jpg"

class Zodiac_Dog(Zodiac):
    name = "Dog"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/dog.jpg"

class Zodiac_Pig(Zodiac):
    name = "Pig"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/pig.jpg"


# --------------------------------------------------------------------------------------
# TRIGRAMS
# --------------------------------------------------------------------------------------

class Trigram_Sky(Trigram):
    name = "Sky"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/sky.jpg"

class Trigram_Lake(Trigram):
    name = "Lake"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/lake.jpg"

class Trigram_Flame(Trigram):
    name = "Flame"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/flame.jpg"

class Trigram_Thunder(Trigram):
    name = "Thunder"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/thunder.jpg"

class Trigram_Wind(Trigram):
    name = "Wind"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/wind.jpg"

class Trigram_Water(Trigram):
    name = "Water"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/water.jpg"

class Trigram_Mountain(Trigram):
    name = "Mountain"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/mountain.jpg"

class Trigram_Earth(Trigram):
    name = "Earth"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/zodiac/earth.jpg"

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

# --------------------------------------------------------------------------------------
# ALL TRIGRAMS LIST
# --------------------------------------------------------------------------------------
all_trigrams_list = []
all_trigrams_list.append(Trigram_Sky())
all_trigrams_list.append(Trigram_Lake())
all_trigrams_list.append(Trigram_Flame())
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
all_trigrams_dict["flame"] = Trigram_Flame()
all_trigrams_dict["thunder"] = Trigram_Thunder()
all_trigrams_dict["wind"] = Trigram_Wind()
all_trigrams_dict["water"] = Trigram_Water()
all_trigrams_dict["mountain"] = Trigram_Mountain()
all_trigrams_dict["earth"] = Trigram_Earth()
