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
    cost = 2
    img_src = "/items/bag.jpg"

class Item_Called_Shot_Dragon(Item):
    name = "Called Shot: Dragon"
    description = "Choose a player. If that player has a dragon tile, they must give it to you. You give them back a tile of your choice from your hand."
    cost = 2
    img_src = "/items/called-shot-dragon.jpg"

class Item_Called_Shot_Wind(Item):
    name = "Called Shot: Wind"
    description = "Choose a player. If that player has a wind tile, they must give it to you. You give them back a tile of your choice from your hand."
    cost = 2
    img_src = "/items/called-shot-wind.jpg"

class Item_Called_Shot_Rank(Item):
    name = "Called Shot: Rank"
    description = "Choose a player and name a group, low(1-3), mid(4-6), or high(7-9). If that player has a tile within that group, they must give you a tile matching that rank. You give them back a tile of your choice from your hand."
    cost = 2
    img_src = "/items/called-shot-rank.jpg"

class Item_Called_Shot_Suit(Item):
    name = "Called Shot: Suit"
    description = "Choose a player and name a suit. If that player has a tile with that suit they must give you a tile matching that suit. You give them back a tile of your choice from your hand."
    cost = 2
    img_src = "/items/called-shot-suit.jpg"

class Item_Controlled_Chaos(Item):
    name = "Controlled Chaos"
    description = "Take a random tile from an opponent's hand. Give them a tile from your hand."
    cost = 2
    img_src = "/items/controlled-chaos.jpg"

class Item_Disguise(Item):
    name = "Disguise"
    description = "Change the suit of a tile in your hand."
    cost = 6
    img_src = "/items/disguise.jpg"

class Item_Dumpster_Diver(Item):
    name = "Dumpster Diver"
    description = "Take any revealed discarded tile. Then discard a tile at random from your hand."
    cost = 3
    img_src = "/items/dumpster-diver.jpg"

class Item_Equity(Item):
    name = "Equity"
    description = "Roll a D6, then decide whether all players gain or lose that amount of money."
    cost = 3
    img_src = "/items/equity.jpg"

class Item_Golden_Compass(Item):
    name = "Golden Compass"
    description = "Select your seat wind. All players orient to your wind."
    cost = 3
    img_src = "/items/golden-compass.jpg"

class Item_Grave_Dig(Item):
    name = "Grave Dig"
    description = "Draw a tile from the dead wall. Then discard a tile to the back of the dead wall."
    cost = 2
    img_src = "/items/grave-dig.jpg"

class Item_Literally_Gambling(Item):
    name = "Literally Gambling"
    description = "You may roll up to three D6.  Each roll costs $1.  On an even roll you gain that much money.  On an odd roll you lose that much money."
    cost = 3
    img_src = "/items/literally-gambling.jpg"

class Item_Mahjongkers_Dilemma(Item):
    name = "Mahjongker's Dilemma"
    description = "Select another player.  You both lose $1.  There is a prize of $6, and you both secretly choose to split or steal.  This is resolved just like the prisoner’s dilemma."
    cost = 1
    img_src = "/items/mahjongkers-dilemma.jpg"

class Item_Oracle(Item):
    name = "Oracle"
    description = "Look at the top 2 tiles of the wall, you may discard any number of these tiles (cannot be picked up)."
    cost = 3
    img_src = "/items/oracle.jpg"

class Item_Perpendicularity(Item):
    name = "Perpendicularity"
    description = "Add a Honor Tile to your hand. You can only use this when you current hand size <= max hand size."
    cost = 4
    img_src = "/items/perpendicularity.jpg"

class Item_Power_Hour_Bamboo(Item):
    name = "Power Hour: Bamboo"
    description = "Add a bamboo tile of your choice to your hand."
    cost = 4
    img_src = "/items/power-hour-bamboo.jpg"

class Item_Power_Hour_Character(Item):
    name = "Power Hour: Character"
    description = "Add a character tile of your choice to your hand."
    cost = 4
    img_src = "/items/power-hour-character.jpg"

class Item_Power_Hour_Dots(Item):
    name = "Power Hour: Dots"
    description = "Add a circle tile of your choice to your hand."
    cost = 4
    img_src = "/items/power-hour-dots.jpg"

class Item_Splitter(Item):
    name = "Splitter"
    description = "You may split a ranked tile in two in half. e.g. 9 of bamboo ->  4 & 5 of bamboo.  You cannot split a 1."
    cost = 4
    img_src = "/items/splitter.jpg"

class Item_Stun_Gun(Item):
    name = "Stun Gun"
    description = "Choose a player. They cannot act until the end of their next turn."
    cost = 1
    img_src = "/items/stun-gun.jpg"

class Item_Take_2(Item):
    name = "Take 2"
    description = "Discard two tiles.  Then draw 2 tiles from the wall."
    cost = 3
    img_src = "/items/take-2.jpg"

class Item_Trap_Card(Item):
    name = "Trap Card"
    description = "Name a specific tile.  If a player draws it, they must discard it."
    cost = 2
    img_src = "/items/trap-card.jpg"

class Item_Upheaval(Item):
    name = "Upheaval"
    description = "Change the rank of one of your tiles into rank of your choice."
    cost = 6
    img_src = "/items/upheaval.jpg"

class Item_Weather_Vane(Item):
    name = "Weather Vane"
    description = "Select your seat wind. All players orient to your wind."
    cost = 2
    img_src = "/items/weather-vane.jpg"

class Item_Handmaxxing(Item):
    name = "Handmaxxing"
    description = "Draw 4. Skip your draw phase for the rest of the round."
    cost = 4
    img_src = "/items/handmaxxing.jpg"

class Item_12_Inch(Item):
    name = "12 Inch Barrel Revolver"
    description = "Choose a player.  A random mahjongker for that player is disabled for the rest of this round."
    cost = 2
    img_src = "/items/12inch.jpg"

class Item_Sleight_Of_Han(Item):
    name = "Sleight of Han"
    description = "Steal a random item from another player."
    cost = 3
    img_src = "/items/sleight-of-han.jpg"

class Item_Black_Eyed_Peas(Item):
    name = "Black Eyed Peas"
    description = "Combine two tiles of the same suit. Then split them down the middle. (3+7 -> 5,5)."
    cost = 4
    img_src = "/items/black-eyed-peas.jpg"

class Item_Mutually_Assured_Destruction(Item):
    name = "Mutually Assured Destruction"
    description = "Select a player.  Randomly discard tiles up to your current hand size.  The chosen player must also randomly discard up to that many tiles as well. Both players draw the discarded amount back."
    cost = 3
    img_src = "/items/mutually-assured-destruction.jpg"

class Item_Re_Suitbaru(Item):
    name = "Re: Suitbaru"
    description = "Reroll the suit of a tile in your hand."
    cost = 2
    img_src = "/items/re-suitbaru.jpg"

class Item_Re_Sident_Evil(Item):
    name = "Re: Sident Evil"
    description = "Reroll an honor tile in your hand, within its category (dragon, wind)."
    cost = 2
    img_src = "/items/re-sident-evil.jpg"

class Item_Re_Surrection(Item):
    name = "Re: Surrection"
    description = "Reroll the rank of a tile in your hand.  Pick low (1-3), mid (4-6), or high (7-9)."
    cost = 2
    img_src = "/items/re-surrection.jpg"

class Item_Piggy_Bank(Item):
    name = "Piggy Bank"
    description = "This item gains $1 if empty. Pick break or wait. If wait, the next piggy bank you get is worth 2x.  If break, get the value of the piggy bank and then set it back to 0."
    cost = 2
    img_src = "/items/piggy-bank.jpg"

class Item_Pivoter(Item):
    name = "Pivoter"
    description = "Discard a random tile in your hand.  The next time you draw you get a copy of the drawn tile."
    cost = 2
    img_src = "/items/pivoter.jpg"

class Item_Well_Laid_Plans(Item):
    name = "Well Laid Plans"
    description = "Draw a tile and then place a tile from your hand on top of the deck."
    cost = 2
    img_src = "/items/well-laid-plans.jpg"

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
# all_items_list.append(Item_Perpendicularity())
# all_items_list.append(Item_Power_Hour_Bamboo())
# all_items_list.append(Item_Power_Hour_Character())
# all_items_list.append(Item_Power_Hour_Dots())
all_items_list.append(Item_Splitter())
all_items_list.append(Item_Stun_Gun())
all_items_list.append(Item_Take_2())
# all_items_list.append(Item_Trap_Card())
all_items_list.append(Item_Upheaval())
# all_items_list.append(Item_Weather_Vane())
all_items_list.append(Item_Handmaxxing())
all_items_list.append(Item_12_Inch())
all_items_list.append(Item_Sleight_Of_Han())
all_items_list.append(Item_Black_Eyed_Peas())
all_items_list.append(Item_Mutually_Assured_Destruction())
all_items_list.append(Item_Re_Suitbaru())
all_items_list.append(Item_Re_Sident_Evil())
all_items_list.append(Item_Re_Surrection())
all_items_list.append(Item_Piggy_Bank())
all_items_list.append(Item_Pivoter())
all_items_list.append(Item_Well_Laid_Plans())

# --------------------------------------------------------------------------------------
# ITEM DICT
# --------------------------------------------------------------------------------------
all_items_dict = {}
all_items_dict["bag"] = Item_Bag()
all_items_dict["called-shot-dragon"] = Item_Called_Shot_Dragon()
all_items_dict["called-shot-wind"] = Item_Called_Shot_Wind()
all_items_dict["called-shot-rank"] = Item_Called_Shot_Rank()
all_items_dict["called-shot-suit"] = Item_Called_Shot_Suit()
all_items_dict["controlled-chaos"] = Item_Controlled_Chaos()
all_items_dict["disguise"] = Item_Disguise()
all_items_dict["dumpster-diver"] = Item_Dumpster_Diver()
all_items_dict["equity"] = Item_Equity()
all_items_dict["grave-dig"] = Item_Grave_Dig()
all_items_dict["literally-gambling"] = Item_Literally_Gambling()
all_items_dict["mahjongkers-dilemma"] = Item_Mahjongkers_Dilemma()
all_items_dict["oracle"] = Item_Oracle()
# all_items_dict["perpendicularity"] = Item_Perpendicularity()
# all_items_dict["power-hour-bamboo"] = Item_Power_Hour_Bamboo()
# all_items_dict["power-hour-character"] = Item_Power_Hour_Character()
# all_items_dict["power-hour-dots"] = Item_Power_Hour_Dots()
all_items_dict["splitter"] = Item_Splitter()
all_items_dict["stun-gun"] = Item_Stun_Gun()
all_items_dict["take-2"] = Item_Take_2()
# all_items_dict["trap-card"] = Item_Trap_Card()
all_items_dict["upheaval"] = Item_Upheaval()
# all_items_dict["weather-vane"] = Item_Weather_Vane()
all_items_dict["handmaxxing"] = Item_Handmaxxing()
all_items_dict["12inch"] = Item_12_Inch()
all_items_dict["sleight-of-han"] = Item_Sleight_Of_Han()
all_items_dict["black-eyed-peas"] = Item_Black_Eyed_Peas()
all_items_dict["mutually-assured-destruction"] = Item_Mutually_Assured_Destruction()
all_items_dict["re-suitbaru"] = Item_Re_Suitbaru()
all_items_dict["re-sident-evil"] = Item_Re_Sident_Evil()
all_items_dict["re-surrection"] = Item_Re_Surrection()
all_items_dict["piggy-bank"] = Item_Piggy_Bank()
all_items_dict["pivoter"] = Item_Pivoter()
all_items_dict["well-laid-plans"] = Item_Well_Laid_Plans()

# --------------------------------------------------------------------------------------
# ITEM NAME DICT
# --------------------------------------------------------------------------------------
all_item_names_dict = {}
all_item_names_dict["Bag"] = Item_Bag()
all_item_names_dict["Called Shot: Dragon"] = Item_Called_Shot_Dragon()
all_item_names_dict["Called Shot: Wind"] = Item_Called_Shot_Wind()
all_item_names_dict["Called Shot: Rank"] = Item_Called_Shot_Rank()
all_item_names_dict["Called Shot: Suit"] = Item_Called_Shot_Suit()
all_item_names_dict["Controlled Chaos"] = Item_Controlled_Chaos()
all_item_names_dict["Disguise"] = Item_Disguise()
all_item_names_dict["Dumpster Diver"] = Item_Dumpster_Diver()
all_item_names_dict["Equity"] = Item_Equity()
all_item_names_dict["Grave Dig"] = Item_Grave_Dig()
all_item_names_dict["Literally Gambling"] = Item_Literally_Gambling()
all_item_names_dict["Mahjongker's Dilemma"] = Item_Mahjongkers_Dilemma()
all_item_names_dict["Oracle"] = Item_Oracle()
# all_item_names_dict["Perpendicularity"] = Item_Perpendicularity()
# all_item_names_dict["Power Hour: Bamboo"] = Item_Power_Hour_Bamboo()
# all_item_names_dict["Power Hour: Character"] = Item_Power_Hour_Character()
# all_item_names_dict["Power Hour: Dots"] = Item_Power_Hour_Dots()
all_item_names_dict["Splitter"] = Item_Splitter()
all_item_names_dict["Stun Gun"] = Item_Stun_Gun()
all_item_names_dict["Take 2"] = Item_Take_2()
# all_item_names_dict["Trap Card"] = Item_Trap_Card()
all_item_names_dict["Upheaval"] = Item_Upheaval()
# all_item_names_dict["Weather Vane"] = Item_Weather_Vane()
all_item_names_dict["Handmaxxing"] = Item_Handmaxxing()
all_item_names_dict["12 Inch Barrel Revolver"] = Item_12_Inch()
all_item_names_dict["Sleight Of Han"] = Item_Sleight_Of_Han()
all_item_names_dict["Black Eyed Peas"] = Item_Black_Eyed_Peas()
all_item_names_dict["Mutually Assured Destruction"] = Item_Mutually_Assured_Destruction()
all_item_names_dict["Re: Suitbaru"] = Item_Re_Suitbaru()
all_item_names_dict["Re: Sident Evil"] = Item_Re_Sident_Evil()
all_item_names_dict["Re: Surrection"] = Item_Re_Surrection()
all_item_names_dict["Piggy Bank"] = Item_Piggy_Bank()
all_item_names_dict["Pivoter"] = Item_Pivoter()
all_item_names_dict["Well Laid Plans"] = Item_Well_Laid_Plans()
