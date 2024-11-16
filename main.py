import flet as ft
import time
import random
from items import *
from mahscorer import *

# -------------------------------------------------------------
# GLOBAL VARS
# -------------------------------------------------------------

# global scoring
HAND_TYPE_UPGRADE_MULT = 1.5
HAND_SIZE_COSTS = [6,11,16,26]
SEQUENCE_UPGRADE_COST = 3
TRIPLET_UPGRADE_COST = 3
HALF_FLUSH_UPGRADE_COST = 3
FLUSH_UPGRADE_COST = 3
AVATAR_UPGRADE_COST = 10
ITEM_COST = 3
MAX_NUM_MAHJONGKERS = 5
SEQUENCE_UPGRADE_AMOUNT = 0.5
TRIPLET_UPGRADE_AMOUNT = 0.7
HALF_FLUSH_UPGRADE_AMOUNT = 0.7
FLUSH_UPGRADE_AMOUNT = 1.0

# hands
sequence_hand_level = 0
triplet_hand_level = 0
half_flush_hand_level = 0
flush_hand_level = 0
hand_size_level = 0
sequence_hand_mult = 1.5
triplet_hand_mult = 2.0
half_flush_hand_mult = 2.0
flush_hand_mult = 3.0

# stats
money = 0
total_score = 0
hand_size = 10
money_text = ft.Text(money, size=80)
score_text = ft.Text(total_score, size=80)
hand_size_text = ft.Text(hand_size, size=80)
score_adjust_tf = []
sequence_mult_text = []
triplet_mult_text = []
half_flush_mult_text = []
flush_mult_text = []

# mahjongkers
my_mahjongkers = []
filtered_mahjongkers_list = []
all_mahjongker_text = []
all_mahjongkers_containers = []
my_mahjongker_text = []
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

# scorer
selected_tiles = []
current_hand = Hand()
table_wind = all_tiles["wind"]["east"]
seat_wind = all_tiles["wind"]["east"]
hand_score_text = ft.Text(f"Score: 0", size=20)
add_tiles_panel = []
tile_radio = []
all_tile_grid = []
selected_tiles_row = []
all_tile_containers = []
other_scoring_panel = []
scoring_tiles_row = []
current_hand_panel = []
tot_score = 0

# shop
initial_mahjongkers_row = []
initial_mahjongker_text = ""
shop_row = []
item_row = []
shop_mahjongker_text = ""
reroll_cost = 1
shop_money_text = ""
hand_size_upgrade_button = []
shop_selected_i = []
item_selected = []
sequence_button = []
triplet_button = []
half_flush_button = []
flush_button = []
avatar_button = []
hand_upgrade_enabled = True

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
            page.go("/mahjongkers")
        elif e.control.selected_index == 2:
            page.go("/scorer")
        else:
            page.go("/shop")

    # -------------------------------------------------------------
    # STATS FUNC
    # -------------------------------------------------------------

    def increment_money(e):
        global money
        money += 1
        money_text.value = str(money)
        page.update()

    def decrement_money(e):
        global money
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
        sequence_hand_mult = sequence_hand_mult + SEQUENCE_UPGRADE_AMOUNT
        sequence_mult_text.value = str(sequence_hand_mult)
        page.update()

    def increment_triplet_mult(e):
        global triplet_hand_mult
        global triplet_mult_text
        triplet_hand_mult = triplet_hand_mult + TRIPLET_UPGRADE_AMOUNT
        triplet_mult_text.value = str(triplet_hand_mult)
        page.update()

    def increment_half_flush_mult(e):
        global half_flush_hand_mult
        global half_flush_mult_text
        half_flush_hand_mult = half_flush_hand_mult + HALF_FLUSH_UPGRADE_AMOUNT
        half_flush_mult_text.value = str(half_flush_hand_mult)
        page.update()

    def increment_flush_mult(e):
        global flush_hand_mult
        global flush_mult_text
        flush_hand_mult = flush_hand_mult + FLUSH_UPGRADE_AMOUNT
        flush_mult_text.value = str(flush_hand_mult)
        page.update()

    def decrement_sequence_mult(e):
        global sequence_hand_mult
        global sequence_mult_text
        sequence_hand_mult = sequence_hand_mult - SEQUENCE_UPGRADE_AMOUNT
        sequence_mult_text.value = str(sequence_hand_mult)
        page.update()

    def decrement_triplet_mult(e):
        global triplet_hand_mult
        global triplet_mult_text
        triplet_hand_mult = triplet_hand_mult - TRIPLET_UPGRADE_AMOUNT
        triplet_mult_text.value = str(triplet_hand_mult)
        page.update()


    def decrement_half_flush_mult(e):
        global half_flush_hand_mult
        global half_flush_mult_text
        half_flush_hand_mult = half_flush_hand_mult - HALF_FLUSH_UPGRADE_AMOUNT
        half_flush_mult_text.value = str(half_flush_hand_mult)
        page.update()

    def decrement_flush_mult(e):
        global flush_hand_mult
        global flush_mult_text
        flush_hand_mult = flush_hand_mult - FLUSH_UPGRADE_AMOUNT
        flush_mult_text.value = str(flush_hand_mult)
        page.update()

    # -------------------------------------------------------------
    # MAHJONGKER FUNC
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
        aycker.point_value = aycker.point_value + 15
        aycker_text.value = f"AYCker value: {aycker.point_value}"
        page.update()

    def decrement_aycker_score(e):
        global aycker_text
        aycker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "AYCker":
                aycker = mahjongker
                break
        aycker.point_value = max(0, aycker.point_value - 15)
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
        pingker.point_value = pingker.point_value + 20
        pingker_text.value = f"Pingker value: {pingker.point_value}"
        page.update()

    def decrement_pingker_score(e):
        global pingker_text
        pingker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Pingker":
                pingker = mahjongker
                break
        pingker.point_value = max(0, pingker.point_value - 20)
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
        kingkongker.point_value = kingkongker.point_value + 40
        kingkongker_text.value = f"KingKongker value: {kingkongker.point_value}"
        page.update()

    def decrement_kingkongker_score(e):
        global kingkongker_text
        kingkongker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "KingKongker":
                kingkongker = mahjongker
                break
        kingkongker.point_value = max(0, kingkongker.point_value - 40)
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
        meldker.point_value = meldker.point_value + 30
        meldker_text.value = f"Meldker value: {meldker.point_value}"
        page.update()

    def decrement_meldker_score(e):
        global meldker_text
        meldker = []
        for mahjongker in my_mahjongkers:
            if mahjongker.name == "Meldker":
                meldker = mahjongker
                break
        meldker.point_value = max(0, meldker.point_value - 30)
        meldker_text.value = f"Meldker value: {meldker.point_value}"
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
        tile_suit = e.control.image.src.split("/")[2].split(".")[0].split("-")[0]
        tile_rank = e.control.image.src.split("/")[2].split(".")[0].split("-")[1]
        tile = all_tiles[tile_suit][tile_rank]
        if len(selected_tiles) < 4:
            selected_tiles.append(tile)
        refresh_selected_tiles()
        page.update()

    def handle_remove_tile(e):
        global selected_tiles
        tile_suit = e.control.image.src.split("/")[2].split(".")[0].split("-")[0]
        tile_rank = e.control.image.src.split("/")[2].split(".")[0].split("-")[1]
        tile = all_tiles[tile_suit][tile_rank]
        selected_tiles.remove(tile)    
        refresh_selected_tiles()
        page.update()        

    def handle_tile_filter(e):
        all_tile_containers.clear()
        all_tile_grid.controls.clear()
        print(tile_radio.value)
        if tile_radio.value == "honor":
            for rank in all_tiles["dragon"].keys():
                tile = all_tiles["dragon"][rank]
                all_tile_containers.append(
                    ft.Container(
                        content=ft.Text(f"dragon-{tile.rank}", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src=tile.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        on_click=handle_add_tile_select,
                    )
                )
            for rank in all_tiles["wind"].keys():
                tile = all_tiles["wind"][rank]
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
            for rank in all_tiles[tile_radio.value].keys():
                tile = all_tiles[tile_radio.value][rank]
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
            print("is eyes")
            eyes = Eyes()
            for tile in selected_tiles:
                eyes.add_tile(tile)
            current_hand.add_eyes(eyes)
        else:
            print ("is meld")
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

        global hand_score_text
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
        i = score(current_hand, table_wind, seat_wind, my_mahjongkers, sequence_hand_mult, triplet_hand_mult, half_flush_hand_mult, flush_hand_mult)
        tot_score = i[0] * i[1]
        hand_score_text.value =  f"Score: {i[0]} x {i[1]} = {tot_score}"
        page.update()

    def add_to_total_score(e):
        global total_score
        global tot_score
        total_score += tot_score
        tot_score = 0
        hand_score_text.value =  f"Score: 0"
        score_text.value = str(total_score)
        current_hand.melds = []
        current_hand.eyes = []
        refresh_current_hand()

    # -------------------------------------------------------------
    # SHOP FUNC
    # -------------------------------------------------------------
    def refresh_initial_mahjongkers(e):
        global initial_mahjongkers_row
        initial_mahjongkers_row.controls.clear()
        i = 0
        selected_i = []
        while i < 3:
            index = random.randint(0,len(common_mahjongkers_list)-1)
            if index not in selected_i: 
                selected_i.append(index)
                i = i+1

        for i in selected_i:
            mahjongker = common_mahjongkers_list[i]
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
        initial_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_initial_mahjongkers))
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
        initial_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_initial_mahjongkers))
        page.update()

    def handle_add_initial_mahjongker_select(e):
        global initial_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        initial_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def add_initial_mahjongker(e):
        global my_mahjongkers
        global initial_mahjongker_text
        if initial_mahjongker_text.value != "":
            my_mahjongkers.append(all_mahjongkers_dict[initial_mahjongker_text.value.lower()])
        initial_mahjongker_text.value = ""
        refresh_my_mahjongkers()
        refresh_initial_mahjongkers_empty()

    def refresh_shop(e):
        global shop_row
        global reroll_cost
        global shop_selected_i
        global my_mahjongkers
        shop_row.controls.clear()
        i = 0
        shop_selected_i = []
        while i < 3:
            index = random.randint(0,len(all_mahjongkers_list)-1)
            if index not in shop_selected_i: 
                mahjongker = all_mahjongkers_list[index]
                if mahjongker not in my_mahjongkers:
                    shop_selected_i.append(index)
                    i = i+1

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
        reroll_cost = 1
        shop_row.controls.append(ft.FloatingActionButton(text=f"${reroll_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_mahjongkers))
        page.update()
        enable_hand_upgrade_buy()

    def reroll_shop_mahjongkers(e):
        global my_mahjongkers
        global reroll_cost
        global shop_row
        global shop_selected_i
        global money
        if money >= reroll_cost:
            money = money - reroll_cost
            refresh_money_text()
            reroll_cost += 1
            shop_row.controls.clear()
            i = 0
            shop_selected_i = []
            while i < 3:
                index = random.randint(0,len(all_mahjongkers_list)-1)
                if index not in shop_selected_i: 
                    mahjongker = all_mahjongkers_list[index]
                    if mahjongker not in my_mahjongkers:
                        shop_selected_i.append(index)
                        i = i+1

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
            shop_row.controls.append(ft.FloatingActionButton(text=f"${reroll_cost}", icon=ft.icons.REFRESH, on_click=reroll_shop_mahjongkers))
            page.update()

    def handle_add_shop_mahjongker_select(e):
        global shop_mahjongker_text
        jonker_name = e.control.image.src.split("/")[2].split(".")[0]
        shop_mahjongker_text.value = all_mahjongkers_dict[jonker_name].name
        page.update()

    def buy_mahjongker(e):
        global my_mahjongkers
        global shop_mahjongker_text
        global money
        global shop_row
        selected_container = []
        if shop_mahjongker_text.value != "" and shop_mahjongker_text.value != "TOO POOR":
            mahjongker = all_mahjongkers_dict[shop_mahjongker_text.value.lower()]
            if money >= mahjongker.cost:
                my_mahjongkers.append(mahjongker)
                money = money - mahjongker.cost
                # then replace this slot in the grid view
                for container in shop_row.controls:
                    # print(container.content.value)
                    if mahjongker.name in container.content.value:
                        selected_container = container
                        break
                refresh_money_text()
                shop_mahjongker_text.value = ""
                selected_container.image="/jongker/sold.png"
                selected_container.content.value= "SOLD"
            else:
                shop_mahjongker_text.value = "TOO POOR"
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
            sequence_hand_mult = sequence_hand_mult + SEQUENCE_UPGRADE_AMOUNT
            refresh_money_text()
            # disable_hand_upgrade_buy()

    def upgrade_triplet(e):
        global money
        global triplet_hand_mult
        if money >= TRIPLET_UPGRADE_COST:
            money = money - TRIPLET_UPGRADE_COST
            # triplet_hand_mult = triplet_hand_mult * HAND_TYPE_UPGRADE_MULT
            triplet_hand_mult = triplet_hand_mult + TRIPLET_UPGRADE_AMOUNT
            refresh_money_text()
            # disable_hand_upgrade_buy()

    def upgrade_half_flush(e):
        global money
        global half_flush_hand_mult
        if money >= HALF_FLUSH_UPGRADE_COST:
            money = money - HALF_FLUSH_UPGRADE_COST
            # half_flush_hand_mult = half_flush_hand_mult * HAND_TYPE_UPGRADE_MULT
            half_flush_hand_mult = half_flush_hand_mult + HALF_FLUSH_UPGRADE_AMOUNT
            refresh_money_text()
            # disable_hand_upgrade_buy()

    def upgrade_flush(e):
        global money
        global flush_hand_mult
        if money >= FLUSH_UPGRADE_COST:
            money = money - FLUSH_UPGRADE_COST
            # flush_hand_mult = flush_hand_mult * HAND_TYPE_UPGRADE_MULT
            flush_hand_mult = flush_hand_mult + FLUSH_UPGRADE_AMOUNT
            refresh_money_text()
            # disable_hand_upgrade_buy()

    def upgrade_avatar(e):
        global money
        global sequence_hand_mult
        global triplet_hand_mult
        global half_flush_hand_mult
        global flush_hand_mult
        if money >= AVATAR_UPGRADE_COST:
            money = money - AVATAR_UPGRADE_COST
            sequence_hand_mult = sequence_hand_mult + SEQUENCE_UPGRADE_AMOUNT
            triplet_hand_mult = triplet_hand_mult + TRIPLET_UPGRADE_AMOUNT
            half_flush_hand_mult = half_flush_hand_mult + HALF_FLUSH_UPGRADE_AMOUNT
            flush_hand_mult = flush_hand_mult + FLUSH_UPGRADE_AMOUNT
            refresh_money_text()
            # disable_hand_upgrade_buy()

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
        sequence_button.text = "${0}".format(SEQUENCE_UPGRADE_COST)
        sequence_button.on_click = upgrade_sequence
        triplet_button.text = "${0}".format(TRIPLET_UPGRADE_COST)
        triplet_button.on_click = upgrade_triplet
        half_flush_button.text = "${0}".format(HALF_FLUSH_UPGRADE_COST)
        half_flush_button.on_click = upgrade_half_flush
        flush_button.text = "${0}".format(FLUSH_UPGRADE_COST)
        flush_button.on_click = upgrade_flush
        avatar_button.text = "${0}".format(AVATAR_UPGRADE_COST)
        avatar_button.on_click = upgrade_avatar
        hand_upgrade_enabled = True
        page.update()


    def buy_item(e):
        global money
        global item_selected
        global item_row
        if money >= ITEM_COST:
            item_selected = []
            item_row.controls = []
            money = money - ITEM_COST
            refresh_money_text()
            i = 0
            item_selected = []
            while i < 3:
                random_i = random.randint(0,len(all_items_list)-1)
                print(random_i)
                item = all_items_list[random_i]
                print(item)
                if item not in item_selected: 
                    item_selected.append(item)
                    i = i+1

            for item in item_selected:

                item_row.controls.append(
                    ft.Container(
                            image=ft.DecorationImage(src=item.img_src, fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                            content=ft.Text(f"{item.name}", bgcolor="#000000", color=ft.colors.WHITE),
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
            page.update()

    def handle_add_shop_item_select(e):
        item_row.controls = []
        for i in range(3):
            item_row.controls.append(
                ft.Container(
                    image=ft.DecorationImage(src="/jongker/sold.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                    border_radius=ft.border_radius.all(5),
                    ink=True,
                )
            )
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

    def do_nothing(e):
        print("I do nothing!")

    # -------------------------------------------------------------
    # PAGES - ROUTES HERE
    # -------------------------------------------------------------
    def route_change(e):
        global score_adjust_tf
        global money
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
        global my_mahjongkers
        global filtered_mahjongkers_list
        global all_mahjongker_text
        global all_mahjongker_grid
        global my_mahjongker_text
        global mahjongker_filter
        global my_mahjongker_grid
        global my_jongkers_panel
        global selected_tiles
        global current_hand
        global table_wind
        global seat_wind
        global hand_score_text
        global add_tiles_panel
        global tile_radio
        global all_tile_grid
        global selected_tiles_row
        global all_tile_containers
        global other_scoring_panel
        global scoring_tiles_row
        global current_hand_panel
        global initial_mahjongkers_row
        global initial_mahjongker_text
        global shop_row
        global item_row
        global shop_mahjongker_text
        global reroll_cost
        global shop_money_text
        global hand_size_upgrade_button
        global shop_selected_i
        global item_selected
        global sequence_button
        global triplet_button
        global half_flush_button
        global flush_button
        global avatar_button
        global hand_upgrade_enabled

        score_adjust_tf = ft.TextField(label="Score Adjust")
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
                        alignment=ft.MainAxisAlignment.CENTER),
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
                            ))
                        ],
                        alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row(
                        [
                            ft.DataTable(
                                columns=[
                                    ft.DataColumn(ft.Text("Hand")),
                                    ft.DataColumn(ft.Text("Mult")),
                                    ft.DataColumn(ft.Text("Adjust")),
                                ],
                                rows=[
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("Sequence")),
                                            ft.DataCell(sequence_mult_text),
                                            ft.DataCell(
                                                ft.Row([
                                                    ft.ElevatedButton(text="↑", on_click=increment_sequence_mult),
                                                    ft.ElevatedButton(text="↓", on_click=decrement_sequence_mult)
                                                    ])
                                            )
                                        ]
                                    ),
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("Triplet")),
                                            ft.DataCell(triplet_mult_text),
                                            ft.DataCell(
                                                ft.Row([
                                                    ft.ElevatedButton(text="↑", on_click=increment_triplet_mult),
                                                    ft.ElevatedButton(text="↓", on_click=decrement_triplet_mult)
                                                    ])
                                            )
                                        ]
                                    ),
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("Half Flush")),
                                            ft.DataCell(half_flush_mult_text),
                                            ft.DataCell(
                                                ft.Row([
                                                    ft.ElevatedButton(text="↑", on_click=increment_half_flush_mult),
                                                    ft.ElevatedButton(text="↓", on_click=decrement_half_flush_mult)
                                                    ])
                                            )
                                        ]
                                    ),
                                    ft.DataRow(
                                        cells=[
                                            ft.DataCell(ft.Text("Flush")),
                                            ft.DataCell(flush_mult_text),
                                            ft.DataCell(
                                                ft.Row([
                                                    ft.ElevatedButton(text="↑", on_click=increment_flush_mult),
                                                    ft.ElevatedButton(text="↓", on_click=decrement_flush_mult)
                                                    ])
                                            )
                                        ]
                                    ),
                                ]
                            )],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15), 

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
                        ft.NavigationBarDestination(icon=ft.icons.ADD_TO_PHOTOS, label="Mahjongkers"),
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
        if page.route == "/mahjongkers":
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
            # add jongkers tab 
            # -------------------------------------------------------------

            add_jongkers_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.BLUE_800,
                header=ft.ListTile(title=ft.Text("Add Jongkers")),
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
                    "/mahjongkers",
                    [
                        panel,
                        ft.NavigationBar(destinations=[
                            ft.NavigationBarDestination(icon=ft.icons.QUERY_STATS, label="Stats"),
                            ft.NavigationBarDestination(icon=ft.icons.ADD_TO_PHOTOS, label="Mahjongkers"),
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
            )

            tile_radio = ft.RadioGroup(content=ft.Row([
                ft.Radio(value="bamboo", label="Bamboo"),
                ft.Radio(value="dot", label="Dot"),
                ft.Radio(value="character", label="Character"),
                ft.Radio(value="honor", label="Honor")      
            ]),
            value="bamboo",
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

            add_tiles_panel.content = ft.Column([
                    tile_radio,
                    all_tile_grid,
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
                bgcolor=ft.colors.GREEN_500,
                header=ft.ListTile(title=ft.Text(f"Other Scoring")),
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
                bgcolor=ft.colors.GREEN_500,
                header=ft.ListTile(title=ft.Text(f"Current Hand Scoring")),
            )

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
                            ft.NavigationBarDestination(icon=ft.icons.ADD_TO_PHOTOS, label="Mahjongkers"),
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
                bgcolor=ft.colors.GREEN_500,
                header=ft.ListTile(title=ft.Text(f"Shop")),
            )

            shop_row = ft.GridView(
                # expand=1,
                height=100,
                width=400,
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
            shop_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            shop_money_text = ft.Text(f"Money: {money}", size=30)
            hand_size_upgrade_button = ft.ElevatedButton(text=f"Upgrade Hand Size - ${HAND_SIZE_COSTS[hand_size_level]}", on_click=upgrade_hand_size)
            sequence_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            triplet_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            half_flush_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            flush_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            avatar_button = ft.ElevatedButton(text="x", on_click=do_nothing)
            shop_panel.content = ft.Column([
                ft.Row([
                    shop_money_text,
                    ft.ElevatedButton(text="Refresh Shop", on_click=refresh_shop)
                ]),
                ft.Divider(),
                ft.Row([
                    ft.Text("Mahjongkers", size=20, color=ft.colors.WHITE),
                    ]),
                shop_row,
                ft.Row([
                    ft.ElevatedButton(text="Buy", on_click=buy_mahjongker),
                    shop_mahjongker_text
                ]),
                ft.Divider(),
                ft.Row([
                    ft.Text("Item Pack ", size=20, color=ft.colors.WHITE),
                    ]),
                ft.Column([
                    ft.ElevatedButton(text=f"Buy Item - ${ITEM_COST}", on_click=buy_item),
                    ],
                    spacing=50),
                item_row,
                ft.Divider(),
                ft.Row([
                    ft.Text("Hand Size Upgrade", size=20, color=ft.colors.WHITE),
                    ]),
                ft.Row([
                    hand_size_upgrade_button
                    ]),
                ft.Divider(),
                ft.Row([
                    ft.Text("Hand Type Upgrades", size=20, color=ft.colors.WHITE),
                    ]),
                ft.Row(
                    [ft.DataTable(
                    columns=[
                        ft.DataColumn(ft.Text("Hand")),
                        ft.DataColumn(ft.Text("Cost")),
                    ],
                    rows=[
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Sequence")),
                                ft.DataCell(sequence_button)
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Triplet")),
                                ft.DataCell(triplet_button)
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Half Flush")),
                                ft.DataCell(half_flush_button)
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Flush")),
                                ft.DataCell(flush_button)
                            ]
                        ),
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text("Avatar")),
                                ft.DataCell(avatar_button)
                            ]
                        ),
                    ]) 
                ])
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
            else:
                for i in range(3):
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
                            content=ft.Text(f"{item.name}", bgcolor="#000000", color=ft.colors.WHITE),
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
            else:
                for i in range(3):
                    item_row.controls.append(
                        ft.Container(
                            image=ft.DecorationImage(src="/jongker/sold.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                            border_radius=ft.border_radius.all(5),
                            ink=True,
                        )
                    )
            panel.controls.append(shop_panel)

            # -------------------------------------------------------------
            # first mahjongker tab 
            # -------------------------------------------------------------

            first_mahjongker_panel = ft.ExpansionPanel(
                bgcolor=ft.colors.GREEN_500,
                header=ft.ListTile(title=ft.Text(f"First Mahjongker Roll")),
            )

            initial_mahjongkers_row = ft.GridView(
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
                initial_mahjongkers_row.controls.append(
                    ft.Container(
                        content=ft.Text("Empty", bgcolor="#000000",color=ft.colors.WHITE),
                        image=ft.DecorationImage(src="/tiles/empty.png", fit=ft.ImageFit.FILL, repeat=ft.ImageRepeat.NO_REPEAT),
                        border_radius=ft.border_radius.all(5),
                        ink=True,
                        )
                    )
            initial_mahjongkers_row.controls.append(ft.FloatingActionButton(icon=ft.icons.REFRESH, on_click=refresh_initial_mahjongkers))
            initial_mahjongker_text = ft.Text("", color=ft.colors.WHITE)
            first_mahjongker_panel.content = ft.Column([
                    initial_mahjongkers_row,
                    ft.Row([
                        ft.ElevatedButton(text="Select", on_click=add_initial_mahjongker),
                        initial_mahjongker_text
                    ])
                ])

            panel.controls.append(first_mahjongker_panel)

            page.views.append(
                ft.View(
                    "/shop",
                    [
                        panel,
                        ft.NavigationBar(destinations=[
                            ft.NavigationBarDestination(icon=ft.icons.QUERY_STATS, label="Stats"),
                            ft.NavigationBarDestination(icon=ft.icons.ADD_TO_PHOTOS, label="Mahjongkers"),
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
