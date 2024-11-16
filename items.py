class Item:
    name = ""
    description = ""
    cost = 3
    img_src = ""

    def __repr__(self):
        return repr((self.name, self.description))

    def __eq__(self, other):
        return self.name == other.name

# --------------------------------------------------------------------------------------
# ITEMS
# --------------------------------------------------------------------------------------

class Item_Bag(Item):
    name = "Bag"
    description = "Put a tile face-up on this bag. Draw another tile. On your turn you may draw this tile back instead of drawing from the wall."
    img_src = "/items/bag.png"

class Item_Called_Shot_Dragon(Item):
    name = "Called Shot: Dragon"
    description = "Choose a player and name a dragon tile. If that player has that tile, they must give it to you. Give them back a tile of your choice from your hand."
    img_src = "/items/called-shot-dragon.png"

class Item_Called_Shot_Wind(Item):
    name = "Called Shot: Wind"
    description = "Choose a player and name a wind tile. If that player has that tile, they must give it to you. Give them back a tile of your choice from your hand."
    img_src = "/items/called-shot-wind.png"

class Item_Called_Shot_Rank(Item):
    name = "Called Shot: Rank"
    description = "Choose a player and name a rank. If that player has a tile of that rank, they must give it to you. Give them back a tile of your choice from your hand."
    img_src = "/items/called-shot-rank.png"

class Item_Called_Shot_Suit(Item):
    name = "Called Shot: Suit"
    description = "Choose a player and name a suit. If that player has a tile of that suit, they must give it to you. Give them back a tile of your choice from your hand."
    img_src = "/items/called-shot-suit.png"

class Item_Controlled_Chaos(Item):
    name = "Controlled Chaos"
    description = "Take a random tile from an opponent's hand. Give them a tile from your hand."
    img_src = "/items/controlled-chaos.png"

class Item_Disguise(Item):
    name = "Disguise"
    description = "Change the suit of a tile in your hand."
    img_src = "/items/disguise.png"

class Item_Dumpster_Diver(Item):
    name = "Dumpster Diver"
    description = "Take any revealed discarded tile. Then discard a tile at random from your hand."
    img_src = "/items/dumpster-diver.png"

class Item_Equity(Item):
    name = "Equity"
    description = "Roll a D6, then decide whether all players gain or lose that amount of money."
    img_src = "/items/equity.png"

class Item_Golden_Compass(Item):
    name = "Golden Compass"
    description = "Select your seat wind. All players orient to your wind."
    img_src = "/items/golden-compass.png"

class Item_Grave_Dig(Item):
    name = "Grave Dig"
    description = "Draw a tile from the dead wall. Then discard a tile to the back of the dead wall."
    img_src = "/items/grave-dig.png"

class Item_Literally_Gambling(Item):
    name = "Literally Gambling"
    description = "You may roll up to three D6.  Each roll costs $1.  On an even roll you gain that much money.  On an odd roll you lose that much money."
    img_src = "/items/literally-gambling.png"

class Item_Mahjongkers_Dilemma(Item):
    name = "Mahjongker's Dilemma"
    description = "Select another player.  You both lose $1.  There is a prize of $6, and you both secretly choose to split or steal.  This is resolved just like the prisoner’s dilemma."
    img_src = "/items/mahjongkers-dilemma.png"

class Item_Oracle(Item):
    name = "Oracle"
    description = "Look at the top tile of the wall. You may discard this tile (cannot be picked up)."
    img_src = "/items/oracle.png"

class Item_Perpendicularity(Item):
    name = "Perpendicularity"
    description = "Add an honor tile of your choice to your hand."
    img_src = "/items/perpendicularity.png"

class Item_Power_Hour_Bamboo(Item):
    name = "Power Hour: Bamboo"
    description = "Add a bamboo tile of your choice to your hand."
    img_src = "/items/power-hour-bamboo.png"

class Item_Power_Hour_Character(Item):
    name = "Power Hour: Character"
    description = "Add a character tile of your choice to your hand."
    img_src = "/items/power-hour-character.png"

class Item_Power_Hour_Circles(Item):
    name = "Power Hour: Circles"
    description = "Add a circle tile of your choice to your hand."
    img_src = "/items/power-hour-circles.png"

class Item_Splitter(Item):
    name = "Splitter"
    description = "You may split a ranked tile in two in half. e.g. 9 of bamboo ->  4 & 5 of bamboo.  You cannot split a 1."
    img_src = "/items/splitter.png"

class Item_Stun_Gun(Item):
    name = "Stun Gun"
    description = "Choose a player.  One random tile for that player is disabled until the end of their next turn.  It still counts towards hand size but otherwise does not exist, e.g. it cannot be used to pong, chi, or mahjong."
    img_src = "/items/stun-gun.png"

class Item_Take_2(Item):
    name = "Take 2"
    description = "Discard two tiles.  Then draw 2 tiles from the wall."
    img_src = "/items/take-2.png"

class Item_Trap_Card(Item):
    name = "Trap Card"
    description = "Name a specific tile.  If a player draws it, they must discard it."
    img_src = "/items/trap-card.png"

class Item_Upheaval(Item):
    name = "Upheaval"
    description = "Change the rank of one of your tiles into rank of your choice."
    img_src = "/items/upheaval.png"

class Item_Weather_Vane(Item):
    name = "Weather Vane"
    description = "Shift the seat winds clockwise or counterclockwise."
    img_src = "/items/weather-vane.png"

class Item_Handmaxxing(Item):
    name = "Handmaxxing"
    description = "Draw 4. Skip your draw phase for the rest of the round."
    img_src = "/items/handmaxxing.jpg"

class Item_12_Inch(Item):
    name = "12 Inch Barrel Revolver"
    description = "Choose a player.  A random mahjongker for that player is disabled for the rest of this round."
    img_src = "/items/12inch.png"

# --------------------------------------------------------------------------------------
# ALL ITEMS LIST
# --------------------------------------------------------------------------------------

all_items_list = []
all_items_list.append(Item_Bag())
all_items_list.append(Item_Called_Shot_Dragon())
all_items_list.append(Item_Called_Shot_Wind())
all_items_list.append(Item_Called_Shot_Rank())
all_items_list.append(Item_Called_Shot_Suit())
all_items_list.append(Item_Controlled_Chaos())
all_items_list.append(Item_Disguise())
all_items_list.append(Item_Dumpster_Diver())
all_items_list.append(Item_Equity())
# all_items_list.append(Item_Golden_Compass())
all_items_list.append(Item_Grave_Dig())
all_items_list.append(Item_Literally_Gambling())
all_items_list.append(Item_Mahjongkers_Dilemma())
all_items_list.append(Item_Oracle())
all_items_list.append(Item_Perpendicularity())
all_items_list.append(Item_Power_Hour_Bamboo())
all_items_list.append(Item_Power_Hour_Character())
all_items_list.append(Item_Power_Hour_Circles())
all_items_list.append(Item_Splitter())
all_items_list.append(Item_Stun_Gun())
all_items_list.append(Item_Take_2())
all_items_list.append(Item_Trap_Card())
all_items_list.append(Item_Upheaval())
all_items_list.append(Item_Weather_Vane())
all_items_list.append(Item_Handmaxxing())
all_items_list.append(Item_12_Inch())