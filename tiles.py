class Tile:
    rank = "1" # 1-9, red, green, white, east, south, west, north
    suit = "dot" # dot, bamboo, character, dragon, wind
    points = 5 # 5 for regular, 15 for dragon, 20 for wind
    img_src = ""

    def __init__(self, r, s, p, i):
        self.rank = r
        self.suit = s 
        self.points = p 
        self.img_src = i

    def __repr__(self):
        return repr((self.suit, self.rank, self.points))

    def __eq__(self, other_tile):
        return self.rank == other_tile.rank and self.suit == other_tile.suit

all_tiles = {"dot":{}, "bamboo":{}, "character":{}, "dragon":{}, "wind":{}}

for suit in ["dot", "bamboo", "character"]:
    for rank in range(1, 10):
        all_tiles[suit][str(rank)] = Tile(str(rank), suit, 5, "img/tiles/" + suit + "-" + str(rank) + ".jpg")

for rank in ["red", "white", "green"]:
    all_tiles["dragon"][rank] = Tile(rank, "dragon", 15, "img/tiles/" + "dragon" + "-" + rank + ".jpg")

for rank in ["east", "south", "west", "north"]:
    all_tiles["wind"][rank] = Tile(rank, "wind", 20, "img/tiles/" + "wind" + "-" + rank + ".jpg")