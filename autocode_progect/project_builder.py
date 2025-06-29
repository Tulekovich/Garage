# -*- coding: utf-8 -*-
# ПРОТОКОЛ "АБСОЛЮТНАЯ СИНХРОНИЗАЦИЯ И РЕМОНТ" v3.0
# Этот скрипт полностью пересоздает всю систему UI инвентаря с нуля.

import os

# --- ПУТИ К ФАЙЛАМ ---
INVENTORY_SLOT_SCENE_PATH = "./scenes/ui/components/inventory_slot.tscn"
INVENTORY_UI_SCENE_PATH = "./scenes/ui/inventory_ui.tscn"
INVENTORY_UI_SCRIPT_PATH = "./scripts/ui/inventory_ui.gd"

# --- "ЧЕРТЕЖ" inventory_slot.tscn ---
INVENTORY_SLOT_SCENE_CONTENT = """[gd_scene load_steps=2 format=3 uid="uid://dcw784kge5i7c"]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_0u8de"]
bg_color = Color(0.141176, 0.141176, 0.172549, 0.588235)
corner_radius_top_left = 5
corner_radius_top_right = 5
corner_radius_bottom_right = 5
corner_radius_bottom_left = 5

[node name="InventorySlot" type="PanelContainer"]
custom_minimum_size = Vector2(0, 74)
theme_override_styles/panel = SubResource("StyleBoxFlat_0u8de")

[node name="HBoxContainer" type="HBoxContainer" parent="."]
layout_mode = 2
theme_override_constants/separation = 10

[node name="Icon" type="TextureRect" parent="HBoxContainer"]
layout_mode = 2
custom_minimum_size = Vector2(64, 64)
expand_mode = 1
stretch_mode = 5

[node name="InfoVBox" type="VBoxContainer" parent="HBoxContainer"]
layout_mode = 2
size_flags_horizontal = 3
alignment = 1

[node name="NameLabel" type="Label" parent="HBoxContainer/InfoVBox"]
layout_mode = 2
text = "Название предмета"

[node name="AmountLabel" type="Label" parent="HBoxContainer/InfoVBox"]
layout_mode = 2
text = "x 99"
theme_override_colors/font_color = Color(0.67451, 0.67451, 0.67451, 1)

[node name="SellButton" type="Button" parent="HBoxContainer"]
layout_mode = 2
size_flags_vertical = 4
text = "Продать"

"""

# --- "ЧЕРТЕЖ" inventory_ui.tscn ---
INVENTORY_UI_SCENE_CONTENT = """[gd_scene load_steps=3 format=3 uid="uid://b1i4w4j7d1s7e"]

[ext_resource type="Script" path="res://scripts/ui/inventory_ui.gd" id="1_4qf0v"]
[ext_resource type="PackedScene" uid="uid://dcw784kge5i7c" path="res://scenes/ui/components/inventory_slot.tscn" id="2_4h2n7"]

[node name="InventoryUI" type="PanelContainer"]
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -250.0
offset_top = -200.0
offset_right = 250.0
offset_bottom = 200.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_4qf0v")
inventory_slot_scene = ExtResource("2_4h2n7")

[node name="VBoxContainer" type="VBoxContainer" parent="."]
layout_mode = 2
theme_override_constants/separation = 10

[node name="TitleLabel" type="Label" parent="VBoxContainer"]
layout_mode = 2
text = "Инвентарь"
horizontal_alignment = 1

[node name="HSeparator" type="HSeparator" parent="VBoxContainer"]
layout_mode = 2

[node name="ScrollContainer" type="ScrollContainer" parent="VBoxContainer"]
layout_mode = 2
size_flags_vertical = 3

[node name="ItemList" type="VBoxContainer" parent="VBoxContainer/ScrollContainer"]
layout_mode = 2
size_flags_horizontal = 3

[node name="CloseButton" type="Button" parent="VBoxContainer"]
layout_mode = 2
size_flags_horizontal = 4
text = "Закрыть"

"""

# --- "ЧЕРТЕЖ" inventory_ui.gd ---
INVENTORY_UI_SCRIPT_CONTENT = """# res://scripts/ui/inventory_ui.gd
# Версия 14.0: Автоматически сгенерированная, финальная.
extends PanelContainer

signal sell_button_pressed(resource_id: String)

@export var inventory_slot_scene: PackedScene
@onready var item_list = $VBoxContainer/ScrollContainer/ItemList

func _ready():
	sell_button_pressed.connect(_on_sell_button_pressed)
	GameManager.resource_updated.connect(_on_inventory_changed)
	GameManager.item_updated.connect(_on_inventory_changed)
	GameManager.state_initialized.connect(_redraw_inventory)

func open_window():
	_redraw_inventory()
	show()

func _redraw_inventory():
	if inventory_slot_scene == null: return
	if not is_instance_valid(item_list): return
	for child in item_list.get_children():
		child.queue_free()
	for resource_id in GameManager.player_state.resources:
		if GameManager.player_state.resources[resource_id] > 0:
			_create_slot(resource_id, GameManager.player_state.resources[resource_id], true)
	for item_id in GameManager.player_state.items:
		if GameManager.player_state.items[item_id] > 0:
			_create_slot(item_id, GameManager.player_state.items[item_id], false)

func _create_slot(id: String, amount: int, is_material: bool):
	var resource_data = GameManager.resource_database.get(id)
	if not resource_data: return
	var slot = inventory_slot_scene.instantiate()
	var icon: TextureRect = slot.get_node("HBoxContainer/Icon")
	var name_label: Label = slot.get_node("HBoxContainer/InfoVBox/NameLabel")
	var amount_label: Label = slot.get_node("HBoxContainer/InfoVBox/AmountLabel")
	var sell_button: Button = slot.get_node("HBoxContainer/SellButton")
	name_label.text = resource_data.display_name
	amount_label.text = "x %d" % amount
	if resource_data.texture:
		icon.texture = resource_data.texture
	if is_material:
		sell_button.show()
		sell_button.pressed.connect(func(): emit_signal("sell_button_pressed", id))
	else:
		sell_button.hide()
	item_list.add_child(slot)

func _on_inventory_changed(id: String, amount: int):
	if is_visible(): _redraw_inventory()

func _on_sell_button_pressed(resource_id: String):
	GameManager.sell_all_resources(resource_id)
"""

def write_file(path, content, name):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"УСПЕХ: {name} успешно создан/перезаписан.")
    except Exception as e:
        print(f"!!! ОШИБКА при записи {name}: {e}")

if __name__ == "__main__":
    print("--- ЗАПУСК ПРОТОКОЛА 'АБСОЛЮТНАЯ СИНХРОНИЗАЦИЯ И РЕМОНТ' ---")
    write_file(INVENTORY_SLOT_SCENE_PATH, INVENTORY_SLOT_SCENE_CONTENT, "Сцена Слота Инвентаря")
    write_file(INVENTORY_UI_SCENE_PATH, INVENTORY_UI_SCENE_CONTENT, "Сцена UI Инвентаря")
    write_file(INVENTORY_UI_SCRIPT_PATH, INVENTORY_UI_SCRIPT_CONTENT, "Скрипт UI Инвентаря")
    print("\n--- ВСЕ ОПЕРАЦИИ ЗАВЕРШЕНЫ ---")