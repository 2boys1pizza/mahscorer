import flet as ft
import time
import random
from items import *
from mahscorer import *
from deck_modifiers import *

# -------------------------------------------------------------
# GLOBAL VARS
# -------------------------------------------------------------

# global scoring
HAND_TYPE_UPGRADE_MULT = 1.5
HAND_SIZE_COSTS = [6,11,16,26]
MULLIGAN_COSTS = [1,4,7,10]
SEQUENCE_UPGRADE_COST = 2
TRIPLET_UPGRADE_COST = 2
HALF_FLUSH_UPGRADE_COST = 2
FLUSH_UPGRADE_COST = 2
AVATAR_UPGRADE_COST = 6
SEQUENCE_UPGRADE_COSTS = [2,3,4,5,6]
TRIPLET_UPGRADE_COSTS = [2,3,4,5,6]
HALF_FLUSH_UPGRADE_COSTS = [2,3,4,5,6]
FLUSH_UPGRADE_COSTS = [2,3,4,5,6]
AVATAR_UPGRADE_COSTS = [6,9,12,15,18]
MAHJONGKERS_REROLL_COST = 2
ZODIAC_COST = 3
TRIGRAM_COST = 2
ITEM_COST = 2
MAX_NUM_MAHJONGKERS = 5
MAX_NUM_ITEMS = 2
SEQUENCE_UPGRADE_AMOUNT = 0.1
TRIPLET_UPGRADE_AMOUNT = 0.15
HALF_FLUSH_UPGRADE_AMOUNT = 0.15
FLUSH_UPGRADE_AMOUNT = 0.2
SHOP_MAHJONGKER_RARITIES = ["common", "uncommon", "rare"]
SHOP_MAHJONGKER_RARITY_PROBABILITIES = {0:[95, 5, 0], 1:[87, 13, 0], 2:[72, 25, 3], 3:[57, 35, 8], 4:[40, 45, 15]}
ITEM_RARITIES = ["piggy", "common", "uncommon", "rare"]
ITEM_RARITY_PROBABILITY = [13, 65, 17, 5]
START_MONEY = 2
ROUND_UBI = [0,0,0,0,0]

# hands
sequence_hand_level = 0
triplet_hand_level = 0
half_flush_hand_level = 0
flush_hand_level = 0
hand_size_level = 0
sequence_hand_mult = 1.1
triplet_hand_mult = 1.3
half_flush_hand_mult = 1.3
flush_hand_mult = 1.5

# stats
money = START_MONEY
total_score = 0
hand_size = 10
money_text = ft.Text(money, size=80)
score_text = ft.Text(total_score, size=80)
hand_size_text = ft.Text(hand_size, size=80)
score_adjust_tf = []
money_adjust_tf = []
sequence_mult_text = []
triplet_mult_text = []
half_flush_mult_text = []
flush_mult_text = []

# inventory
my_mahjongkers = []
my_items = []
filtered_mahjongkers_list = []
all_mahjongker_text = []
all_mahjongkers_containers = []
my_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
my_item_text = ft.Text("", color=ft.colors.WHITE)
mahjongker_filter = ""
my_mahjongker_grid = ft.GridView(
    # expand=1,
    height=100,
    width=400,
    runs_count=5,
    max_extent=150,
    child_aspect_ratio=1.0,
    spacing=15,
    run_spacing=15,
)
my_items_grid = ft.GridView(
    # expand=1,
    height=100,
    width=400,
    runs_count=5,
    max_extent=150,
    child_aspect_ratio=1.0,
    spacing=15,
    run_spacing=15,
)
all_mahjongker_grid = ft.GridView(
    # expand=1,
    height=100,
    width=400,
    runs_count=5,
    max_extent=150,
    child_aspect_ratio=1.0,
    spacing=15,
    run_spacing=15,
)
my_jongkers_panel = ft.ExpansionPanel()
aycker_text = ft.Text("AYCker value: 0", size=40)
pingker_text = ft.Text("Pingker value: 0", size=40)
kingkongker_text = ft.Text("KingKongker value: 0", size=40)
meldker_text = ft.Text("Meldker value: 0", size=40)
fuckgker_text = ft.Text("Fuckgker value: 0", size=40)
suckgker_text = ft.Text("Suckgker value: 0", size=40)
speedker_text = ft.Text("Speedker value: 30", size=40)
empressker_text = ft.Text("Empressker value: 0", size=40)
laobanker_text = ft.Text("Laobanker value: 0", size=40)
spoilker_text = ft.Text("Spoilker value: 50", size=40)
donnerker_text = ft.Text("Donnerker value: 0", size=40)
doraker_text = ft.Text("Doraker value: 0", size=40)
odiumker_text = ft.Text("Odiumker value: 0", size=40)
bamenker_text = ft.Text("Bamenker value: 0", size=40)
denker_text = ft.Text("Denker value: 0", size=40)
chenker_text = ft.Text("Chenker value: 0", size=40)
tanavastker_text = ft.Text("Tanavastker value: 0", size=40)
jackblackgker_text = ft.Text("JackBlackgker value: 0", size=40)
lake_text = ft.Text("Lake value: 0", size=40)
mahjong_pts_text = ft.Text("Mahjong Pts: 0 pts", size=20)
mahjong_money_text = ft.Text("Mahjong Money: $ 0", size=20)

# scorer
selected_tiles = []
current_hand = Hand()
table_wind = all_tiles["wind"]["east"]
seat_wind = all_tiles["wind"]["east"]
hand_score_text = ft.Text(f"Score: 0", size=20)
add_tiles_panel = []
tile_radio = []
modifier_radio = []
seal_radio = []
all_tile_grid = []
selected_tiles_row = []
all_tile_containers = []
other_scoring_panel = []
scoring_tiles_row = []
current_hand_panel = []
tot_score = 0
scored_money = 0
lake_adjuster = []
mahjong_pts_adjuster = []
mahjong_money_adjuster = []

# shop
shop_round = 0
refresh_shop_button = []
shop_row = []
my_mahjongkers_shop_row = []
item_row = []
item_pack_row = []
my_items_shop_row = []
shop_zodiac_row = []
shop_trigram_row = []
shop_mahjongker_text = ""
shop_sell_mahjongker_text = ""
shop_item_text = ""
shop_zodiac_text = ""
shop_trigram_text = ""
reroll_cost = MAHJONGKERS_REROLL_COST
reroll_item_cost = 1
reroll_zodiac_cost = 3
reroll_trigram_cost = 2
current_zodiac_cost = 3
current_trigram_cost = 2
shop_money_text = ft.Text("", color=ft.colors.WHITE)
shop_tier_text = ft.Text("", color=ft.colors.WHITE)
hand_size_upgrade_button = []
shop_selected_i = []
item_selected = []
zodiac_selected = []
trigram_selected = []
sequence_button = []
sequence_current_text = []
triplet_button = []
triplet_current_text = []
half_flush_button = []
half_flush_current_text = []
flush_button = []
flush_current_text = []
avatar_button = []
hand_upgrade_enabled = True

shop_info_column = []
trigram_pack_info_column = []
item_pack_info_column = []
initial_mahjongker_info_column = []

zodiac_row = []
zodiac_text = []
trigram_row = []
trigram_text = []
initial_mahjongkers_row = []
initial_mahjongker_text = ""
uncommon_mahjongkers_row = []
uncommon_mahjongker_text = ""
rare_mahjongkers_row = []
rare_mahjongker_text = ""


#------------------------------------------
# CUSTOM CLASSES 
#------------------------------------------
# this shit dont work lol
class MahjongkerTooltip(ft.Tooltip):
    def __init__(self, mahjongker):
        super().__init__()
        self.message=mahjongker.description,
        self.padding=20,
        self.border_radius=10,
        self.text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
        self.gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.Alignment(0.8, 1),
            colors=[
                "0xff1f005c",
                "0xff5b0060",
                "0xff870160",
                "0xffac255e",
                "0xffca485c",
                "0xffe16b5c",
                "0xfff39060",
                "0xffffb56b",
            ],
            tile_mode=ft.GradientTileMode.MIRROR,
        )

def main(page: ft.Page):
    # -------------------------------------------------------------
    # NAVBAR FUNC
    # -------------------------------------------------------------
    def go_to_page(e):
        if e.control.selected_index == 0:
            page.go("/stats")
        elif e.control.selected_index == 1:
            page.go("/inventory")
        elif e.control.selected_index == 2:
            page.go("/scorer")
        else:
            page.go("/shop")

    # -------------------------------------------------------------
    # STATS FUNC
    # -------------------------------------------------------------

    def increment_money(e):
        global money
        global money_text
        money += 1
        money_text.value = str(money)
        page.update()

    def decrement_money(e):
        global money
        global money_text
        money -= 1
        money_text.value = str(money)
        page.update()

    def adjust_score(e):
        global total_score
        global score_text
        print(float(score_adjust_tf.value))
        total_score = float(score_adjust_tf.value)
        score_text.value = total_score
        page.update()

    def adjust_money(e):
        global money
        global money_text
        money = int(money_adjust_tf.value)
        money_text.value = str(money)
        page.update()

    def increment_hand_size(e):
        global hand_size
        global hand_size_level
        global hand_size_text
        hand_size = hand_size + 1
        hand_size_level = hand_size_level + 1
        hand_size_text.value = str(hand_size)
        page.update()

    def decrement_hand_size(e):
        global hand_size
        global hand_size_level
        global hand_size_text
        hand_size = max(10, hand_size - 1)
        hand_size_level = max(0, hand_size_level - 1)
        hand_size_text.value = str(hand_size)
        page.update()

    def increment_sequence_mult(e):
        global sequence_hand_mult
        global sequence_mult_text
        sequence_hand_mult = round(sequence_hand_mult + SEQUENCE_UPGRADE_AMOUNT, 2)
        print(sequence_hand_mult)
        sequence_mult_text.value = str(sequence_hand_mult)
        page.update()

    def increment_triplet_mult(e):
        global triplet_hand_mult
        global triplet_mult_text
        triplet_hand_mult = round(triplet_hand_mult + TRIPLET_UPGRADE_AMOUNT, 2)
        triplet_mult_text.value = str(triplet_hand_mult)
        page.update()

    def increment_half_flush_mult(e):
        global half_flush_hand_mult
        global half_flush_mult_text
        half_flush_hand_mult = round(half_flush_hand_mult + HALF_FLUSH_UPGRADE_AMOUNT, 2)
        half_flush_mult_text.value = str(half_flush_hand_mult)
        page.update()

    def increment_flush_mult(e):
        global flush_hand_mult
        global flush_mult_text
        flush_hand_mult = round(flush_hand_mult + FLUSH_UPGRADE_AMOUNT, 2)
        flush_mult_text.value = str(flush_hand_mult)
        page.update()

    def decrement_sequence_mult(e):
        global sequence_hand_mult
        global sequence_mult_text
        sequence_hand_mult = round(sequence_hand_mult - SEQUENCE_UPGRADE_AMOUNT, 2)
        sequence_mult_text.value = str(sequence_hand_mult)
        page.update()

    def decrement_triplet_mult(e):
        global triplet_hand_mult
        global triplet_mult_text
        triplet_hand_mult = round(triplet_hand_mult - TRIPLET_UPGRADE_AMOUNT, 2)
        triplet_mult_text.value = str(triplet_hand_mult)
        page.update()


    def decrement_half_flush_mult(e):
        global half_flush_hand_mult
        global half_flush_mult_text
        half_flush_hand_mult = round(half_flush_hand_mult - HALF_FLUSH_UPGRADE_AMOUNT, 2)
        half_flush_mult_text.value = str(half_flush_hand_mult)
        page.update()

    def decrement_flush_mult(e):
        global flush_hand_mult
        global flush_mult_text
        flush_hand_mult = round(flush_hand_mult - FLUSH_UPGRADE_AMOUNT, 2)
        flush_mult_text.value = str(flush_hand_mult)
        page.update()

    # -------------------------------------------------------------
    # INVENTORY FUNC
    # -------------------------------------------------------------

    def handle_add_mahjongker_select(e):
        global my_jongkers_panel
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        all_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def handle_remove_mahjongker_select(e):
        global my_mahjongker_text
        global all_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        if len(my_jongkers_panel.content.controls) >= 3:
            del my_jongkers_panel.content.controls[1]
        page.update()

    def handle_remove_item_select(e):
        global my_item_text
        global all_item_text
        item_name = e.control.image.src.split("/")[2].split(".")[0]
        my_item_text.value = all_items_dict[item_name].name
        print(all_items_dict[item_name].name)
        if len(my_items_panel.content.controls) >= 3:
            del my_items_panel.content.controls[1]
        page.update()

    def handle_AYCker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global aycker_text
        # Add UI to increase/decrease value of ayceker
        aycker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "AYCker":
                aycker = mahjongker
                break
        aycker_text.value = f"AYCker value: {aycker.point_value}"
        upgrade_row = ft.Row([
            aycker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_aycker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_aycker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_aycker_score(e):
        global aycker_text
        aycker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "AYCker":
                aycker = mahjongker
                break
        aycker.point_value = aycker.point_value + 7
        aycker_text.value = f"AYCker value: {aycker.point_value}"
        page.update()

    def decrement_aycker_score(e):
        global aycker_text
        aycker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "AYCker":
                aycker = mahjongker
                break
        aycker.point_value = max(0, aycker.point_value - 7)
        aycker_text.value = f"AYCker value: {aycker.point_value}"
        page.update()

    def handle_pingker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global pingker_text
        # Add UI to increase/decrease value of ayceker
        pingker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Pingker":
                pingker = mahjongker
                break
        pingker_text.value = f"Pingker value: {pingker.point_value}"
        upgrade_row = ft.Row([
            pingker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_pingker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_pingker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_pingker_score(e):
        global pingker_text
        pingker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Pingker":
                pingker = mahjongker
                break
        pingker.point_value = pingker.point_value + 7
        pingker_text.value = f"Pingker value: {pingker.point_value}"
        page.update()

    def decrement_pingker_score(e):
        global pingker_text
        pingker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Pingker":
                pingker = mahjongker
                break
        pingker.point_value = max(0, pingker.point_value - 7)
        pingker_text.value = f"Pingker value: {pingker.point_value}"
        page.update()

    def handle_kingkongker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global kingkongker_text
        # Add UI to increase/decrease value of ayceker
        kingkongker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "KingKongker":
                kingkongker = mahjongker
                break
        kingkongker_text.value = f"KingKongker value: {kingkongker.point_value}"
        upgrade_row = ft.Row([
            kingkongker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_kingkongker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_kingkongker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_kingkongker_score(e):
        global kingkongker_text
        kingkongker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "KingKongker":
                kingkongker = mahjongker
                break
        kingkongker.point_value = kingkongker.point_value + 14
        kingkongker_text.value = f"KingKongker value: {kingkongker.point_value}"
        page.update()

    def decrement_kingkongker_score(e):
        global kingkongker_text
        kingkongker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "KingKongker":
                kingkongker = mahjongker
                break
        kingkongker.point_value = max(0, kingkongker.point_value - 14)
        kingkongker_text.value = f"KingKongker value: {kingkongker.point_value}"
        page.update()

    def handle_meldker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global meldker_text
        # Add UI to increase/decrease value of ayceker
        meldker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Meldker":
                meldker = mahjongker
                break
        meldker_text.value = f"Meldker value: {meldker.point_value}"
        upgrade_row = ft.Row([
            meldker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_meldker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_meldker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_meldker_score(e):
        global meldker_text
        meldker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Meldker":
                meldker = mahjongker
                break
        meldker.point_value = meldker.point_value + 15
        meldker_text.value = f"Meldker value: {meldker.point_value}"
        page.update()

    def decrement_meldker_score(e):
        global meldker_text
        meldker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Meldker":
                meldker = mahjongker
                break
        meldker.point_value = max(0, meldker.point_value - 15)
        meldker_text.value = f"Meldker value: {meldker.point_value}"
        page.update()

    def handle_fuckgker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global fuckgker_text
        # Add UI to increase/decrease value of ayceker
        fuckgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Fuckgker":
                fuckgker = mahjongker
                break
        fuckgker_text.value = f"Fuckgker value: {fuckgker.point_value}"
        upgrade_row = ft.Row([
            fuckgker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_fuckgker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_fuckgker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_fuckgker_score(e):
        global fuckgker_text
        fuckgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Fuckgker":
                fuckgker = mahjongker
                break
        fuckgker.point_value = fuckgker.point_value + 5
        fuckgker_text.value = f"Fuckgker value: {fuckgker.point_value}"
        page.update()

    def decrement_fuckgker_score(e):
        global fuckgker_text
        fuckgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Fuckgker":
                fuckgker = mahjongker
                break
        fuckgker.point_value = max(0, fuckgker.point_value - 5)
        fuckgker_text.value = f"Fuckgker value: {fuckgker.point_value}"
        page.update()

    def handle_suckgker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global suckgker_text
        # Add UI to increase/decrease value of ayceker
        suckgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Suckgker":
                suckgker = mahjongker
                break
        suckgker_text.value = f"Suckgker value: {suckgker.point_value}"
        upgrade_row = ft.Row([
            suckgker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_suckgker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_suckgker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_suckgker_score(e):
        global suckgker_text
        suckgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Suckgker":
                suckgker = mahjongker
                break
        suckgker.point_value = suckgker.point_value + 5
        suckgker_text.value = f"Suckgker value: {suckgker.point_value}"
        page.update()

    def decrement_suckgker_score(e):
        global suckgker_text
        suckgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Suckgker":
                suckgker = mahjongker
                break
        suckgker.point_value = max(0, suckgker.point_value - 5)
        suckgker_text.value = f"Suckgker value: {suckgker.point_value}"
        page.update()

    def handle_speedker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global speedker_text
        # Add UI to increase/decrease value of ayceker
        speedker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Speedker":
                speedker = mahjongker
                break
        speedker_text.value = f"Speedker value: {speedker.point_value}"
        upgrade_row = ft.Row([
            speedker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_speedker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_speedker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_speedker_score(e):
        global speedker_text
        speedker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Speedker":
                speedker = mahjongker
                break
        speedker.point_value = speedker.point_value + 15
        speedker_text.value = f"Speedker value: {speedker.point_value}"
        page.update()

    def decrement_speedker_score(e):
        global speedker_text
        speedker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Speedker":
                speedker = mahjongker
                break
        speedker.point_value = max(0, speedker.point_value - 15)
        speedker_text.value = f"Speedker value: {speedker.point_value}"
        page.update()

    def handle_empressker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global empressker_text
        # Add UI to increase/decrease value of ayceker
        empressker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Empressker":
                empressker = mahjongker
                break
        empressker_text.value = f"Empressker value: {empressker.point_value}"
        upgrade_row = ft.Row([
            empressker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_empressker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_empressker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_empressker_score(e):
        global empressker_text
        empressker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Empressker":
                empressker = mahjongker
                break
        empressker.point_value = empressker.point_value + 7
        empressker_text.value = f"Empressker value: {empressker.point_value}"
        page.update()

    def decrement_empressker_score(e):
        global empressker_text
        empressker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Empressker":
                empressker = mahjongker
                break
        empressker.point_value = max(0, empressker.point_value - 7)
        empressker_text.value = f"Empressker value: {empressker.point_value}"
        page.update()

    def handle_laobanker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global laobanker_text
        # Add UI to increase/decrease value of ayceker
        laobanker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Laobanker":
                laobanker = mahjongker
                break
        laobanker_text.value = f"Laobanker value: {laobanker.point_value}"
        upgrade_row = ft.Row([
            laobanker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_laobanker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_laobanker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_laobanker_score(e):
        global laobanker_text
        laobanker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Laobanker":
                laobanker = mahjongker
                break
        laobanker.point_value = laobanker.point_value + 5
        laobanker_text.value = f"Laobanker value: {laobanker.point_value}"
        page.update()

    def decrement_laobanker_score(e):
        global laobanker_text
        laobanker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Laobanker":
                laobanker = mahjongker
                break
        laobanker.point_value = max(0, laobanker.point_value - 5)
        laobanker_text.value = f"Laobanker value: {laobanker.point_value}"
        page.update()

    def handle_spoilker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global spoilker_text
        # Add UI to increase/decrease value of ayceker
        spoilker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Spoilker":
                spoilker = mahjongker
                break
        spoilker_text.value = f"Spoilker value: {spoilker.point_value}"
        upgrade_row = ft.Row([
            spoilker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_spoilker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_spoilker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_spoilker_score(e):
        global spoilker_text
        spoilker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Spoilker":
                spoilker = mahjongker
                break
        spoilker.point_value = spoilker.point_value + 1
        spoilker_text.value = f"Spoilker value: {spoilker.point_value}"
        page.update()

    def decrement_spoilker_score(e):
        global spoilker_text
        spoilker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Spoilker":
                spoilker = mahjongker
                break
        spoilker.point_value = max(0, spoilker.point_value - 1)
        spoilker_text.value = f"Spoilker value: {spoilker.point_value}"
        page.update()

    def handle_donnerker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global donnerker_text
        # Add UI to increase/decrease value of ayceker
        donnerker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Donnerker":
                donnerker = mahjongker
                break
        donnerker_text.value = f"Donnerker value: {donnerker.point_value}"
        upgrade_row = ft.Row([
            donnerker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_donnerker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_donnerker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_donnerker_score(e):
        global donnerker_text
        donnerker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Donnerker":
                donnerker = mahjongker
                break
        donnerker.point_value = donnerker.point_value + 15
        donnerker_text.value = f"Donnerker value: {donnerker.point_value}"
        page.update()

    def decrement_donnerker_score(e):
        global donnerker_text
        donnerker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Donnerker":
                donnerker = mahjongker
                break
        donnerker.point_value = max(0, donnerker.point_value - 15)
        donnerker_text.value = f"Donnerker value: {donnerker.point_value}"
        page.update()

    def handle_doraker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global doraker_text
        # Add UI to increase/decrease value of ayceker
        doraker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Doraker":
                doraker = mahjongker
                break
        doraker_text.value = f"Doraker value: {doraker.point_value}"
        upgrade_row = ft.Row([
            doraker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_doraker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_doraker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_doraker_score(e):
        global doraker_text
        doraker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Doraker":
                doraker = mahjongker
                break
        doraker.point_value = doraker.point_value + 15
        doraker_text.value = f"Doraker value: {doraker.point_value}"
        page.update()

    def decrement_doraker_score(e):
        global doraker_text
        doraker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Doraker":
                doraker = mahjongker
                break
        doraker.point_value = max(0, doraker.point_value - 15)
        doraker_text.value = f"Doraker value: {doraker.point_value}"
        page.update()

    def handle_odiumker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global odiumker_text
        # Add UI to increase/decrease value of ayceker
        odiumker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Odiumker":
                odiumker = mahjongker
                break
        odiumker_text.value = f"Odiumker value: {odiumker.point_value}"
        upgrade_row = ft.Row([
            odiumker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_odiumker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_odiumker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_odiumker_score(e):
        global odiumker_text
        odiumker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Odiumker":
                odiumker = mahjongker
                break
        odiumker.point_value = odiumker.point_value + 3
        odiumker_text.value = f"Odiumker value: {odiumker.point_value}"
        page.update()

    def decrement_odiumker_score(e):
        global odiumker_text
        odiumker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Odiumker":
                odiumker = mahjongker
                break
        odiumker.point_value = max(0, odiumker.point_value - 3)
        odiumker_text.value = f"Odiumker value: {odiumker.point_value}"
        page.update()

    def handle_bamenker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global bamenker_text
        # Add UI to increase/decrease value of ayceker
        bamenker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Bamenker":
                bamenker = mahjongker
                break
        bamenker_text.value = f"Bamenker value: {bamenker.point_value}"
        upgrade_row = ft.Row([
            bamenker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_bamenker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_bamenker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_bamenker_score(e):
        global bamenker_text
        bamenker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Bamenker":
                bamenker = mahjongker
                break
        bamenker.point_value = bamenker.point_value + 7
        bamenker_text.value = f"Bamenker value: {bamenker.point_value}"
        page.update()

    def decrement_bamenker_score(e):
        global bamenker_text
        bamenker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Bamenker":
                bamenker = mahjongker
                break
        bamenker.point_value = max(0, bamenker.point_value - 7)
        bamenker_text.value = f"Bamenker value: {bamenker.point_value}"
        page.update()

    def handle_denker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global denker_text
        # Add UI to increase/decrease value of ayceker
        denker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Denker":
                denker = mahjongker
                break
        denker_text.value = f"Denker value: {denker.point_value}"
        upgrade_row = ft.Row([
            denker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_denker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_denker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_denker_score(e):
        global denker_text
        denker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Denker":
                denker = mahjongker
                break
        denker.point_value = denker.point_value + 7
        denker_text.value = f"Denker value: {denker.point_value}"
        page.update()

    def decrement_denker_score(e):
        global denker_text
        denker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Denker":
                denker = mahjongker
                break
        denker.point_value = max(0, denker.point_value - 7)
        denker_text.value = f"Denker value: {denker.point_value}"
        page.update()

    def handle_chenker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global chenker_text
        # Add UI to increase/decrease value of ayceker
        chenker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Chenker":
                chenker = mahjongker
                break
        chenker_text.value = f"Chenker value: {chenker.point_value}"
        upgrade_row = ft.Row([
            chenker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_chenker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_chenker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_chenker_score(e):
        global chenker_text
        chenker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Chenker":
                chenker = mahjongker
                break
        chenker.point_value = chenker.point_value + 7
        chenker_text.value = f"Chenker value: {chenker.point_value}"
        page.update()

    def decrement_chenker_score(e):
        global chenker_text
        chenker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Chenker":
                chenker = mahjongker
                break
        chenker.point_value = max(0, chenker.point_value - 7)
        chenker_text.value = f"Chenker value: {chenker.point_value}"
        page.update()

    def handle_tanavastker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global tanavastker_text
        # Add UI to increase/decrease value of ayceker
        tanavastker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Tanavastker":
                tanavastker = mahjongker
                break
        tanavastker_text.value = f"Tanavastker value: {tanavastker.point_value}"
        upgrade_row = ft.Row([
            tanavastker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_tanavastker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_tanavastker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_tanavastker_score(e):
        global tanavastker_text
        tanavastker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Tanavastker":
                tanavastker = mahjongker
                break
        tanavastker.point_value = tanavastker.point_value + 10
        tanavastker_text.value = f"Tanavastker value: {tanavastker.point_value}"
        page.update()

    def decrement_tanavastker_score(e):
        global tanavastker_text
        tanavastker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Tanavastker":
                tanavastker = mahjongker
                break
        tanavastker.point_value = max(0, tanavastker.point_value - 10)
        tanavastker_text.value = f"Tanavastker value: {tanavastker.point_value}"
        page.update()

    def handle_jackblackgker_select(e):
        global my_mahjongker_text
        global my_jongkers_panel
        global jackblackgker_text
        # Add UI to increase/decrease value of ayceker
        jackblackgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Jackblackgker":
                jackblackgker = mahjongker
                break
        jackblackgker_text.value = f"Jackblackgker value: {jackblackgker.point_value}"
        upgrade_row = ft.Row([
            jackblackgker_text,
            ft.Column([
                ft.ElevatedButton(text="↑", on_click=increment_jackblackgker_score),
                ft.ElevatedButton(text="↓", on_click=decrement_jackblackgker_score)
                ])
            ],
            alignment=ft.MainAxisAlignment.CENTER)
        if len(my_jongkers_panel.content.controls) >= 3:
            my_jongkers_panel.content.controls[1] = upgrade_row
        else:
            my_jongkers_panel.content.controls.insert(1, upgrade_row)

        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        my_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def increment_jackblackgker_score(e):
        global jackblackgker_text
        jackblackgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Jackblackgker":
                jackblackgker = mahjongker
                break
        jackblackgker.point_value = jackblackgker.point_value + 5
        jackblackgker_text.value = f"Jackblackgker value: {jackblackgker.point_value}"
        page.update()

    def decrement_jackblackgker_score(e):
        global jackblackgker_text
        jackblackgker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Jackblackgker":
                jackblackgker = mahjongker
                break
        jackblackgker.point_value = max(0, jackblackgker.point_value - 5)
        jackblackgker_text.value = f"Jackblackgker value: {jackblackgker.point_value}"
        page.update()

    def apply_mahjongker_filter(e):
        global filtered_mahjongkers_list
        global mahjongker_filter
        global all_mahjongkers_list
        filtered_mahjongkers_list.clear()
        if mahjongker_filter.value == "":
            filtered_mahjongkers_list = all_mahjongkers_list.copy()
        else:
            for mahjongker in all_mahjongkers_list:
                if mahjongker_filter.value in mahjongker.name.lower():
                    filtered_mahjongkers_list.append(mahjongker)
        refresh_all_mahjongkers()

    def add_mahjongker(e):
        global my_mahjongkers
        global all_mahjongker_text
        if all_mahjongker_text.value != "":
            my_mahjongkers.append(all_mahjongkers_dict[all_mahjongker_text.value.lower()])
        all_mahjongker_text.value = ""
        refresh_my_mahjongkers()

    def remove_mahjongker(e):
        global my_mahjongkers
        global my_mahjongker_text
        if my_mahjongker_text.value != "":
            my_mahjongkers.remove(all_mahjongkers_dict[my_mahjongker_text.value.lower()])
        my_mahjongker_text.value = ""
        refresh_my_mahjongkers()

    def remove_item(e):
        global my_items
        global my_item_text
        if my_item_text.value != "":
            my_items.remove(all_item_names_dict[my_item_text.value])
        my_item_text.value = ""
        refresh_my_items()

    def refresh_my_mahjongkers():
        global my_mahjongker_grid
        global my_jongkers_panel
        global my_mahjongkers
        my_mahjongker_grid.controls.clear()
        my_mahjongkers_containers = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "AYCker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_AYCker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Pingker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_pingker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "KingKongker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_kingkongker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Meldker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_meldker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Fuckgker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_fuckgker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Suckgker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_suckgker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Speedker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_speedker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Empressker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_empressker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Laobanker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_laobanker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Spoilker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_spoilker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Donnerker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_donnerker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Doraker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_doraker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Odiumker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_odiumker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Bamenker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_bamenker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Denker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_denker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Chenker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_chenker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Tanavastker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_tanavastker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            elif mahjongker.name == "Jackblackgker":
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_jackblackgker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
            else:
                my_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_remove_mahjongker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )
        for mahjongker_container in my_mahjongkers_containers:
            my_mahjongker_grid.controls.append(mahjongker_container)

        my_jongkers_panel.header = ft.ListTile(title=ft.Text(f"My Jongkers ({len(my_mahjongkers)}/{MAX_NUM_MAHJONGKERS})"))
        page.update()

    def refresh_my_items():
        global my_items_grid
        global my_items_panel
        global my_items
        my_items_grid.controls.clear()
        my_items_containers = []
        for item in my_items:
            my_items_containers.append(
                ft.Container(
                    image=ft.DecorationImage(src=item.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    content=ft.Text(item.name, bgcolor="#000000", color=ft.colors.WHITE),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    on_click=handle_remove_item_select,
                    tooltip=ft.Tooltip(
                        message=item.description,
                        padding=20,
                        border_radius=10,
                        text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.Alignment(0.8, 1),
                            colors=[
                                "0xff1f005c",
                                "0xff5b0060",
                                "0xff870160",
                                "0xffac255e",
                                "0xffca485c",
                                "0xffe16b5c",
                                "0xfff39060",
                                "0xffffb56b",
                            ],
                            tile_mode=ft.GradientTileMode.MIRROR,
                        )
                    )
                )
            )
        for item_container in my_items_containers:
            my_items_grid.controls.append(item_container)

        my_items_panel.header = ft.ListTile(title=ft.Text(f"My Items ({len(my_items)}/{MAX_NUM_ITEMS})"))
        page.update()

    def refresh_all_mahjongkers():
        global all_mahjongker_grid
        global filtered_mahjongkers_list
        global all_mahjongker_grid
        all_mahjongker_grid.controls.clear()
        all_mahjongkers_containers = []
        # print(len(filtered_mahjongkers_list))
        for mahjongker in filtered_mahjongkers_list:
            all_mahjongkers_containers.append(
                ft.Container(
                    image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    on_click=handle_add_mahjongker_select,
                    tooltip=ft.Tooltip(
                        message=mahjongker.description,
                        padding=20,
                        border_radius=10,
                        text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.Alignment(0.8, 1),
                            colors=[
                                "0xff1f005c",
                                "0xff5b0060",
                                "0xff870160",
                                "0xffac255e",
                                "0xffca485c",
                                "0xffe16b5c",
                                "0xfff39060",
                                "0xffffb56b",
                            ],
                            tile_mode=ft.GradientTileMode.MIRROR,
                        )
                    )
                )
            )

        for mahjongker_container in all_mahjongkers_containers:
            all_mahjongker_grid.controls.append(mahjongker_container)

        page.update()

    # -------------------------------------------------------------
    # SCORER FUNC
    # -------------------------------------------------------------
    def refresh_selected_tiles():
        global selected_tiles
        global selected_tiles_row
        selected_tiles_row.controls.clear()
        for tile in selected_tiles:
            selected_tiles_row.controls.append(
                ft.Container(
                    content=ft.Text(f"{tile.suit}-{tile.rank}", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    on_click=handle_remove_tile
                    )
                )
        for i in range(4 - len(selected_tiles)):
            selected_tiles_row.controls.append(
                ft.Container(
                    content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    on_click=handle_remove_tile
                    )
                )
        page.update()

    def handle_add_tile_select(e):
        global lake_text
        tile_name_split = e.control.image.src.split("/")[2].split(".")[0].split("-")
        tile_suit = tile_name_split[0]
        tile_rank = tile_name_split[1]
        tile_modifier = "none"
        tile_dict = all_tiles
        tile_seal = "none"
        bonus_points = 0
        if len(tile_name_split) > 2:
            if tile_name_split[2] == "gold":
                tile_modifier = tile_name_split[2]
                if len(tile_name_split) > 3:
                    tile_seal = tile_name_split[3]
            else:
                tile_seal = tile_name_split[2]

        if tile_modifier == "gold":
            if tile_seal == "thunder":
                tile_dict = all_tiles_gold_thunder
            elif tile_seal == "sky":
                tile_dict = all_tiles_gold_sky
            elif tile_seal == "lake":
                tile_dict = all_tiles_gold_lake
                bonus_points = int(lake_text.value.split(" ")[2])
            elif tile_seal == "mountain":
                tile_dict = all_tiles_gold_mountain
            else:
                tile_dict = all_tiles_gold
        else:
            if tile_seal == "thunder":
                tile_dict = all_tiles_thunder
            elif tile_seal == "sky":
                tile_dict = all_tiles_sky
            elif tile_seal == "lake":
                tile_dict = all_tiles_lake
                bonus_points = int(lake_text.value.split(" ")[2])
            elif tile_seal == "mountain":
                tile_dict = all_tiles_mountain
            else:
                tile_dict = all_tiles

        tile = tile_dict[tile_suit][tile_rank].copy()
        tile.points = tile.points + bonus_points
        if len(selected_tiles) < 4:
            selected_tiles.append(tile)
        refresh_selected_tiles()
        page.update()

    def handle_remove_tile(e):
        global selected_tiles
        tile_name_split = e.control.image.src.split("/")[2].split(".")[0].split("-")
        tile_suit = e.control.image.src.split("/")[2].split(".")[0].split("-")[0]
        tile_rank = e.control.image.src.split("/")[2].split(".")[0].split("-")[1]
        tile_modifier = "none"
        tile_dict = all_tiles
        tile_seal = "none"
        if len(tile_name_split) > 2:
            if tile_name_split[2] == "gold":
                tile_modifier = tile_name_split[2]
                if len(tile_name_split) > 3:
                    tile_seal = tile_name_split[3]
            else:
                tile_seal = tile_name_split[2]

        if tile_modifier == "gold":
            if tile_seal == "thunder":
                tile_dict = all_tiles_gold_thunder
            elif tile_seal == "sky":
                tile_dict = all_tiles_gold_sky
            elif tile_seal == "lake":
                tile_dict = all_tiles_gold_lake
            elif tile_seal == "mountain":
                tile_dict = all_tiles_gold_mountain
            else:
                tile_dict = all_tiles_gold
        else:
            if tile_seal == "thunder":
                tile_dict = all_tiles_thunder
            elif tile_seal == "sky":
                tile_dict = all_tiles_sky
            elif tile_seal == "lake":
                tile_dict = all_tiles_lake
            elif tile_seal == "mountain":
                tile_dict = all_tiles_mountain
            else:
                tile_dict = all_tiles

        tile = tile_dict[tile_suit][tile_rank].copy()
        selected_tiles.remove(tile)
        refresh_selected_tiles()
        page.update()        

    def handle_tile_filter(e):
        global lake_adjuster
        # bamboo, dot, character, honor, special
        # none, gold
        # none, thunder, sky, lake, mountain
        # modifier_radio
        # seal_radio
        lake_adjuster.visible = False
        all_tile_containers.clear()
        all_tile_grid.controls.clear()
        tile_dict = all_tiles
        if modifier_radio.value == "gold":
            if seal_radio.value == "thunder":
                tile_dict = all_tiles_gold_thunder
            elif seal_radio.value == "sky":
                tile_dict = all_tiles_gold_sky
            elif seal_radio.value == "lake":
                tile_dict = all_tiles_gold_lake
                lake_adjuster.visible = True
            elif seal_radio.value == "mountain":
                tile_dict = all_tiles_gold_mountain
            else:
                tile_dict = all_tiles_gold
        else:
            if seal_radio.value == "thunder":
                tile_dict = all_tiles_thunder
            elif seal_radio.value == "sky":
                tile_dict = all_tiles_sky
            elif seal_radio.value == "lake":
                tile_dict = all_tiles_lake
                lake_adjuster.visible = True
            elif seal_radio.value == "mountain":
                tile_dict = all_tiles_mountain
            else:
                tile_dict = all_tiles

        if tile_radio.value == "honor":
            for rank in tile_dict["dragon"].keys():
                tile = tile_dict["dragon"][rank].copy()
                all_tile_containers.append(
                    ft.Container(
                        content=ft.Text(f"dragon-{tile.rank}", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_tile_select,
                    )
                )
            for rank in tile_dict["wind"].keys():
                tile = tile_dict["wind"][rank].copy()
                all_tile_containers.append(
                    ft.Container(
                        content=ft.Text(f"wind-{tile.rank}", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_tile_select,
                    )
                )
        else:
            for rank in tile_dict[tile_radio.value].keys():
                tile = tile_dict[tile_radio.value][rank].copy()
                all_tile_containers.append(
                    ft.Container(
                        content=ft.Text(f"{tile.suit}-{tile.rank}", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_tile_select,
                    )
                )
        for tile_container in all_tile_containers:
            all_tile_grid.controls.append(tile_container)
            page.update()

    def add_selected_tiles_to_hand(e):
        global selected_tiles
        # global current_hand
        if len(selected_tiles) < 2:
            print("Invalid tile combination.")
        elif len(selected_tiles) == 2:
            print("Is eyes")
            eyes = Eyes()
            for tile in selected_tiles:
                eyes.add_tile(tile)
            current_hand.add_eyes(eyes)
        else:
            print ("Is meld")
            meld = Meld()
            for tile in selected_tiles:
                meld.add_tile(tile)
            current_hand.add_meld(meld)
        selected_tiles.clear()
        refresh_selected_tiles()
        refresh_current_hand()
        page.update()
        # print(current_hand)

    def remove_from_hand(e):
        if e.control.text.split(" ")[1] == "Eyes":
            current_hand.eyes = []
        else:
            index = int(e.control.text.split(" ")[2]) - 1
            del current_hand.melds[index]
        refresh_current_hand()

    def refresh_current_hand():
        global hand_score_text
        global mahjong_pts_text
        global mahjong_pts_adjuster
        global mahjong_money_text
        global mahjong_money_adjuster

        current_hand_panel.content.controls.clear()
        for i, meld in enumerate(current_hand.melds):
            meld_grid = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )
            for tile in meld.tiles:
                meld_grid.controls.append(
                    ft.Container(
                        image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_tile_select
                ))
            current_hand_panel.content.controls.append(ft.Row([
                ft.ElevatedButton(text=f"Remove Meld {i+1}", on_click=remove_from_hand),
                meld_grid
            ]))

        if current_hand.eyes:
            eye_grid = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )
            for tile in current_hand.eyes[0].tiles:
                eye_grid.controls.append(
                    ft.Container(
                        image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                ))
            current_hand_panel.content.controls.append(ft.Row([
                ft.ElevatedButton(text=f"Remove Eyes", on_click=remove_from_hand),
                eye_grid
            ]))

        current_hand_panel.content.controls.append(mahjong_pts_adjuster)
        current_hand_panel.content.controls.append(mahjong_money_adjuster)

        current_hand_panel.content.controls.append(ft.Row([
            ft.ElevatedButton(text="Score Hand", on_click=score_hand),
            hand_score_text,
            ft.ElevatedButton(text="Add to Total Score", on_click=add_to_total_score)],
            spacing=15)
        )
        page.update()

    def show_select_table_wind(e):
        # select border
        e.control.border = ft.border.all(5, ft.colors.PINK_600)
        for i, control in enumerate(scoring_tiles_row.controls):
            if i != 0:
                control.border = ft.border.all(0)

        if len(other_scoring_panel.content.controls) > 1:
            del other_scoring_panel.content.controls[1]
        wind_select_grid = ft.GridView(
            height=100,
            width=400,
            runs_count=1,
            max_extent=95,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

        other_scoring_panel.content.controls.append(wind_select_grid) # append grid view of selection
        for rank in all_tiles["wind"].keys():
            tile = all_tiles["wind"][rank]
            wind_select_grid.controls.append(
                ft.Container(
                    content=ft.Text(f"wind-{tile.rank}", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    on_click=handle_select_table_wind,
                )
            )
        page.update()

    def handle_select_table_wind(e):
        global table_wind
        tile_suit = e.control.image.src.split("/")[2].split(".")[0].split("-")[0]
        tile_rank = e.control.image.src.split("/")[2].split(".")[0].split("-")[1]
        table_wind = all_tiles[tile_suit][tile_rank]
        refresh_other_scoring()

    def show_select_seat_wind(e):
        # select border
        e.control.border = ft.border.all(5, ft.colors.PINK_600)
        for i, control in enumerate(scoring_tiles_row.controls):
            if i != 1:
                control.border = ft.border.all(0)

        if len(other_scoring_panel.content.controls) > 1:
            del other_scoring_panel.content.controls[1]
        wind_select_grid = ft.GridView(
            height=100,
            width=400,
            runs_count=1,
            max_extent=95,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )

        other_scoring_panel.content.controls.append(wind_select_grid) # append grid view of selection
        for rank in all_tiles["wind"].keys():
            tile = all_tiles["wind"][rank]
            wind_select_grid.controls.append(
                ft.Container(
                    content=ft.Text(f"wind-{tile.rank}", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    on_click=handle_select_seat_wind,
                )
            )
        page.update()

    def handle_select_seat_wind(e):
        global seat_wind
        tile_suit = e.control.image.src.split("/")[2].split(".")[0].split("-")[0]
        tile_rank = e.control.image.src.split("/")[2].split(".")[0].split("-")[1]
        seat_wind = all_tiles[tile_suit][tile_rank]
        refresh_other_scoring()

    def refresh_other_scoring():
        scoring_tiles_row.controls.clear()
        scoring_tiles_row.controls.append(
        ft.Container(
            content=ft.Text("Table Wind", bgcolor="#000000", color=ft.colors.WHITE),
            image=ft.DecorationImage(src=table_wind.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
            border_radius=ft.border_radius.all(5),
            ink=True,
            on_click=show_select_table_wind
            )
        )
        scoring_tiles_row.controls.append(
            ft.Container(
                content=ft.Text("Seat Wind", bgcolor="#000000",color=ft.colors.WHITE),
                image=ft.DecorationImage(src=seat_wind.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                border_radius=ft.border_radius.all(5),
                ink=True,
                on_click=show_select_seat_wind
                )
            )
        page.update()

    def score_hand(e):
        # global hand_score_text
        global tot_score
        global sequence_hand_mult
        global triplet_hand_mult
        global half_flush_hand_mult 
        global flush_hand_mult
        global scored_money
        global mahjong_pts_text
        mahj_pts = int(mahjong_pts_text.value.split(" ")[2])
        mahj_money = int(mahjong_money_text.value.split(" ")[3])
        i = score(current_hand, table_wind, seat_wind, my_mahjongkers, mahj_pts, mahj_money)
        buffetker_score = score_buffettker()
        tot_score = round((i[0] + buffetker_score), 2)
        scored_money = int(i[1])
        hand_score_text.value =  f"Score: {tot_score} | +${i[1]}"
        page.update()

    def add_to_total_score(e):
        global total_score
        global tot_score
        global scored_money
        global money
        global mahjong_pts_text
        global mahjong_money_text
        total_score = round(total_score + tot_score, 2)
        money = money + scored_money
        tot_score = 0
        scored_money = 0
        hand_score_text.value =  f"Score: 0"
        score_text.value = str(total_score)
        current_hand.melds = []
        current_hand.eyes = []
        mahjong_pts_text.value = f"Mahjong Pts: 0 pts"
        mahjong_money_text.value = f"Mahjong Money: $ 0"
        refresh_money_text()
        refresh_current_hand()

    def score_buffettker():
        global my_mahjongkers
        global money
        buffettker = Buffettker()
        if buffettker in my_mahjongkers:
            return int(money/3)*10
        else:
            return 0

    def increment_lake_score(e):
        global lake_text
        point_value = int(lake_text.value.split(" ")[2]) + 10
        lake_text.value = f"Lake value: {point_value}"
        page.update()

    def decrement_lake_score(e):
        global lake_text
        point_value = max(0, int(lake_text.value.split(" ")[2]) - 10)
        lake_text.value = f"Lake value: {point_value}"
        page.update()

    def increment_mahjong_pts(e):
        global mahjong_pts_text
        pts_value = int(mahjong_pts_text.value.split(" ")[2]) + 5
        mahjong_pts_text.value = f"Mahjong Pts: {pts_value} pts"
        page.update()

    def decrement_mahjong_pts(e):
        global mahjong_pts_text
        pts_value = max(0, int(mahjong_pts_text.value.split(" ")[2]) - 5)
        mahjong_pts_text.value = f"Mahjong Pts: {pts_value} pts"
        page.update()

    def increment_mahjong_money(e):
        global mahjong_money_text
        money_value = int(mahjong_money_text.value.split(" ")[3]) + 1
        mahjong_money_text.value = f"Mahjong Money: $ {money_value}"
        page.update()

    def decrement_mahjong_money(e):
        global mahjong_money_text
        money_value = max(0, int(mahjong_money_text.value.split(" ")[3]) - 1)
        mahjong_money_text.value = f"Mahjong Money: $ {money_value}"
        page.update()

    # -------------------------------------------------------------
    # SHOP FUNC
    # -------------------------------------------------------------

    def increment_shop_tier(e):
        global shop_round
        global shop_tier_text
        shop_round += 1
        shop_round = min(4, shop_round)
        shop_tier_text.value = f"Shop Tier: {shop_round}"
        page.update()

    def decrement_shop_tier(e):
        global shop_round
        global shop_tier_text
        shop_round -= 1
        shop_round = max(0, shop_round)
        shop_tier_text.value = f"Shop Tier: {shop_round}"
        page.update()

    # initial mahjongker roll
    def refresh_initial_mahjongkers(e):
        global initial_mahjongkers_row
        global initial_mahjongker_info_column
        initial_mahjongkers_row.controls.clear()
        i = 0
        selected_i = []
        while i < 10:
            index = random.randint(0,len(initial_mahjongkers_list)-1)
            if index not in selected_i: 
                mahjongker = initial_mahjongkers_list[index]
                if mahjongker not in my_mahjongkers:
                    selected_i.append(index)
                    i = i+1

        for i in selected_i:
            mahjongker = initial_mahjongkers_list[i]
            initial_mahjongkers_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_initial_mahjongker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        ),
                        # tooltip=MahjongkerTooltip(mahjongker=mahjongker)
                    )
            )
            initial_mahjongker_info_column.controls.append(ft.Text(f"{mahjongker.name} : {mahjongker.description}", color=ft.colors.WHITE, size=20))
        initial_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.CHECK, on_click=refresh_initial_mahjongkers))
        page.update()

    def refresh_initial_mahjongkers_empty():
        global initial_mahjongkers_row
        initial_mahjongkers_row.controls.clear()
        for i in range(3):
            initial_mahjongkers_row.controls.append(
                ft.Container(
                    content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    )
                )
        initial_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.CHECK, on_click=refresh_initial_mahjongkers))
        page.update()

    def handle_add_initial_mahjongker_select(e):
        global initial_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        initial_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def add_initial_mahjongker(e):
        global my_mahjongkers
        global initial_mahjongkers_row
        global initial_mahjongker_text
        if initial_mahjongker_text.value == "":
            return
        mahjongker = all_mahjongkers_dict[initial_mahjongker_text.value.lower()]
        my_mahjongkers.append(mahjongker)
        # then replace this slot in the grid view
        for container in initial_mahjongkers_row.controls:
            # print(container.content.value)
            if mahjongker.name in container.content.value:
                selected_container = container
                break
        initial_mahjongker_text.value = ""
        selected_container.image="/jongker/sold.png"
        selected_container.content.value= "SOLD"
        page.update()
        refresh_my_mahjongkers()

    # common mahjongker roll
    def refresh_common_mahjongkers(e):
        global common_mahjongkers_row
        common_mahjongkers_row.controls.clear()
        i = 0
        selected_i = []
        while i < 3:
            index = random.randint(0,len(common_mahjongkers_list)-1)
            if index not in selected_i: 
                mahjongker = common_mahjongkers_list[index]
                if mahjongker not in my_mahjongkers:
                    selected_i.append(index)
                    i = i+1

        for i in selected_i:
            mahjongker = common_mahjongkers_list[i]
            common_mahjongkers_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_common_mahjongker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        ),
                        # tooltip=MahjongkerTooltip(mahjongker=mahjongker)
                    )
            )
        common_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_common_mahjongkers))
        page.update()

    def refresh_common_mahjongkers_empty():
        global common_mahjongkers_row
        common_mahjongkers_row.controls.clear()
        for i in range(3):
            common_mahjongkers_row.controls.append(
                ft.Container(
                    content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    )
                )
        common_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_common_mahjongkers))
        page.update()

    def handle_add_common_mahjongker_select(e):
        global common_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        common_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def add_common_mahjongker(e):
        global my_mahjongkers
        global common_mahjongker_text
        if common_mahjongker_text.value != "":
            my_mahjongkers.append(all_mahjongkers_dict[common_mahjongker_text.value.lower()])
        common_mahjongker_text.value = ""
        refresh_my_mahjongkers()
        refresh_common_mahjongkers_empty()

    # uncommon mahjongker roll
    def refresh_uncommon_mahjongkers(e):
        global uncommon_mahjongkers_row
        uncommon_mahjongkers_row.controls.clear()
        i = 0
        selected_i = []
        while i < 3:
            index = random.randint(0,len(uncommon_mahjongkers_list)-1)
            if index not in selected_i: 
                mahjongker = uncommon_mahjongkers_list[index]
                if mahjongker not in my_mahjongkers:
                    selected_i.append(index)
                    i = i+1

        for i in selected_i:
            mahjongker = uncommon_mahjongkers_list[i]
            uncommon_mahjongkers_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_uncommon_mahjongker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        ),
                        # tooltip=MahjongkerTooltip(mahjongker=mahjongker)
                    )
            )
        uncommon_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_uncommon_mahjongkers))
        page.update()

    def refresh_uncommon_mahjongkers_empty():
        global uncommon_mahjongkers_row
        uncommon_mahjongkers_row.controls.clear()
        for i in range(3):
            uncommon_mahjongkers_row.controls.append(
                ft.Container(
                    content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    )
                )
        uncommon_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_uncommon_mahjongkers))
        page.update()

    def handle_add_uncommon_mahjongker_select(e):
        global uncommon_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        uncommon_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def add_uncommon_mahjongker(e):
        global my_mahjongkers
        global uncommon_mahjongker_text
        if uncommon_mahjongker_text.value != "":
            my_mahjongkers.append(all_mahjongkers_dict[uncommon_mahjongker_text.value.lower()])
        uncommon_mahjongker_text.value = ""
        refresh_my_mahjongkers()
        refresh_uncommon_mahjongkers_empty()

    # rare mahjongker roll
    def refresh_rare_mahjongkers(e):
        global rare_mahjongkers_row
        rare_mahjongkers_row.controls.clear()
        i = 0
        selected_i = []
        while i < 3:
            index = random.randint(0,len(rare_mahjongkers_list)-1)
            if index not in selected_i: 
                mahjongker = rare_mahjongkers_list[index]
                if mahjongker not in my_mahjongkers:
                    selected_i.append(index)
                    i = i+1

        for i in selected_i:
            mahjongker = rare_mahjongkers_list[i]
            rare_mahjongkers_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_rare_mahjongker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        ),
                        # tooltip=MahjongkerTooltip(mahjongker=mahjongker)
                    )
            )
        rare_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_rare_mahjongkers))
        page.update()

    def refresh_rare_mahjongkers_empty():
        global rare_mahjongkers_row
        rare_mahjongkers_row.controls.clear()
        for i in range(3):
            rare_mahjongkers_row.controls.append(
                ft.Container(
                    content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    )
                )
        rare_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_rare_mahjongkers))
        page.update()

    def handle_add_rare_mahjongker_select(e):
        global rare_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        rare_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def add_rare_mahjongker(e):
        global my_mahjongkers
        global rare_mahjongker_text
        if rare_mahjongker_text.value != "":
            my_mahjongkers.append(all_mahjongkers_dict[rare_mahjongker_text.value.lower()])
        rare_mahjongker_text.value = ""
        refresh_my_mahjongkers()
        refresh_rare_mahjongkers_empty()

    # item roll
    def refresh_items(e):
        global item_pack_row
        global item_pack_info_column
        item_pack_row.controls.clear()
        item_pack_info_column.controls.clear()
        i = 0
        selected_i = []
        borders = []
        while i < 3:
            rarity_roll = random.choices(ITEM_RARITIES, weights=ITEM_RARITY_PROBABILITY)[0]
            print(rarity_roll)
            item = roll_item(rarity_roll, selected_i)
            selected_i.append(all_items_list.index(item))   
            if rarity_roll == "piggy":
                borders.append(ft.border.all(4, ft.colors.GREEN_600))
            elif rarity_roll == "common":
                borders.append(ft.border.all(4, ft.colors.BLUE_600))
            elif rarity_roll == "uncommon":
                borders.append(ft.border.all(4, ft.colors.PURPLE_600))
            else:
                borders.append(ft.border.all(4, ft.colors.RED_600))
            i = i+1

        j = 0
        for i in selected_i:
            item = all_items_list[i]
            item_pack_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=item.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(f"{item.name}", bgcolor="#000000", color=ft.colors.WHITE),
                        border=borders[j],
                        ink=True,
                        on_click=handle_add_shop_item_select,
                        tooltip=ft.Tooltip(
                            message=f"{item.description}",
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
            )
            item_pack_info_column.controls.append(ft.Text(f"{item.name} : {item.description}", color=ft.colors.WHITE, size=20))
            j += 1

        item_pack_row.controls.append(ft.FloatingActionButton(icon=ft.icons.CHECK, on_click=refresh_items))
        page.update()

    def refresh_items_empty():
        global item_pack_row
        item_pack_row.controls.clear()
        for i in range(3):
            item_pack_row.controls.append(
                ft.Container(
                    content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    )
                )
        item_pack_row.controls.append(ft.FloatingActionButton(icon=ft.icons.CHECK, on_click=refresh_items))
        page.update()

    def handle_item_select(e):
        global item_text
        item_name = e.control.image.src.split("/")[2].split(".")[0]
        item_text.value = all_items_dict[item_name].name
        page.update()

    def select_item(e):
        global my_mahjongkers
        global rare_mahjongker_text
        do_nothing()

    # zodiac roll
    def refresh_zodiacs(e):
        global zodiac_row
        zodiac_row.controls.clear()
        i = 0
        selected_i = []
        while i < 3:
            index = random.randint(0,len(all_zodiacs_list)-1)
            if index not in selected_i: 
                zodiac = all_zodiacs_list[index]
                selected_i.append(index)
                i = i+1

        for i in selected_i:
            zodiac = all_zodiacs_list[i]
            zodiac_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=zodiac.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(zodiac.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_zodiac_select,
                        tooltip=ft.Tooltip(
                            message=zodiac.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        ),
                        # tooltip=zodiacTooltip(zodiac=zodiac)
                    )
            )
        zodiac_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_zodiacs))
        page.update()

    def refresh_zodiacs_empty():
        global zodiac_row
        zodiac_row.controls.clear()
        for i in range(3):
            zodiac_row.controls.append(
                ft.Container(
                    content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    )
                )
        zodiac_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_zodiacs))
        page.update()

    def handle_zodiac_select(e):
        global zodiac_text
        zodiac_name = e.control.image.src.split("/")[2].split(".")[0]
        zodiac_text.value = all_zodiacs_dict[zodiac_name].name
        page.update()

    def select_zodiac(e):
        global my_mahjongkers
        global rare_mahjongker_text
        do_nothing()

    # trigram roll
    def refresh_trigrams(e):
        global trigram_row
        global trigram_pack_info_column
        trigram_row.controls.clear()
        trigram_pack_info_column.controls.clear()
        i = 0
        selected_i = []
        while i < 3:
            index = random.randint(0,len(all_trigrams_list)-1)
            if index not in selected_i: 
                trigram = all_trigrams_list[index]
                selected_i.append(index)
                i = i+1

        for i in selected_i:
            trigram = all_trigrams_list[i]
            trigram_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=trigram.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(trigram.name, bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_trigram_select,
                        tooltip=ft.Tooltip(
                            message=trigram.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        ),
                        # tooltip=trigramTooltip(trigram=trigram)
                    )
            )
            trigram_pack_info_column.controls.append(ft.Text(f"{trigram.name} : {trigram.description}", color=ft.colors.WHITE, size=20))
        trigram_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_trigrams))
        page.update()

    def refresh_trigrams_empty():
        global trigram_row
        trigram_row.controls.clear()
        for i in range(3):
            trigram_row.controls.append(
                ft.Container(
                    content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                    image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    )
                )
        trigram_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_trigrams))
        page.update()

    def handle_trigram_select(e):
        global trigram_text
        trigram_name = e.control.image.src.split("/")[2].split(".")[0]
        trigram_text.value = all_trigrams_dict[trigram_name].name
        page.update()

    def select_trigram(e):
        global my_mahjongkers
        global rare_mahjongker_text
        do_nothing()

    def roll_mahjongker(rarity):
        global my_mahjongkers
        global shop_selected_i
        if rarity == "common":
            for i in range(20):
                index = random.randint(0,len(common_mahjongkers_list)-1)
                mahjongker = common_mahjongkers_list[index]
                if mahjongker not in my_mahjongkers and all_mahjongkers_list.index(mahjongker) not in shop_selected_i:
                    return mahjongker
        elif rarity == "uncommon":
            for i in range(20):
                index = random.randint(0,len(uncommon_mahjongkers_list)-1)
                mahjongker = uncommon_mahjongkers_list[index]
                if mahjongker not in my_mahjongkers and all_mahjongkers_list.index(mahjongker) not in shop_selected_i:
                    return mahjongker
        else:
            for i in range(20):
                index = random.randint(0,len(rare_mahjongkers_list)-1)
                mahjongker = rare_mahjongkers_list[index]
                if mahjongker not in my_mahjongkers and all_mahjongkers_list.index(mahjongker) not in shop_selected_i:
                    return mahjongker 

    def roll_item(rarity, selected_i):
        if rarity == "piggy":
            return piggy_items_list[0]
        elif rarity == "common":
            for i in range(20):
                index = random.randint(0,len(common_items_list)-1)
                item = common_items_list[index]
                if all_items_list.index(item) not in selected_i:
                    return item
        elif rarity == "uncommon":
            for i in range(20):
                index = random.randint(0,len(uncommon_items_list)-1)
                item = uncommon_items_list[index]
                if all_items_list.index(item) not in selected_i:
                    return item
        else:
            for i in range(20):
                index = random.randint(0,len(rare_items_list)-1)
                item = rare_items_list[index]
                if all_items_list.index(item) not in selected_i:
                    return item 

    def refresh_shop(e):
        global shop_row
        global shop_info_column
        global my_mahjongkers_shop_row
        global shop_round
        global refresh_shop_button
        global item_row
        global item_info_column
        global reroll_cost
        global reroll_item_cost
        global shop_selected_i
        global item_selected
        global zodiac_selected
        global trigram_selected
        global my_mahjongkers
        global money
        global reroll_zodiac_cost
        global reroll_trigram_cost
        global shop_zodiac_row
        global shop_trigram_row
        global trigram_info_column

        money = money + ROUND_UBI[shop_round]
        # shop_round = min(5, shop_round + 1)
        refresh_shop_inventory()
        # give UBI
        refresh_money_text()
        # reset zodiac/trigram cost
        current_trigram_cost = TRIGRAM_COST
        current_zodiac_cost = ZODIAC_COST

        shop_row.controls.clear()
        shop_info_column.controls.clear()
        i = 0
        shop_selected_i = []
        borders = []
        while i < 7:
            rarity_roll = random.choices(SHOP_MAHJONGKER_RARITIES, weights=SHOP_MAHJONGKER_RARITY_PROBABILITIES[int(shop_round)])[0]
            print(rarity_roll)
            mahjongker = roll_mahjongker(rarity_roll)
            shop_selected_i.append(all_mahjongkers_list.index(mahjongker))
            if rarity_roll == "common":
                borders.append(ft.border.all(4, ft.colors.BLUE_600))
            elif rarity_roll == "uncommon":
                borders.append(ft.border.all(4, ft.colors.PURPLE_600))
            else:
                borders.append(ft.border.all(4, ft.colors.RED_600))
            i = i+1

        j = 0
        for i in shop_selected_i:
            mahjongker = all_mahjongkers_list[i]
            shop_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(f"{mahjongker.name} - ${mahjongker.cost}", bgcolor="#000000", color=ft.colors.WHITE),
                        border=borders[j],
                        ink=True,
                        on_click=handle_add_shop_mahjongker_select,
                        tooltip=ft.Tooltip(
                            message=f"${mahjongker.cost} - {mahjongker.description}",
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
            )
            shop_info_column.controls.append(ft.Text(f"${mahjongker.cost} - {mahjongker.name} : {mahjongker.description}", color=ft.colors.WHITE, size=20))
            j += 1
        reroll_cost = MAHJONGKERS_REROLL_COST

        # items
        # item_row.controls.clear()
        # item_info_column.controls.clear()
        # i = 0
        # item_selected = []
        # while i < 3:
        #     random_i = random.randint(0,len(all_items_list)-1)
        #     item = all_items_list[random_i]
        #     if item not in item_selected: 
        #         item_selected.append(item)
        #         i = i+1

        # for item in item_selected:
        #     item_row.controls.append(
        #         ft.Container(
        #                 image=ft.DecorationImage(src=item.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
        #                 content=ft.Text(f"{item.name} - ${item.cost}", bgcolor="#000000", color=ft.colors.WHITE),
        #                 border_radius=ft.border_radius.all(5),
        #                 ink=True,
        #                 on_click=handle_add_shop_item_select,
        #                 tooltip=ft.Tooltip(
        #                     message=f"${item.cost} - {item.description}",
        #                     padding=20,
        #                     border_radius=10,
        #                     text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
        #                     gradient=ft.LinearGradient(
        #                         begin=ft.alignment.top_left,
        #                         end=ft.alignment.Alignment(0.8, 1),
        #                         colors=[
        #                             "0xff1f005c",
        #                             "0xff5b0060",
        #                             "0xff870160",
        #                             "0xffac255e",
        #                             "0xffca485c",
        #                             "0xffe16b5c",
        #                             "0xfff39060",
        #                             "0xffffb56b",
        #                         ],
        #                         tile_mode=ft.GradientTileMode.MIRROR,
        #                     )
        #                 )
        #             )
        #     )
        #     item_info_column.controls.append(ft.Text(f"${item.cost} - {item.name} : {item.description}", color=ft.colors.WHITE, size=20))
        # reroll_cost = 1
        # reroll_item_cost = 1

        # zodiacs
        # shop_zodiac_row.controls.clear()
        # reroll_zodiac_cost = ZODIAC_COST
        # i = 0
        # zodiac_selected = []
        # while i < 3:
        #     random_i = random.randint(0,len(all_zodiacs_list)-1)
        #     zodiac = all_zodiacs_list[random_i]
        #     if zodiac not in zodiac_selected: 
        #         zodiac_selected.append(zodiac)
        #         i = i+1

        # for zodiac in zodiac_selected:
        #     shop_zodiac_row.controls.append(
        #         ft.Container(
        #                 image=ft.DecorationImage(src=zodiac.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
        #                 content=ft.Text(f"{zodiac.name} - ${zodiac.cost}", bgcolor="#000000", color=ft.colors.WHITE),
        #                 border_radius=ft.border_radius.all(5),
        #                 ink=True,
        #                 on_click=handle_add_shop_zodiac_select,
        #                 tooltip=ft.Tooltip(
        #                     message=f"${zodiac.cost} - {zodiac.description}",
        #                     padding=20,
        #                     border_radius=10,
        #                     text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
        #                     gradient=ft.LinearGradient(
        #                         begin=ft.alignment.top_left,
        #                         end=ft.alignment.Alignment(0.8, 1),
        #                         colors=[
        #                             "0xff1f005c",
        #                             "0xff5b0060",
        #                             "0xff870160",
        #                             "0xffac255e",
        #                             "0xffca485c",
        #                             "0xffe16b5c",
        #                             "0xfff39060",
        #                             "0xffffb56b",
        #                         ],
        #                         tile_mode=ft.GradientTileMode.MIRROR,
        #                     )
        #                 )
        #             )
        #     )

        # shop_zodiac_row.controls.append(ft.FloatingActionButton(text=f"${reroll_zodiac_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_zodiacs))

        # trigrams
        # reroll_trigram_cost = TRIGRAM_COST
        # shop_trigram_row.controls.clear()
        # trigram_info_column.controls.clear()
        # i = 0
        # trigram_selected = []
        # while i < 3:
        #     random_i = random.randint(0,len(all_trigrams_list)-1)
        #     trigram = all_trigrams_list[random_i]
        #     if trigram not in trigram_selected: 
        #         trigram_selected.append(trigram)
        #         i = i+1

        # for trigram in trigram_selected:
        #     shop_trigram_row.controls.append(
        #         ft.Container(
        #                 image=ft.DecorationImage(src=trigram.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
        #                 content=ft.Text(f"{trigram.name} - ${trigram.cost}", bgcolor="#000000", color=ft.colors.WHITE),
        #                 border_radius=ft.border_radius.all(5),
        #                 ink=True,
        #                 on_click=handle_add_shop_trigram_select,
        #                 tooltip=ft.Tooltip(
        #                     message=f"${trigram.cost} - {trigram.description}",
        #                     padding=20,
        #                     border_radius=10,
        #                     text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
        #                     gradient=ft.LinearGradient(
        #                         begin=ft.alignment.top_left,
        #                         end=ft.alignment.Alignment(0.8, 1),
        #                         colors=[
        #                             "0xff1f005c",
        #                             "0xff5b0060",
        #                             "0xff870160",
        #                             "0xffac255e",
        #                             "0xffca485c",
        #                             "0xffe16b5c",
        #                             "0xfff39060",
        #                             "0xffffb56b",
        #                         ],
        #                         tile_mode=ft.GradientTileMode.MIRROR,
        #                     )
        #                 )
        #             )
        #     )
        #     trigram_info_column.controls.append(ft.Text(f"${trigram.cost} - {trigram.name} : {trigram.description}", color=ft.colors.WHITE, size=20))

        # shop_trigram_row.controls.append(ft.FloatingActionButton(text=f"${reroll_trigram_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_trigrams))

        # Picker disabled for comp shop
        # for mahjongker in my_mahjongkers:
        #     if mahjongker.name == "Picker":
        #         reroll_cost = 0
        shop_row.controls.append(ft.FloatingActionButton(text=f"${reroll_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_mahjongkers))
        # item_row.controls.append(ft.FloatingActionButton(text=f"${reroll_item_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_items))
        enable_hand_upgrade_buy()
        refresh_shop_button.text = f"Refresh Shop Round {shop_round + 1}"
        page.update()

    def reroll_shop_mahjongkers(e):
        global my_mahjongkers
        global shop_round
        global shop_info_column
        global reroll_cost
        global shop_row
        global shop_selected_i
        global money
        if money >= reroll_cost:
            money = money - reroll_cost
            refresh_money_text()
            # reroll_cost += 1
            shop_row.controls.clear()
            shop_info_column.controls.clear()
            i = 0
            shop_selected_i = []
            borders = []

            while i < 7:
                rarity_roll = random.choices(SHOP_MAHJONGKER_RARITIES, weights=SHOP_MAHJONGKER_RARITY_PROBABILITIES[int(shop_round)])[0]
                print(rarity_roll)
                mahjongker = roll_mahjongker(rarity_roll)
                shop_selected_i.append(all_mahjongkers_list.index(mahjongker))
                if rarity_roll == "common":
                    borders.append(ft.border.all(4, ft.colors.BLUE_600))
                elif rarity_roll == "uncommon":
                    borders.append(ft.border.all(4, ft.colors.PURPLE_600))
                else:
                    borders.append(ft.border.all(4, ft.colors.RED_600))
                i = i+1

            j = 0
            for i in shop_selected_i:
                mahjongker = all_mahjongkers_list[i]
                shop_row.controls.append(
                    ft.Container(
                            image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                            content=ft.Text(f"{mahjongker.name} - ${mahjongker.cost}", bgcolor="#000000", color=ft.colors.WHITE),
                            border=borders[j],
                            ink=True,
                            on_click=handle_add_shop_mahjongker_select,
                            tooltip=ft.Tooltip(
                                message=f"${mahjongker.cost} - {mahjongker.description}",
                                padding=20,
                                border_radius=10,
                                text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_left,
                                    end=ft.alignment.Alignment(0.8, 1),
                                    colors=[
                                        "0xff1f005c",
                                        "0xff5b0060",
                                        "0xff870160",
                                        "0xffac255e",
                                        "0xffca485c",
                                        "0xffe16b5c",
                                        "0xfff39060",
                                        "0xffffb56b",
                                    ],
                                    tile_mode=ft.GradientTileMode.MIRROR,
                                )
                            )
                        )
                )
                shop_info_column.controls.append(ft.Text(f"${mahjongker.cost} - {mahjongker.name} : {mahjongker.description}", color=ft.colors.WHITE, size=20))
                j += 1
            shop_row.controls.append(ft.FloatingActionButton(text=f"${reroll_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_mahjongkers))
            page.update()

    def refill_shop_mahjongkers(e):
        global my_mahjongkers
        global shop_round
        global shop_info_column
        global shop_row
        global shop_selected_i

        borders = []
        for i in range(len(shop_selected_i)):
            if shop_selected_i[i] == -1:
                rarity_roll = random.choices(SHOP_MAHJONGKER_RARITIES, weights=SHOP_MAHJONGKER_RARITY_PROBABILITIES[int(shop_round)])[0]
                print(rarity_roll)
                mahjongker = roll_mahjongker(rarity_roll)
                shop_selected_i[i] = all_mahjongkers_list.index(mahjongker)
                if rarity_roll == "common":
                    borders.append(ft.border.all(4, ft.colors.BLUE_600))
                elif rarity_roll == "uncommon":
                    borders.append(ft.border.all(4, ft.colors.PURPLE_600))
                else:
                    borders.append(ft.border.all(4, ft.colors.RED_600))
            else:
                mahjongker = all_mahjongkers_list[shop_selected_i[i]]
                if mahjongker.cost == COMMON_MAHJONGKER_COST:
                    borders.append(ft.border.all(4, ft.colors.BLUE_600))
                elif mahjongker.cost == UNCOMMON_MAHJONGKER_COST:
                    borders.append(ft.border.all(4, ft.colors.PURPLE_600))
                else:
                    borders.append(ft.border.all(4, ft.colors.RED_600))

        j = 0
        shop_row.controls.clear()
        shop_info_column.controls.clear()

        for i in shop_selected_i:
            mahjongker = all_mahjongkers_list[i]
            shop_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(f"{mahjongker.name} - ${mahjongker.cost}", bgcolor="#000000", color=ft.colors.WHITE),
                        border=borders[j],
                        ink=True,
                        on_click=handle_add_shop_mahjongker_select,
                        tooltip=ft.Tooltip(
                            message=f"${mahjongker.cost} - {mahjongker.description}",
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
            )
            shop_info_column.controls.append(ft.Text(f"${mahjongker.cost} - {mahjongker.name} : {mahjongker.description}", color=ft.colors.WHITE, size=20))
            j += 1
        shop_row.controls.append(ft.FloatingActionButton(text=f"${reroll_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_mahjongkers))
        page.update()

    def reroll_shop_items(e):
        global reroll_item_cost
        global money
        global item_row
        global item_info_column
        if money >= reroll_item_cost:
            money = money - reroll_item_cost
            refresh_money_text()
            reroll_item_cost += 1
            item_row.controls.clear()
            item_info_column.controls.clear()
        else:
            return
        i = 0
        item_selected = []
        while i < 3:
            random_i = random.randint(0,len(all_items_list)-1)
            item = all_items_list[random_i]
            if item not in item_selected: 
                item_selected.append(item)
                i = i+1

        for item in item_selected:
            item_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=item.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(f"{item.name} - ${item.cost}", bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_shop_item_select,
                        tooltip=ft.Tooltip(
                            message=f"${item.cost} - {item.description}",
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
            )
            item_info_column.controls.append(ft.Text(f"${item.cost} - {item.name} : {item.description}", color=ft.colors.WHITE, size=20))

        item_row.controls.append(ft.FloatingActionButton(text=f"${reroll_item_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_items))
        page.update()

    def reroll_shop_zodiacs(e):
        global reroll_zodiac_cost
        global money
        global shop_zodiac_row
        if money >= reroll_zodiac_cost:
            money = money - reroll_zodiac_cost
            refresh_money_text()
            reroll_zodiac_cost += 1
            shop_zodiac_row.controls.clear()
        i = 0
        zodiac_selected = []
        while i < 3:
            random_i = random.randint(0,len(all_zodiacs_list)-1)
            zodiac = all_zodiacs_list[random_i]
            if zodiac not in zodiac_selected: 
                zodiac_selected.append(zodiac)
                i = i+1

        for zodiac in zodiac_selected:
            shop_zodiac_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=zodiac.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(f"{zodiac.name} - ${zodiac.cost}", bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_shop_zodiac_select,
                        tooltip=ft.Tooltip(
                            message=f"${zodiac.cost} - {zodiac.description}",
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
            )

        shop_zodiac_row.controls.append(ft.FloatingActionButton(text=f"${reroll_zodiac_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_zodiacs))
        page.update()

    def reroll_shop_trigrams(e):
        global reroll_trigram_cost
        global money
        global shop_trigram_row
        global trigram_info_column
        if money >= reroll_trigram_cost:
            money = money - reroll_trigram_cost
            refresh_money_text()
            reroll_trigram_cost += 1
            shop_trigram_row.controls.clear()
            trigram_info_column.controls.clear()
        else:
            return
        i = 0
        trigram_selected = []
        while i < 3:
            random_i = random.randint(0,len(all_trigrams_list)-1)
            trigram = all_trigrams_list[random_i]
            if trigram not in trigram_selected: 
                trigram_selected.append(trigram)
                i = i+1

        for trigram in trigram_selected:
            shop_trigram_row.controls.append(
                ft.Container(
                        image=ft.DecorationImage(src=trigram.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(f"{trigram.name} - ${trigram.cost}", bgcolor="#000000", color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_shop_trigram_select,
                        tooltip=ft.Tooltip(
                            message=f"${trigram.cost} - {trigram.description}",
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
            )
            trigram_info_column.controls.append(ft.Text(f"${trigram.cost} - {trigram.name} : {trigram.description}", color=ft.colors.WHITE, size=20))

        shop_trigram_row.controls.append(ft.FloatingActionButton(text=f"${reroll_trigram_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_trigrams))
        page.update()

    def handle_add_shop_mahjongker_select(e):
        global shop_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        shop_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def handle_sell_shop_mahjongker_select(e):
        global shop_sell_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        shop_sell_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def buy_mahjongker(e):
        global my_mahjongkers
        global shop_mahjongker_text
        global money
        global shop_row
        global shop_selected_i
        selected_container = []
        if shop_mahjongker_text.value != "" and shop_mahjongker_text.value != "TOO POOR":
            mahjongker = all_mahjongkers_dict[shop_mahjongker_text.value.lower()]
            if money >= mahjongker.cost:
                my_mahjongkers.append(mahjongker)
                money = money - mahjongker.cost
                # then replace this slot in the grid view
                for i, container in enumerate(shop_row.controls):
                    # print(container.content.value)
                    if mahjongker.name in container.content.value:
                        selected_container = container
                        shop_selected_i[i] = -1
                        break
                refresh_money_text()
                shop_mahjongker_text.value = ""
                selected_container.image="/jongker/sold.png"
                selected_container.content.value= "SOLD"
            else:
                shop_mahjongker_text.value = "TOO POOR"
        refresh_shop_inventory()
        refresh_my_mahjongkers()
        page.update()

    def sell_mahjongker(e):
        global my_mahjongkers
        global shop_sell_mahjongker_text
        global money
        selected_container = []
        if shop_sell_mahjongker_text.value != "":
            mahjongker = all_mahjongkers_dict[shop_sell_mahjongker_text.value.lower()]
            my_mahjongkers.remove(mahjongker)
            money = money + mahjongker.sell_value
            refresh_shop_inventory()
            refresh_money_text()
            shop_sell_mahjongker_text.value = ""
        refresh_shop_inventory()
        page.update()

    def buy_zodiac(e):
        global shop_zodiac_row
        global money
        global current_zodiac_cost
        global zodiac_selected
        global shop_zodiac_text

        selected_container = []
        zodiac = all_zodiacs_dict[shop_zodiac_text.value.lower()]
        if money >= zodiac.cost:
            money = money - zodiac.cost
            # current_zodiac_cost = current_zodiac_cost + 1
            for container in shop_zodiac_row.controls:
                # print(container.content.value)
                if zodiac.name in container.content.value:
                    selected_container = container
                    break
            shop_zodiac_text.value = ""
            selected_container.image="/jongker/sold.png"
            selected_container.content.value= "SOLD"
            refresh_money_text()
        else:
            shop_zodiac_text.value = "TOO POOR"
            return

        # shop_zodiac_row.controls.clear()
        # i = 0
        # zodiac_selected = []
        # while i < 3:
        #     index = random.randint(0,len(all_zodiacs_list)-1)
        #     if index not in zodiac_selected: 
        #         zodiac = all_zodiacs_list[index]
        #         zodiac_selected.append(index)
        #         i = i+1

        # for i in zodiac_selected:
        #     zodiac = all_zodiacs_list[i]
        #     shop_zodiac_row.controls.append(
        #         ft.Container(
        #                 image=ft.DecorationImage(src=zodiac.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
        #                 content=ft.Text(zodiac.name, bgcolor="#000000", color=ft.colors.WHITE),
        #                 border_radius=ft.border_radius.all(5),
        #                 ink=True,
        #                 on_click=handle_zodiac_select,
        #                 tooltip=ft.Tooltip(
        #                     message=zodiac.description,
        #                     padding=20,
        #                     border_radius=10,
        #                     text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
        #                     gradient=ft.LinearGradient(
        #                         begin=ft.alignment.top_left,
        #                         end=ft.alignment.Alignment(0.8, 1),
        #                         colors=[
        #                             "0xff1f005c",
        #                             "0xff5b0060",
        #                             "0xff870160",
        #                             "0xffac255e",
        #                             "0xffca485c",
        #                             "0xffe16b5c",
        #                             "0xfff39060",
        #                             "0xffffb56b",
        #                         ],
        #                         tile_mode=ft.GradientTileMode.MIRROR,
        #                     )
        #                 ),
        #                 # tooltip=zodiacTooltip(zodiac=zodiac)
        #             )
        #     )
        # shop_zodiac_row.controls.append(ft.FloatingActionButton(text=f"${current_zodiac_cost}", icon=ft.icons.REFRESH, on_click=buy_zodiac))
        page.update()

    def buy_trigram(e):
        global shop_trigram_row
        global money
        global current_trigram_cost
        global trigram_selected
        global shop_trigram_text

        selected_container = []
        if len(shop_trigram_text.value) == 0: return
        trigram = all_trigrams_dict[shop_trigram_text.value.lower()]
        if money >= trigram.cost:
            money = money - trigram.cost
            # current_trigram_cost = current_trigram_cost + 1
            for container in shop_trigram_row.controls:
                # print(container.content.value)
                if trigram.name in container.content.value:
                    selected_container = container
                    break
            shop_trigram_text.value = ""
            selected_container.image="/jongker/sold.png"
            selected_container.content.value= "SOLD"
            refresh_money_text()
        else:
            shop_zodiac_text.value = "TOO POOR"
            return

        # if money >= current_trigram_cost:
        #     money = money - current_trigram_cost
        #     current_trigram_cost = current_trigram_cost + 1
        #     refresh_money_text()
        # else:
        #     return

        # shop_trigram_row.controls.clear()
        # i = 0
        # trigram_selected = []
        # while i < 3:
        #     index = random.randint(0,len(all_trigrams_list)-1)
        #     if index not in trigram_selected: 
        #         trigram = all_trigrams_list[index]
        #         trigram_selected.append(index)
        #         i = i+1

        # for i in trigram_selected:
        #     trigram = all_trigrams_list[i]
        #     shop_trigram_row.controls.append(
        #         ft.Container(
        #                 image=ft.DecorationImage(src=trigram.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
        #                 content=ft.Text(trigram.name, bgcolor="#000000", color=ft.colors.WHITE),
        #                 border_radius=ft.border_radius.all(5),
        #                 ink=True,
        #                 on_click=handle_trigram_select,
        #                 tooltip=ft.Tooltip(
        #                     message=trigram.description,
        #                     padding=20,
        #                     border_radius=10,
        #                     text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
        #                     gradient=ft.LinearGradient(
        #                         begin=ft.alignment.top_left,
        #                         end=ft.alignment.Alignment(0.8, 1),
        #                         colors=[
        #                             "0xff1f005c",
        #                             "0xff5b0060",
        #                             "0xff870160",
        #                             "0xffac255e",
        #                             "0xffca485c",
        #                             "0xffe16b5c",
        #                             "0xfff39060",
        #                             "0xffffb56b",
        #                         ],
        #                         tile_mode=ft.GradientTileMode.MIRROR,
        #                     )
        #                 ),
        #                 # tooltip=trigramTooltip(trigram=trigram)
        #             )
        #     )
        # shop_trigram_row.controls.append(ft.FloatingActionButton(text=f"${current_trigram_cost}", icon=ft.icons.REFRESH, on_click=buy_trigram))
        page.update()

    def refresh_shop_inventory():
        global my_mahjongkers
        global my_mahjongkers_shop_row
        my_mahjongkers_shop_row.controls.clear()
        my_mahjongkers_shop_row_containers = []
        for mahjongker in my_mahjongkers:
            my_mahjongkers_shop_row_containers.append(
                ft.Container(
                    image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    content=ft.Text(f"{mahjongker.name} - ${mahjongker.sell_value}", bgcolor="#000000", color=ft.colors.WHITE),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                    on_click=handle_sell_shop_mahjongker_select,
                    tooltip=ft.Tooltip(
                        message=mahjongker.description,
                        padding=20,
                        border_radius=10,
                        text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.top_left,
                            end=ft.alignment.Alignment(0.8, 1),
                            colors=[
                                "0xff1f005c",
                                "0xff5b0060",
                                "0xff870160",
                                "0xffac255e",
                                "0xffca485c",
                                "0xffe16b5c",
                                "0xfff39060",
                                "0xffffb56b",
                            ],
                            tile_mode=ft.GradientTileMode.MIRROR,
                        )
                    )
                )
            )
        for mahjongker_container in my_mahjongkers_shop_row_containers:
            my_mahjongkers_shop_row.controls.append(mahjongker_container)
        page.update()

    def refresh_money_text():
        global shop_money_text
        global money_text
        global money
        shop_money_text.value = f"Money: {money}"
        money_text.value = f"{money}"
        page.update()

    def upgrade_sequence(e):
        global money
        global sequence_hand_mult
        if money >= SEQUENCE_UPGRADE_COST:
            money = money - SEQUENCE_UPGRADE_COST
            # sequence_hand_mult = sequence_hand_mult * HAND_TYPE_UPGRADE_MULT
            sequence_hand_mult = round(sequence_hand_mult + SEQUENCE_UPGRADE_AMOUNT, 2)
            refresh_money_text()
            refresh_hand_mult_text()
            # disable_hand_upgrade_buy()

    def upgrade_triplet(e):
        global money
        global triplet_hand_mult
        if money >= TRIPLET_UPGRADE_COST:
            money = money - TRIPLET_UPGRADE_COST
            # triplet_hand_mult = triplet_hand_mult * HAND_TYPE_UPGRADE_MULT
            triplet_hand_mult = round(triplet_hand_mult + TRIPLET_UPGRADE_AMOUNT, 2)
            refresh_money_text()
            refresh_hand_mult_text()
            # disable_hand_upgrade_buy()

    def upgrade_half_flush(e):
        global money
        global half_flush_hand_mult
        if money >= HALF_FLUSH_UPGRADE_COST:
            money = money - HALF_FLUSH_UPGRADE_COST
            # half_flush_hand_mult = half_flush_hand_mult * HAND_TYPE_UPGRADE_MULT
            half_flush_hand_mult = round(half_flush_hand_mult + HALF_FLUSH_UPGRADE_AMOUNT, 2)
            refresh_money_text()
            refresh_hand_mult_text()
            # disable_hand_upgrade_buy()

    def upgrade_flush(e):
        global money
        global flush_hand_mult
        if money >= FLUSH_UPGRADE_COST:
            money = money - FLUSH_UPGRADE_COST
            # flush_hand_mult = flush_hand_mult * HAND_TYPE_UPGRADE_MULT
            flush_hand_mult = round(flush_hand_mult + FLUSH_UPGRADE_AMOUNT, 2)
            refresh_money_text()
            refresh_hand_mult_text()
            # disable_hand_upgrade_buy()

    def upgrade_avatar(e):
        global money
        global sequence_hand_mult
        global triplet_hand_mult
        global half_flush_hand_mult
        global flush_hand_mult
        if money >= AVATAR_UPGRADE_COST:
            money = money - AVATAR_UPGRADE_COST
            sequence_hand_mult = round(sequence_hand_mult + SEQUENCE_UPGRADE_AMOUNT, 2)
            triplet_hand_mult = round(triplet_hand_mult + TRIPLET_UPGRADE_AMOUNT, 2)
            half_flush_hand_mult = round(half_flush_hand_mult + HALF_FLUSH_UPGRADE_AMOUNT, 2)
            flush_hand_mult = round(flush_hand_mult + FLUSH_UPGRADE_AMOUNT, 2)
            refresh_money_text()
            refresh_hand_mult_text()
            # disable_hand_upgrade_buy()

    def refresh_hand_mult_text():
        global sequence_current_text
        global triplet_current_text
        global half_flush_current_text
        global flush_current_text
        sequence_current_text.value = f"+{sequence_hand_mult}"
        triplet_current_text.value = f"+{triplet_hand_mult}"
        half_flush_current_text.value = f"+{half_flush_hand_mult}"
        flush_current_text.value = f"+{flush_hand_mult}"
        page.update()

    def disable_hand_upgrade_buy():
        global sequence_button
        global triplet_button
        global half_flush_button
        global flush_button
        global avatar_button
        global hand_upgrade_enabled
        sequence_button.text = "x"
        sequence_button.on_click = do_nothing
        triplet_button.text = "x"
        triplet_button.on_click = do_nothing
        half_flush_button.text = "x"
        half_flush_button.on_click = do_nothing
        flush_button.text = "x"
        flush_button.on_click = do_nothing
        avatar_button.text = "x"
        avatar_button.on_click = do_nothing
        hand_upgrade_enabled = False
        page.update()

    def enable_hand_upgrade_buy():
        global sequence_button
        global triplet_button
        global half_flush_button
        global flush_button
        global avatar_button
        global hand_upgrade_enabled
        global shop_round
        sequence_button.text = "${0}".format(SEQUENCE_UPGRADE_COSTS[shop_round - 1])
        sequence_button.on_click = upgrade_sequence
        triplet_button.text = "${0}".format(TRIPLET_UPGRADE_COSTS[shop_round - 1])
        triplet_button.on_click = upgrade_triplet
        half_flush_button.text = "${0}".format(HALF_FLUSH_UPGRADE_COSTS[shop_round - 1])
        half_flush_button.on_click = upgrade_half_flush
        flush_button.text = "${0}".format(FLUSH_UPGRADE_COSTS[shop_round - 1])
        flush_button.on_click = upgrade_flush
        avatar_button.text = "${0}".format(AVATAR_UPGRADE_COSTS[shop_round - 1])
        avatar_button.on_click = upgrade_avatar
        hand_upgrade_enabled = True
        page.update()


    def buy_item(e):
        global shop_item_text
        global money
        global my_items
        global item_row
        selected_container = []
        if shop_item_text.value != "" and shop_item_text.value != "TOO POOR":
            item = all_item_names_dict[shop_item_text.value]
            if money >= item.cost:
                my_items.append(item)
                money = money - item.cost
                # then replace this slot in the grid view
                for container in item_row.controls:
                    # print(container.content.value)
                    if item.name in container.content.value:
                        selected_container = container
                        break
                refresh_money_text()
                shop_item_text.value = ""
                selected_container.image="/jongker/sold.png"
                selected_container.content.value= "SOLD"
            else:
                shop_item_text.value = "TOO POOR"
        page.update()    

    def handle_add_shop_item_select(e):
        global shop_item_text
        item_name = e.control.image.src.split("/")[2].split(".")[0]
        shop_item_text.value = all_items_dict[item_name].name
        page.update()

    def handle_add_shop_zodiac_select(e):
        global shop_zodiac_text
        zodiac_name = e.control.image.src.split("/")[2].split(".")[0]
        shop_zodiac_text.value = all_zodiacs_dict[zodiac_name].name
        page.update()

    def handle_add_shop_trigram_select(e):
        global shop_trigram_text
        trigram_name = e.control.image.src.split("/")[2].split(".")[0]
        shop_trigram_text.value = all_trigrams_dict[trigram_name].name
        page.update()

    def upgrade_hand_size(e):
        global money
        global hand_size_level
        global hand_size_text
        global hand_size
        global hand_size_upgrade_button
        print(hand_size_upgrade_button.text)
        if money >= HAND_SIZE_COSTS[hand_size_level]:
            money = money - HAND_SIZE_COSTS[hand_size_level]
            hand_size = hand_size + 1
            hand_size_level = hand_size_level + 1
            hand_size_text.value = str(hand_size)
            hand_size_upgrade_button.text = f"Upgrade Hand Size - ${HAND_SIZE_COSTS[hand_size_level]}"
            print(hand_size_upgrade_button.text)
            refresh_money_text()
            page.update()
        page.update()

    def adjust_shop_round(e):
        global shop_round
        global refresh_shop_button
        shop_round = int(e.control.value)
        refresh_shop_button.text = f"Refresh Shop Round {shop_round}"
        page.update()

    def do_nothing(e):
        print("I do nothing!")

    # -------------------------------------------------------------
    # PAGES - ROUTES HERE
    # -------------------------------------------------------------
    def route_change(e):
        # stats
        global score_adjust_tf
        global shop_round
        global money
        global money_adjust_tf
        global hand_size_text
        global hand_size
        global hand_size_level
        global sequence_hand_mult
        global triplet_hand_mult
        global half_flush_hand_mult
        global flush_hand_mult
        global sequence_mult_text
        global triplet_mult_text
        global half_flush_mult_text
        global flush_mult_text
        # inventory
        global my_mahjongkers
        global filtered_mahjongkers_list
        global all_mahjongker_text
        global all_mahjongker_grid
        global my_mahjongker_text
        global my_item_text
        global mahjongker_filter
        global my_mahjongker_grid
        global my_items_grid
        global my_jongkers_panel
        global my_items_panel
        # scorer
        global selected_tiles
        global current_hand
        global table_wind
        global seat_wind
        global hand_score_text
        global add_tiles_panel
        global tile_radio
        global modifier_radio
        global seal_radio
        global all_tile_grid
        global selected_tiles_row
        global all_tile_containers
        global other_scoring_panel
        global scoring_tiles_row
        global current_hand_panel
        global lake_text
        global lake_adjuster
        global mahjong_pts_text
        global mahjong_pts_adjuster
        global mahjong_money_text
        global mahjong_money_adjuster
        # shop
        global refresh_shop_button
        global zodiac_row
        global zodiac_text
        global trigram_row
        global trigram_info_column
        global trigram_text
        global initial_mahjongkers_row
        global initial_mahjongker_text
        global initial_mahjongker_info_column
        global common_mahjongkers_row
        global common_mahjongker_text
        global uncommon_mahjongkers_row
        global uncommon_mahjongker_text
        global rare_mahjongkers_row
        global rare_mahjongker_text
        global shop_row
        global shop_info_column
        global my_mahjongkers_shop_row
        global item_row
        global item_info_column
        global my_items_shop_row
        global item_pack_row
        global item_pack_info_column
        global trigram_pack_info_column
        global shop_zodiac_row
        global shop_trigram_row
        global shop_mahjongker_text
        global shop_sell_mahjongker_text
        global shop_item_text
        global shop_zodiac_text
        global shop_trigram_text
        global reroll_cost
        global reroll_item_cost
        global current_zodiac_cost
        global current_trigram_cost
        global shop_money_text
        global shop_tier_text
        global hand_size_upgrade_button
        global shop_selected_i
        global item_selected
        global zodiac_selected
        global trigram_selected
        global sequence_button
        global sequence_current_text
        global triplet_button
        global triplet_current_text
        global half_flush_button
        global half_flush_current_text
        global flush_button
        global flush_current_text
        global avatar_button
        global hand_upgrade_enabled

        # -------------------------------------------------------------
        # Stats Page
        # -------------------------------------------------------------

        score_adjust_tf = ft.TextField(label="Score Adjust")
        money_adjust_tf = ft.TextField(label="Money Adjust")
        sequence_mult_text = ft.Text(f"{sequence_hand_mult}")
        triplet_mult_text = ft.Text(f"{triplet_hand_mult}")
        half_flush_mult_text = ft.Text(f"{half_flush_hand_mult}")
        flush_mult_text = ft.Text(f"{flush_hand_mult}")

        page.views.clear() 
        page.views.append(
            ft.View(
                "/stats",
                [
                    ft.Row(
                        [
                            (ft.Column([
                                ft.Text("Score", size=40),
                                score_text],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )),
                            (ft.Column([
                                score_adjust_tf,
                                ft.ElevatedButton(text="Adjust Score", on_click=adjust_score)],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )),
                        ],
                        spacing=50,
                        alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Row(
                        [
                            (ft.Column([
                                ft.Text("Money", size=40),
                                ft.Row([
                                    money_text,
                                    ft.Column([
                                        ft.ElevatedButton(text="↑", on_click=increment_money),
                                        ft.ElevatedButton(text="↓", on_click=decrement_money)
                                        ])
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER)
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )),
                            (ft.Column([
                                money_adjust_tf,
                                ft.ElevatedButton(text="Adjust Money", on_click=adjust_money)],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ))
                        ],
                        spacing=50,
                        alignment=ft.MainAxisAlignment.CENTER),
                    # ft.Divider(),
                    # ft.Row(
                    #     [
                    #         ft.DataTable(
                    #             columns=[
                    #                 ft.DataColumn(ft.Text("Hand")),
                    #                 ft.DataColumn(ft.Text("Mult")),
                    #                 ft.DataColumn(ft.Text("Adjust")),
                    #             ],
                    #             rows=[
                    #                 ft.DataRow(
                    #                     cells=[
                    #                         ft.DataCell(ft.Text("Sequence")),
                    #                         ft.DataCell(sequence_mult_text),
                    #                         ft.DataCell(
                    #                             ft.Row([
                    #                                 ft.ElevatedButton(text="↑", on_click=increment_sequence_mult),
                    #                                 ft.ElevatedButton(text="↓", on_click=decrement_sequence_mult)
                    #                                 ])
                    #                         )
                    #                     ]
                    #                 ),
                    #                 ft.DataRow(
                    #                     cells=[
                    #                         ft.DataCell(ft.Text("Triplet")),
                    #                         ft.DataCell(triplet_mult_text),
                    #                         ft.DataCell(
                    #                             ft.Row([
                    #                                 ft.ElevatedButton(text="↑", on_click=increment_triplet_mult),
                    #                                 ft.ElevatedButton(text="↓", on_click=decrement_triplet_mult)
                    #                                 ])
                    #                         )
                    #                     ]
                    #                 ),
                    #                 ft.DataRow(
                    #                     cells=[
                    #                         ft.DataCell(ft.Text("Half Flush")),
                    #                         ft.DataCell(half_flush_mult_text),
                    #                         ft.DataCell(
                    #                             ft.Row([
                    #                                 ft.ElevatedButton(text="↑", on_click=increment_half_flush_mult),
                    #                                 ft.ElevatedButton(text="↓", on_click=decrement_half_flush_mult)
                    #                                 ])
                    #                         )
                    #                     ]
                    #                 ),
                    #                 ft.DataRow(
                    #                     cells=[
                    #                         ft.DataCell(ft.Text("Flush")),
                    #                         ft.DataCell(flush_mult_text),
                    #                         ft.DataCell(
                    #                             ft.Row([
                    #                                 ft.ElevatedButton(text="↑", on_click=increment_flush_mult),
                    #                                 ft.ElevatedButton(text="↓", on_click=decrement_flush_mult)
                    #                                 ])
                    #                         )
                    #                     ]
                    #                 ),
                    #             ]
                    #         )],
                    #         alignment=ft.MainAxisAlignment.CENTER,
                    #         spacing=15), 
                        ft.Divider(),
                        ft.Column([
                            ft.Text("Hand Size", size=40),
                            ft.Row([
                                hand_size_text,
                                ft.Column([
                                    ft.ElevatedButton(text="↑", on_click=increment_hand_size),
                                    ft.ElevatedButton(text="↓", on_click=decrement_hand_size)
                                    ])
                                ],
                                alignment=ft.MainAxisAlignment.CENTER)
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                    ft.NavigationBar(destinations=[
                        ft.NavigationBarDestination(icon=ft.icons.QUERY_STATS, label="Stats"),
                        ft.NavigationBarDestination(icon=ft.icons.ADD_TO_PHOTOS, label="Inventory"),
                        ft.NavigationBarDestination(icon=ft.icons.CALCULATE, label="Scorer"),
                        ft.NavigationBarDestination(icon=ft.icons.ADD_SHOPPING_CART, label="Shop"),
                        ],
                        on_change=go_to_page,
                        selected_index=0)
                ],
                scroll=ft.ScrollMode.AUTO
            )
        )
        page.update()
        # -------------------------------------------------------------
        # Mahjongkers Page
        # -------------------------------------------------------------
        if page.route == "/inventory":
            # expansion panel list
            panel = ft.ExpansionPanelList(
                expand_icon_color=ft.colors.AMBER,
                elevation=1,
                divider_color=ft.colors.AMBER,
                expanded_header_padding=ft.padding.symmetric(0.0, 0.0)
            )
            
            # -------------------------------------------------------------
            # my jongkers tab 
            # -------------------------------------------------------------

            my_jongkers_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.GREEN_500,
                header=ft.ListTile(title=ft.Text(f"My Jongkers ({len(my_mahjongkers)}/{MAX_NUM_MAHJONGKERS})")),
                can_tap_header=True
            )

            my_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            my_mahjongker_grid = ft.GridView(
                # expand=1,
                height=400,
                width=400,
                runs_count=5,
                max_extent=150,
                child_aspect_ratio=1.0,
                spacing=15,
                run_spacing=15,
            )
            
            my_jongkers_panel.content = ft.Column([
                my_mahjongker_grid,
                ft.Row([
                    ft.ElevatedButton(text="Remove", on_click=remove_mahjongker),
                    my_mahjongker_text
                ])
            ])
            
            refresh_my_mahjongkers()
            panel.controls.append(my_jongkers_panel)

            # -------------------------------------------------------------
            # my items tab 
            # -------------------------------------------------------------
            my_items_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.RED_500,
                header=ft.ListTile(title=ft.Text(f"My Items ({len(my_items)}/{MAX_NUM_ITEMS})")),
                can_tap_header=True
            )

            my_item_text = ft.Text("", color=ft.colors.WHITE)
            my_items_grid = ft.GridView(
                # expand=1,
                height=400,
                width=400,
                runs_count=5,
                max_extent=150,
                child_aspect_ratio=1.0,
                spacing=15,
                run_spacing=15,
            )
            
            my_items_panel.content = ft.Column([
                my_items_grid,
                ft.Row([
                    ft.ElevatedButton(text="Remove", on_click=remove_item),
                    my_item_text
                ])
            ])

            refresh_my_items()
            panel.controls.append(my_items_panel)

            # -------------------------------------------------------------
            # add jongkers tab 
            # -------------------------------------------------------------

            add_jongkers_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.BLUE_800,
                header=ft.ListTile(title=ft.Text("Add Jongkers")),
                can_tap_header=True
            )

            mahjongker_filter = ft.TextField(label="Filter", on_change=apply_mahjongker_filter)
            all_mahjongker_grid = ft.GridView(
                # expand=1,
                height=400,
                width=400,
                runs_count=5,
                max_extent=150,
                child_aspect_ratio=1.0,
                spacing=15,
                run_spacing=15,
            )
            all_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            add_jongkers_panel.content = ft.Column([
                    mahjongker_filter,
                    all_mahjongker_grid,
                    ft.Row([
                        ft.ElevatedButton(text="Add", on_click=add_mahjongker),
                        all_mahjongker_text
                    ])
                    
                ])

            all_mahjongkers_containers = []

            for mahjongker in all_mahjongkers_list:
                all_mahjongkers_containers.append(
                    ft.Container(
                        image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        content=ft.Text(mahjongker.name, bgcolor="#000000",color=ft.colors.WHITE),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_mahjongker_select,
                        tooltip=ft.Tooltip(
                            message=mahjongker.description,
                            padding=20,
                            border_radius=10,
                            text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.Alignment(0.8, 1),
                                colors=[
                                    "0xff1f005c",
                                    "0xff5b0060",
                                    "0xff870160",
                                    "0xffac255e",
                                    "0xffca485c",
                                    "0xffe16b5c",
                                    "0xfff39060",
                                    "0xffffb56b",
                                ],
                                tile_mode=ft.GradientTileMode.MIRROR,
                            )
                        )
                    )
                )

            for mahjongker_container in all_mahjongkers_containers:
                all_mahjongker_grid.controls.append(mahjongker_container)

            panel.controls.append(add_jongkers_panel)

            page.views.append(
                ft.View(
                    "/inventory",
                    [
                        panel,
                        ft.NavigationBar(destinations=[
                            ft.NavigationBarDestination(icon=ft.icons.QUERY_STATS, label="Stats"),
                            ft.NavigationBarDestination(icon=ft.icons.ADD_TO_PHOTOS, label="Inventory"),
                            ft.NavigationBarDestination(icon=ft.icons.CALCULATE, label="Scorer"),
                            ft.NavigationBarDestination(icon=ft.icons.ADD_SHOPPING_CART, label="Shop"),
                            ],
                            on_change=go_to_page,
                            selected_index=1)
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )
        page.update()
        # -------------------------------------------------------------
        # SCORER Page
        # -------------------------------------------------------------
        if page.route == "/scorer":
            # expansion panel list
            panel = ft.ExpansionPanelList(
                expand_icon_color=ft.colors.AMBER,
                elevation=1,
                divider_color=ft.colors.AMBER,
                expanded_header_padding=ft.padding.symmetric(0.0, 0.0)
            )

            # -------------------------------------------------------------
            # add tiles tab 
            # -------------------------------------------------------------

            add_tiles_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.GREEN_500,
                header=ft.ListTile(title=ft.Text(f"Add Tiles")),
                can_tap_header=True
            )

            tile_radio = ft.RadioGroup(content=ft.Row([
                ft.Radio(value="bamboo", label="Bamboo"),
                ft.Radio(value="dot", label="Dot"),
                ft.Radio(value="character", label="Character"),
                ft.Radio(value="honor", label="Honor"),
                ft.Radio(value="special", label="Special")
            ]),
            value="bamboo",
            on_change=handle_tile_filter)

            modifier_radio = ft.RadioGroup(content=ft.Row([
                ft.Radio(value="none", label="None"),
                ft.Radio(value="gold", label="Gold"),
            ]),
            value="none",
            on_change=handle_tile_filter)

            seal_radio = ft.RadioGroup(content=ft.Row([
                ft.Radio(value="none", label="None"),
                ft.Radio(value="thunder", label="Thunder"),
                ft.Radio(value="sky", label="Sky"),
                # ft.Radio(value="lake", label="Lake"),
                ft.Radio(value="mountain", label="Mountain")   
            ]),
            value="none",
            on_change=handle_tile_filter)

            all_tile_grid = ft.GridView(
                # expand=1,
                height=400,
                width=400,
                runs_count=5,
                max_extent=150,
                child_aspect_ratio=1.0,
                spacing=15,
                run_spacing=15,
            )
            all_mahjongker_text = ft.Text("", color=ft.colors.WHITE)    
            selected_tiles_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )
            lake_adjuster = ft.Row([
                lake_text,
                ft.Column([
                    ft.ElevatedButton(text="↑", on_click=increment_lake_score),
                    ft.ElevatedButton(text="↓", on_click=decrement_lake_score)
                    ])
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                visible=False)

            add_tiles_panel.content = ft.Column([
                    tile_radio,
                    # ft.Divider(),
                    # modifier_radio,
                    # ft.Divider(),
                    # seal_radio,
                    all_tile_grid,
                    # ft.Row(
                    #     [all_tile_grid, lake_adjuster],
                    #     spacing=50),
                    selected_tiles_row,
                    ft.ElevatedButton(text="Add To Hand", on_click=add_selected_tiles_to_hand)
                ])

            all_tile_containers = []

            # filtered tiles
            for rank in all_tiles["bamboo"].keys():
                tile = all_tiles["bamboo"][rank]
                all_tile_containers.append(
                    ft.Container(
                        content=ft.Text(f"bamboo-{rank}", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_tile_select
                    )
                )

            for tile_container in all_tile_containers:
                all_tile_grid.controls.append(tile_container)

            # selected row
            refresh_selected_tiles()

            panel.controls.append(add_tiles_panel)

            # -------------------------------------------------------------
            # other scoring tab 
            # -------------------------------------------------------------
            other_scoring_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.RED_500,
                header=ft.ListTile(title=ft.Text(f"Other Scoring")),
                can_tap_header=True
            )

            other_scoring_panel.content = ft.Column([])

            scoring_tiles_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            refresh_other_scoring()
            
            other_scoring_panel.content.controls.append(scoring_tiles_row)
            panel.controls.append(other_scoring_panel)

            # -------------------------------------------------------------
            # current hand tab 
            # -------------------------------------------------------------
            
            current_hand_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.BLUE_800,
                header=ft.ListTile(title=ft.Text(f"Current Hand Scoring")),
                can_tap_header=True
            )

            mahjong_pts_adjuster = ft.Row([
                mahjong_pts_text,
                ft.Column([
                    ft.ElevatedButton(text="↑", on_click=increment_mahjong_pts),
                    ft.ElevatedButton(text="↓", on_click=decrement_mahjong_pts)
                    ])
                ],
                alignment=ft.MainAxisAlignment.START)

            mahjong_money_adjuster = ft.Row([
                mahjong_money_text,
                ft.Column([
                    ft.ElevatedButton(text="↑", on_click=increment_mahjong_money),
                    ft.ElevatedButton(text="↓", on_click=decrement_mahjong_money)
                    ])
                ],
                alignment=ft.MainAxisAlignment.START)

            current_hand_panel.content = ft.Column([])
            refresh_current_hand()
            
            panel.controls.append(current_hand_panel)
            
            page.views.append(
                ft.View(
                    "/scorer",
                    [
                        panel,
                        ft.NavigationBar(destinations=[
                            ft.NavigationBarDestination(icon=ft.icons.QUERY_STATS, label="Stats"),
                            ft.NavigationBarDestination(icon=ft.icons.ADD_TO_PHOTOS, label="Inventory"),
                            ft.NavigationBarDestination(icon=ft.icons.CALCULATE, label="Scorer"),
                            ft.NavigationBarDestination(icon=ft.icons.ADD_SHOPPING_CART, label="Shop"),
                            ],
                            on_change=go_to_page,
                            selected_index=2)
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )

        
        page.update()

        # -------------------------------------------------------------
        # SHOP Page
        # -------------------------------------------------------------
        if page.route == "/shop":
            # expansion panel list
            panel = ft.ExpansionPanelList(
                expand_icon_color=ft.colors.AMBER,
                elevation=1,
                divider_color=ft.colors.AMBER,
                expanded_header_padding=ft.padding.symmetric(0.0, 0.0)
            )

            # -------------------------------------------------------------
            # shop tab NEEDS TO KEEP STATE
            # -------------------------------------------------------------

            shop_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.GREY_500,
                header=ft.ListTile(title=ft.Text(f"Shop")),
                can_tap_header=True
            )

            shop_row = ft.GridView(
                # expand=1,
                height=100,
                width=800,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            shop_info_column = ft.Column()

            my_mahjongkers_shop_row = ft.GridView(
                # expand=1,
                height=100,
                width=500,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )
            item_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            item_info_column = ft.Column()

            my_items_shop_row = ft.GridView(
                # expand=1,
                height=100,
                width=200,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )
            shop_zodiac_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )
            
            shop_trigram_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            trigram_info_column = ft.Column()

            refresh_shop_button = ft.ElevatedButton(text=f"Refill Shop", on_click=refill_shop_mahjongkers)
            shop_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            shop_sell_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            shop_item_text = ft.Text("", color=ft.colors.WHITE)
            shop_money_text = ft.Text(f"Money: {money}", size=30)
            shop_tier_text = ft.Text(f"Shop Tier: {shop_round}", size=30)
            shop_zodiac_text = ft.Text("", color=ft.colors.WHITE)
            shop_trigram_text = ft.Text("", color=ft.colors.WHITE)
            item_pack_button = ft.ElevatedButton(text=f"Buy Item Pack - ${ITEM_COST}")
            trigram_pack_button = ft.ElevatedButton(text=f"Buy Trigram Pack - ${TRIGRAM_COST}")
            hand_size_upgrade_button = ft.ElevatedButton(text=f"Upgrade Hand Size - ${HAND_SIZE_COSTS[hand_size_level]}", on_click=upgrade_hand_size)
            # hand_size_upgrade_button = ft.ElevatedButton(text=f"Upgrade Hand Size - $ Check your own app!")
            sequence_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            sequence_current_text = ft.Text(f"{sequence_hand_mult}")
            triplet_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            triplet_current_text = ft.Text(f"{triplet_hand_mult}")
            half_flush_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            half_flush_current_text = ft.Text(f"{half_flush_hand_mult}")
            flush_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            flush_current_text = ft.Text(f"{flush_hand_mult}")
            avatar_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            shop_panel.content = ft.Column([
                ft.Row([
                    # shop_money_text,
                    shop_tier_text,
                    ft.Column([
                        ft.ElevatedButton(text="↑", on_click=increment_shop_tier),
                        ft.ElevatedButton(text="↓", on_click=decrement_shop_tier)
                        ]),
                    refresh_shop_button,
                ]),
                ft.Divider(),
                ft.Text("Mahjongkers", size=20, color=ft.colors.WHITE),
                shop_row,
                ft.Row([
                    ft.ElevatedButton(text="Buy", on_click=buy_mahjongker),
                    shop_mahjongker_text]),
                shop_info_column,
                ft.Divider(),
                # ft.Row([
                #     ft.Text("Items ", size=20, color=ft.colors.WHITE),
                #     ]),
                # ft.Row([
                #     item_row,
                #     # ft.Column([ft.Text("Inventory", size=20, color=ft.colors.WHITE), my_items_shop_row])],
                #     ],
                #     spacing=90),
                # ft.Row([
                #     ft.ElevatedButton(text="Buy", on_click=buy_item),
                #     shop_item_text
                # ]),
                # item_info_column,
                item_pack_button,
                ft.Divider(),
                # ft.Row([
                #     # ft.Text("Zodiacs", size=20, color=ft.colors.WHITE),
                #     ft.Text("Trigrams", size=20, color=ft.colors.WHITE)],
                #     spacing=450),
                # ft.Row([
                #     # shop_zodiac_row,
                #     shop_trigram_row],
                #     spacing=120),
                # ft.Row([
                #     # ft.Row([ft.ElevatedButton(text="Buy", on_click=buy_zodiac),
                #     #     shop_zodiac_text]),
                #     ft.Row([ft.ElevatedButton(text="Buy", on_click=buy_trigram),
                #         shop_trigram_text]),
                #     ],
                #     spacing=450),
                # trigram_info_column,
                # trigram_pack_button,
                # ft.Divider(),
                ft.Row([
                    ft.Text("Hand Size Upgrade (+1)", size=20, color=ft.colors.WHITE),
                    ]),
                ft.Row([
                    hand_size_upgrade_button
                    ]),
                ft.Divider(),
                # ft.Row([
                #     ft.Text("Hand Type Upgrades", size=20, color=ft.colors.WHITE),
                #     ]),
                # ft.Row(
                #     [ft.DataTable(
                #     columns=[
                #         ft.DataColumn(ft.Text("Hand")),
                #         ft.DataColumn(ft.Text("Amount")),
                #         ft.DataColumn(ft.Text("Current")),
                #         ft.DataColumn(ft.Text("Cost")),
                #     ],
                #     rows=[
                #         ft.DataRow(
                #             cells=[
                #                 ft.DataCell(ft.Text("Sequence")),
                #                 ft.DataCell(ft.Text(f"+{SEQUENCE_UPGRADE_AMOUNT}", color=ft.colors.WHITE)),
                #                 ft.DataCell(sequence_current_text),
                #                 ft.DataCell(sequence_button)
                #             ]
                #         ),
                #         ft.DataRow(
                #             cells=[
                #                 ft.DataCell(ft.Text("Triplet")),
                #                 ft.DataCell(ft.Text(f"+{TRIPLET_UPGRADE_AMOUNT}", color=ft.colors.WHITE)),
                #                 ft.DataCell(triplet_current_text),
                #                 ft.DataCell(triplet_button)
                #             ]
                #         ),
                #         ft.DataRow(
                #             cells=[
                #                 ft.DataCell(ft.Text("Half Flush")),
                #                 ft.DataCell(ft.Text(f"+{HALF_FLUSH_UPGRADE_AMOUNT}", color=ft.colors.WHITE)),
                #                 ft.DataCell(half_flush_current_text),
                #                 ft.DataCell(half_flush_button)
                #             ]
                #         ),
                #         ft.DataRow(
                #             cells=[
                #                 ft.DataCell(ft.Text("Flush")),
                #                 ft.DataCell(ft.Text(f"+{FLUSH_UPGRADE_AMOUNT}", color=ft.colors.WHITE)),
                #                 ft.DataCell(flush_current_text),
                #                 ft.DataCell(flush_button)
                #             ]
                #         ),
                #         ft.DataRow(
                #             cells=[
                #                 ft.DataCell(ft.Text("All")),
                #                 ft.DataCell(ft.Text(f"+0.x", color=ft.colors.WHITE)),
                #                 ft.DataCell(ft.Text(f"+y.z", color=ft.colors.WHITE)),
                #                 ft.DataCell(avatar_button)
                #             ]
                #         ),
                #     ]) 
                # ])
            ])

            if hand_upgrade_enabled:
                enable_hand_upgrade_buy()
            else:
                disable_hand_upgrade_buy()

            if shop_selected_i:
                for i in shop_selected_i:
                    mahjongker = all_mahjongkers_list[i]
                    shop_row.controls.append(
                        ft.Container(
                                image=ft.DecorationImage(src=mahjongker.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                                content=ft.Text(f"{mahjongker.name} - ${mahjongker.cost}", bgcolor="#000000", color=ft.colors.WHITE),
                                border_radius=ft.border_radius.all(5),
                                ink=True,
                                on_click=handle_add_shop_mahjongker_select,
                                tooltip=ft.Tooltip(
                                    message=f"${mahjongker.cost} - {mahjongker.description}",
                                    padding=20,
                                    border_radius=10,
                                    text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.Alignment(0.8, 1),
                                        colors=[
                                            "0xff1f005c",
                                            "0xff5b0060",
                                            "0xff870160",
                                            "0xffac255e",
                                            "0xffca485c",
                                            "0xffe16b5c",
                                            "0xfff39060",
                                            "0xffffb56b",
                                        ],
                                        tile_mode=ft.GradientTileMode.MIRROR,
                                    )
                                )
                            )
                        )
                    shop_info_column.controls.append(ft.Text(f"${mahjongker.cost} - {mahjongker.name} : {mahjongker.description}", color=ft.colors.WHITE, size=20))
            else:
                for i in range(7):
                    shop_row.controls.append(
                        ft.Container(
                            image=ft.DecorationImage(src="/jongker/sold.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                            border_radius=ft.border_radius.all(5),
                            ink=True,
                        )
                    )
            shop_row.controls.append(ft.FloatingActionButton(text=f"${reroll_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_mahjongkers))

            if item_selected:
                for item in item_selected:
                    item_row.controls.append(
                        ft.Container(
                            image=ft.DecorationImage(src=item.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                            content=ft.Text(f"{item.name} - ${item.cost}", bgcolor="#000000", color=ft.colors.WHITE),
                            border_radius=ft.border_radius.all(5),
                            ink=True,
                            on_click=handle_add_shop_item_select,
                            tooltip=ft.Tooltip(
                                message=f"{item.description}",
                                padding=20,
                                border_radius=10,
                                text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                                gradient=ft.LinearGradient(
                                    begin=ft.alignment.top_left,
                                    end=ft.alignment.Alignment(0.8, 1),
                                    colors=[
                                        "0xff1f005c",
                                        "0xff5b0060",
                                        "0xff870160",
                                        "0xffac255e",
                                        "0xffca485c",
                                        "0xffe16b5c",
                                        "0xfff39060",
                                        "0xffffb56b",
                                    ],
                                    tile_mode=ft.GradientTileMode.MIRROR,
                                )
                            )
                        )
                    )
                    item_info_column.controls.append(ft.Text(f"${item.cost} - {item.name} : {item.description}", color=ft.colors.WHITE, size=20))
            else:
                for i in range(3):
                    item_row.controls.append(
                        ft.Container(
                            image=ft.DecorationImage(src="/jongker/sold.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                            border_radius=ft.border_radius.all(5),
                            ink=True,
                        )
                    )
            item_row.controls.append(ft.FloatingActionButton(text=f"${reroll_item_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_items))

            # if zodiac_selected:
                # for zodiac in zodiac_selected:
            #         shop_zodiac_row.controls.append(
            #             ft.Container(
            #                     image=ft.DecorationImage(src=zodiac.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
            #                     content=ft.Text(f"{zodiac.name}", bgcolor="#000000", color=ft.colors.WHITE),
            #                     border_radius=ft.border_radius.all(5),
            #                     ink=True,
            #                     on_click=handle_add_shop_zodiac_select,
            #                     tooltip=ft.Tooltip(
            #                         message=f"${zodiac.cost} - {zodiac.description}",
            #                         padding=20,
            #                         border_radius=10,
            #                         text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
            #                         gradient=ft.LinearGradient(
            #                             begin=ft.alignment.top_left,
            #                             end=ft.alignment.Alignment(0.8, 1),
            #                             colors=[
            #                                 "0xff1f005c",
            #                                 "0xff5b0060",
            #                                 "0xff870160",
            #                                 "0xffac255e",
            #                                 "0xffca485c",
            #                                 "0xffe16b5c",
            #                                 "0xfff39060",
            #                                 "0xffffb56b",
            #                             ],
            #                             tile_mode=ft.GradientTileMode.MIRROR,
            #                         )
            #                     )
            #                 )
            #             )
            # else:
            #     for i in range(3):
            #         shop_zodiac_row.controls.append(
            #             ft.Container(
            #                 image=ft.DecorationImage(src="/jongker/sold.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
            #                 border_radius=ft.border_radius.all(5),
            #                 ink=True,
            #             )
            #         )
            # shop_zodiac_row.controls.append(ft.FloatingActionButton(text=f"${current_zodiac_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_zodiacs))

            if trigram_selected:
                for trigram in trigram_selected:
                    shop_trigram_row.controls.append(
                        ft.Container(
                                image=ft.DecorationImage(src=trigram.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                                content=ft.Text(f"{trigram.name}", bgcolor="#000000", color=ft.colors.WHITE),
                                border_radius=ft.border_radius.all(5),
                                ink=True,
                                on_click=handle_add_shop_trigram_select,
                                tooltip=ft.Tooltip(
                                    message=f"${trigram.cost} - {trigram.description}",
                                    padding=20,
                                    border_radius=10,
                                    text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                                    gradient=ft.LinearGradient(
                                        begin=ft.alignment.top_left,
                                        end=ft.alignment.Alignment(0.8, 1),
                                        colors=[
                                            "0xff1f005c",
                                            "0xff5b0060",
                                            "0xff870160",
                                            "0xffac255e",
                                            "0xffca485c",
                                            "0xffe16b5c",
                                            "0xfff39060",
                                            "0xffffb56b",
                                        ],
                                        tile_mode=ft.GradientTileMode.MIRROR,
                                    )
                                )
                            )
                        )
                    trigram_info_column.controls.append(ft.Text(f"${trigram.cost} - {trigram.name} : {trigram.description}", color=ft.colors.WHITE, size=20))
            else:
                for i in range(3):
                    shop_trigram_row.controls.append(
                        ft.Container(
                            image=ft.DecorationImage(src="/jongker/sold.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                            border_radius=ft.border_radius.all(5),
                            ink=True,
                        )
                    )
            shop_trigram_row.controls.append(ft.FloatingActionButton(text=f"${current_trigram_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_trigrams))

            panel.controls.append(shop_panel)

            # -------------------------------------------------------------
            # item roll tab 
            # -------------------------------------------------------------
            item_roll_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.PURPLE_300,
                header=ft.ListTile(title=ft.Text(f"Item Roll")),
                can_tap_header=True
            )

            item_pack_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            item_pack_info_column = ft.Column()

            # set up base row
            for i in range(3):
                item_pack_row.controls.append(
                    ft.Container(
                        content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        )
                    )
            item_pack_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_items))
            item_roll_text = ft.Text("", color=ft.colors.WHITE)
            item_roll_panel.content = ft.Row([ft.Column([
                    item_pack_row,
                    item_pack_info_column
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START)])

            panel.controls.append(item_roll_panel)

            # -------------------------------------------------------------
            # free trigram tab 
            # -------------------------------------------------------------
            trigram_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.RED_500,
                header=ft.ListTile(title=ft.Text(f"Trigram Roll")),
                can_tap_header=True
            )

            trigram_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            trigram_pack_info_column = ft.Column()

            # set up base row
            for i in range(3):
                trigram_row.controls.append(
                    ft.Container(
                        content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        )
                    )
            trigram_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_trigrams))
            trigram_text = ft.Text("", color=ft.colors.WHITE)
            trigram_panel.content = ft.Column([
                    trigram_row,
                    trigram_pack_info_column
                ])

            panel.controls.append(trigram_panel)

            # -------------------------------------------------------------
            # common mahjongker tab 
            # -------------------------------------------------------------

            first_mahjongker_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.BLUE_500,
                header=ft.ListTile(title=ft.Text(f"Common Mahjongker Roll")),
                can_tap_header=True
            )

            common_mahjongkers_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            # set up base row
            for i in range(3):
                common_mahjongkers_row.controls.append(
                    ft.Container(
                        content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        )
                    )
            common_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_common_mahjongkers))
            common_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            first_mahjongker_panel.content = ft.Column([
                    common_mahjongkers_row,
                    ft.Row([
                        ft.ElevatedButton(text="Select", on_click=add_common_mahjongker),
                        common_mahjongker_text
                    ])
                ])

            panel.controls.append(first_mahjongker_panel)


            # -------------------------------------------------------------
            # uncommon mahjongker tab 
            # -------------------------------------------------------------

            uncommon_mahjongker_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.GREEN_500,
                header=ft.ListTile(title=ft.Text(f"Uncommon Mahjongker Roll")),
                can_tap_header=True
            )

            uncommon_mahjongkers_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            # set up base row
            for i in range(3):
                uncommon_mahjongkers_row.controls.append(
                    ft.Container(
                        content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        )
                    )
            uncommon_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_uncommon_mahjongkers))
            uncommon_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            uncommon_mahjongker_panel.content = ft.Column([
                    uncommon_mahjongkers_row,
                    ft.Row([
                        ft.ElevatedButton(text="Select", on_click=add_uncommon_mahjongker),
                        uncommon_mahjongker_text
                    ])
                ])

            panel.controls.append(uncommon_mahjongker_panel)

            # -------------------------------------------------------------
            # rare mahjongker tab 
            # -------------------------------------------------------------

            rare_mahjongker_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.PURPLE_500,
                header=ft.ListTile(title=ft.Text(f"Rare Mahjongker Roll")),
                can_tap_header=True
            )

            rare_mahjongkers_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            # set up base row
            for i in range(3):
                rare_mahjongkers_row.controls.append(
                    ft.Container(
                        content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        )
                    )
            rare_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_rare_mahjongkers))
            rare_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            rare_mahjongker_panel.content = ft.Column([
                    rare_mahjongkers_row,
                    ft.Row([
                        ft.ElevatedButton(text="Select", on_click=add_rare_mahjongker),
                        rare_mahjongker_text
                    ])
                ])

            panel.controls.append(rare_mahjongker_panel)

            # -------------------------------------------------------------
            # free zodiac tab 
            # -------------------------------------------------------------
            zodiac_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.RED_500,
                header=ft.ListTile(title=ft.Text(f"Zodiac Roll")),
                can_tap_header=True
            )

            zodiac_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            # set up base row
            for i in range(3):
                zodiac_row.controls.append(
                    ft.Container(
                        content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        )
                    )
            zodiac_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_zodiacs))
            zodiac_text = ft.Text("", color=ft.colors.WHITE)
            zodiac_panel.content = ft.Column([
                    zodiac_row,
                    ft.Row([
                        ft.ElevatedButton(text="Select", on_click=select_zodiac),
                        rare_mahjongker_text
                    ])
                ])

            panel.controls.append(zodiac_panel)

            # -------------------------------------------------------------
            # jongkers panel for comp shop selling
            # -------------------------------------------------------------

            panel.controls.append(my_jongkers_panel)

            # -------------------------------------------------------------
            # initial mahjongker tab 
            # -------------------------------------------------------------

            first_mahjongker_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.ORANGE_500,
                header=ft.ListTile(title=ft.Text(f"Initial Mahjongker Roll")),
                can_tap_header=True
            )

            initial_mahjongkers_row = ft.GridView(
                # expand=1,
                height=100,
                width=1100,
                runs_count=1,
                max_extent=95,
                child_aspect_ratio=1.0,
                spacing=5,
                run_spacing=5,
            )

            initial_mahjongker_info_column = ft.Column()

            # set up base row
            for i in range(10):
                initial_mahjongkers_row.controls.append(
                    ft.Container(
                        content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        )
                    )
            initial_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.CHECK, on_click=refresh_initial_mahjongkers))
            initial_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            first_mahjongker_panel.content = ft.Column([
                    initial_mahjongkers_row,
                    ft.Row([
                        ft.ElevatedButton(text="Select", on_click=add_initial_mahjongker),
                        initial_mahjongker_text
                    ]),
                    initial_mahjongker_info_column
                ])

            panel.controls.append(first_mahjongker_panel)

            page.views.append(
                ft.View(
                    "/shop",
                    [
                        panel,
                        ft.NavigationBar(destinations=[
                            ft.NavigationBarDestination(icon=ft.icons.QUERY_STATS, label="Stats"),
                            ft.NavigationBarDestination(icon=ft.icons.ADD_TO_PHOTOS, label="Inventory"),
                            ft.NavigationBarDestination(icon=ft.icons.CALCULATE, label="Scorer"),
                            ft.NavigationBarDestination(icon=ft.icons.ADD_SHOPPING_CART, label="Shop"),
                            ],
                            on_change=go_to_page,
                            selected_index=3)
                    ],
                    scroll=ft.ScrollMode.AUTO
                )
            )

            page.update()


    #------------------------
    # Other settings
    #------------------------       

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.scroll = ft.ScrollMode.AUTO
    # page.auto_scroll = True

    page.go("/stats")

ft.app(target=main, assets_dir="assets")
