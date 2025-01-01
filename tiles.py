class Tile:
    rank = "1" # 1-9, red, green, white, east, south, west, north
    suit = "dot" # dot, bamboo, character, dragon, wind
    points = 5 # 5 for regular, 15 for dragon, 20 for wind
    modifier = "none" # none, gold 
    seal = "none" # none, thunder, sky, lake, mountain
    img_src = ""

    def __init__(self, r, s, p, m, se, i):
        self.rank = r
        self.suit = s 
        self.points = p 
        self.modifier = m
        self.seal = se
        self.img_src = i

    def __repr__(self):
        return repr((self.suit, self.rank, self.points))

    def __eq__(self, other_tile):
        return self.rank == other_tile.rank and self.suit == other_tile.suit and self.modifier == other_tile.modifier and self.seal == other_tile.seal

    def copy(self):
        return Tile(self.rank, self.suit, self.points, self.modifier, self.seal, self.img_src)

# regular tiles
all_tiles = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles[suit][str(rank)] = Tile(str(rank), suit, 5, "none", "none",  "/tiles/" + suit + "-" + str(rank) + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles["dragon"][rank] = Tile(rank, "dragon", 10, "none", "none", "/tiles/" + "dragon" + "-" + rank + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles["wind"][rank] = Tile(rank, "wind", 10, "none", "none", "/tiles/" + "wind" + "-" + rank + ".jpg")

# thunder tiles
all_tiles_thunder = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_thunder[suit][str(rank)] = Tile(str(rank), suit, 5, "none", "thunder", "/tiles/" + suit + "-" + str(rank) + "-" + "thunder" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_thunder["dragon"][rank] = Tile(rank, "dragon", 10, "none", "thunder", "/tiles/" + "dragon" + "-" + rank + "-" + "thunder" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_thunder["wind"][rank] = Tile(rank, "wind", 10, "none", "thunder", "/tiles/" + "wind" + "-" + rank + "-" + "thunder" + ".jpg")

# sky tiles
all_tiles_sky = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_sky[suit][str(rank)] = Tile(str(rank), suit, 20, "none", "sky", "/tiles/" + suit + "-" + str(rank) + "-" + "sky" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_sky["dragon"][rank] = Tile(rank, "dragon", 25, "none", "sky", "/tiles/" + "dragon" + "-" + rank + "-" + "sky" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_sky["wind"][rank] = Tile(rank, "wind", 25, "none", "sky", "/tiles/" + "wind" + "-" + rank + "-" + "sky" + ".jpg")

# lake tiles
all_tiles_lake = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_lake[suit][str(rank)] = Tile(str(rank), suit, 5, "none", "lake", "/tiles/" + suit + "-" + str(rank) + "-" + "lake" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_lake["dragon"][rank] = Tile(rank, "dragon", 10, "none", "lake", "/tiles/" + "dragon" + "-" + rank + "-" + "lake" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_lake["wind"][rank] = Tile(rank, "wind", 10, "none", "lake", "/tiles/" + "wind" + "-" + rank + "-" + "lake" + ".jpg")

# mountain tiles
all_tiles_mountain = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_mountain[suit][str(rank)] = Tile(str(rank), suit, 20, "none", "mountain", "/tiles/" + suit + "-" + str(rank) + "-" + "mountain" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_mountain["dragon"][rank] = Tile(rank, "dragon", 25, "none", "mountain", "/tiles/" + "dragon" + "-" + rank + "-" + "mountain" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_mountain["wind"][rank] = Tile(rank, "wind", 25, "none", "mountain", "/tiles/" + "wind" + "-" + rank + "-" + "mountain" + ".jpg")

# gold tiles
all_tiles_gold = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_gold[suit][str(rank)] = Tile(str(rank), suit, 5, "gold", "none", "/tiles/" + suit + "-" + str(rank) + "-" + "gold" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_gold["dragon"][rank] = Tile(rank, "dragon", 10, "gold", "none", "/tiles/" + "dragon" + "-" + rank + "-" + "gold" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_gold["wind"][rank] = Tile(rank, "wind", 10, "gold", "none", "/tiles/" + "wind" + "-" + rank + "-" + "gold" + ".jpg")

# golden thunder tiles
all_tiles_gold_thunder = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_gold_thunder[suit][str(rank)] = Tile(str(rank), suit, 5, "gold", "thunder", "/tiles/" + suit + "-" + str(rank) + "-" + "gold" + "-" + "thunder" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_gold_thunder["dragon"][rank] = Tile(rank, "dragon", 10, "gold", "thunder", "/tiles/" + "dragon" + "-" + rank + "-" + "gold" + "-" + "thunder" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_gold_thunder["wind"][rank] = Tile(rank, "wind", 10, "gold", "thunder", "/tiles/" + "wind" + "-" + rank + "-" + "gold" + "-" + "thunder" + ".jpg")

# golden sky tiles
all_tiles_gold_sky = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_gold_sky[suit][str(rank)] = Tile(str(rank), suit, 20, "gold", "sky", "/tiles/" + suit + "-" + str(rank) + "-" + "gold" + "-" + "sky" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_gold_sky["dragon"][rank] = Tile(rank, "dragon", 25, "gold", "sky", "/tiles/" + "dragon" + "-" + rank + "-" + "gold" + "-" + "sky" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_gold_sky["wind"][rank] = Tile(rank, "wind", 25, "gold", "sky", "/tiles/" + "wind" + "-" + rank + "-" + "gold" + "-" + "sky" + ".jpg")

# golden lake tiles
all_tiles_gold_lake = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_gold_lake[suit][str(rank)] = Tile(str(rank), suit, 5, "gold", "lake", "/tiles/" + suit + "-" + str(rank) + "-" + "gold" + "-" + "lake" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_gold_lake["dragon"][rank] = Tile(rank, "dragon", 10, "gold", "lake", "/tiles/" + "dragon" + "-" + rank + "-" + "gold" + "-" + "lake" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_gold_lake["wind"][rank] = Tile(rank, "wind", 10, "gold", "lake", "/tiles/" + "wind" + "-" + rank + "-" + "gold" + "-" + "lake" + ".jpg")

# golden mountain tiles
all_tiles_gold_mountain = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles_gold_mountain[suit][str(rank)] = Tile(str(rank), suit, 20, "gold", "mountain", "/tiles/" + suit + "-" + str(rank) + "-" + "gold" + "-" + "mountain" + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles_gold_mountain["dragon"][rank] = Tile(rank, "dragon", 25, "gold", "mountain", "/tiles/" + "dragon" + "-" + rank + "-" + "gold" + "-" + "mountain" + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles_gold_mountain["wind"][rank] = Tile(rank, "wind", 25, "gold", "mountain", "/tiles/" + "wind" + "-" + rank + "-" + "gold" + "-" + "mountain" + ".jpg")