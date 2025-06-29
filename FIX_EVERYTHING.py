# -*- coding: utf-8 -*-
# ПРОТОКОЛ "СЖЕЧЬ И ВОССТАНОВИТЬ"
# Этот скрипт полностью пересоздает всю систему UI с нуля.

import os

# --- ПУТИ К ФАЙЛАМ ---
INVENTORY_SCENE_PATH = "./scenes/ui/inventory_ui.tscn"
INVENTORY_SCRIPT_PATH = "./scripts/ui/inventory_ui.gd"
UI_MANAGER_SCRIPT_PATH = "./scripts/ui/ui_manager.gd"

# --- "ЧЕРТЕЖ" inventory_ui.tscn ---
SCENE_CONTENT = """[gd_scene load_steps=3 format=3 uid="uid://b1i4w4j7d1s7e"]

[ext_resource type="Script" path="res://scripts/ui/inventory_ui.gd" id="1_4qf0v"]
[ext_resource type="PackedScene" uid="uid://dcw784kge5i7c" path="res://scenes/ui/components/inventory_slot.tscn" id="2_4h2n7"]

[node name="InventoryUI" type="PanelContainer"]
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -250.0
offset_top = -180.0
offset_right = 250.0
offset_bottom = 180.0
grow_horizontal = 2
grow_vertical = 2
script = ExtResource("1_4qf0v")
inventory_slot_scene = ExtResource("2_4h2n7")

[node name="VBoxContainer" type="VBoxContainer" parent="."]
layout_mode = 2

[node name="TitleLabel" type="Label" parent="VBoxContainer"]
layout_mode = 2
text = "Инвентарь"
horizontal_alignment = 1

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
INVENTORY_SCRIPT_CONTENT = """# res://scripts/ui/inventory_ui.gd
# Версия 5.0: Автоматически сгенерированная, идеальная.
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
	var name_and_count_label: Label = slot.get_node("HBoxContainer/NameAndCount")
	var icon: TextureRect = slot.get_node("HBoxContainer/Icon")
	var sell_button: Button = slot.get_node("HBoxContainer/SellButton")
	name_and_count_label.text = "%s (x%d)" % [resource_data.display_name, amount]
	if resource_data.texture:
		icon.texture = resource_data.texture
		icon.custom_minimum_size = icon.texture.get_size()
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

# --- "ЧЕРТЕЖ" ui_manager.gd ---
UI_MANAGER_SCRIPT_CONTENT = """# res://scripts/ui/ui_manager.gd
# Версия 5.0: Автоматически сгенерированная, идеальная.
extends Control

@onready var money_label: Label = $Money_Label
@onready var stamina_bar: ProgressBar = $Stamina_Container/Stamina_Bar
@onready var stamina_label: Label = $Stamina_Container/Stamina_Label
@onready var upgrades_button: TextureButton = $TopNavContainer/UpgradesButton
@onready var workers_button: TextureButton = $TopNavContainer/WorkersButton
@onready var inventory_button: TextureButton = $TopNavContainer/InventoryButton
@onready var achievements_button: TextureButton = $TopNavContainer/AchievementsButton

const UpgradesUIScene = preload("res://scenes/ui/upgrades_ui.tscn")
const WorkersUIScene = preload("res://scenes/ui/workers_ui.tscn")
const InventoryUIScene = preload("res://scenes/ui/inventory_ui.tscn")
const AchievementsUIScene = preload("res://scenes/ui/achievements_ui.tscn")

var open_windows: Dictionary = {}

func _ready() -> void:
	GameManager.currency_updated.connect(_on_currency_updated)
	GameManager.stamina_updated.connect(_on_stamina_updated)
	_on_currency_updated(GameManager.player_state.currency)
	_on_stamina_updated(GameManager.player_state.current_stamina, GameManager.player_state.max_stamina)
	
	upgrades_button.pressed.connect(_on_toggle_window.bind("upgrades", UpgradesUIScene))
	workers_button.pressed.connect(_on_toggle_window.bind("workers", WorkersUIScene))
	inventory_button.pressed.connect(_on_toggle_window.bind("inventory", InventoryUIScene))
	achievements_button.pressed.connect(_on_toggle_window.bind("achievements", AchievementsUIScene))

func _on_currency_updated(new_amount: int):
	money_label.text = "Деньги: %d" % new_amount

func _on_stamina_updated(current_stamina: float, max_stamina: int):
	stamina_bar.max_value = max_stamina
	stamina_bar.value = current_stamina
	stamina_label.text = "%d / %d" % [int(current_stamina), max_stamina]

func _on_toggle_window(window_name: String, window_scene: PackedScene):
	if open_windows.has(window_name) and is_instance_valid(open_windows[window_name]) and open_windows[window_name].visible:
		open_windows[window_name].hide()
		return
	for key in open_windows:
		if open_windows.has(key) and is_instance_valid(open_windows[key]) and open_windows[key].visible:
			open_windows[key].hide()
	if not open_windows.has(window_name) or not is_instance_valid(open_windows[window_name]):
		var new_window = window_scene.instantiate()
		open_windows[window_name] = new_window
		add_child(new_window)
		var close_button = new_window.get_node_or_null("VBoxContainer/CloseButton")
		if is_instance_valid(close_button):
			close_button.pressed.connect(_on_close_window.bind(new_window))
	if open_windows[window_name].has_method("open_window"):
		open_windows[window_name].open_window()
	else:
		open_windows[window_name].show()

func _on_close_window(window_node):
	if is_instance_valid(window_node):
		window_node.hide()
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
    print("--- ЗАПУСК ПРОТОКОЛА 'СЖЕЧЬ И ВОССТАНОВИТЬ' ---")
    write_file(INVENTORY_SCENE_PATH, SCENE_CONTENT, "Сцена Инвентаря")
    write_file(INVENTORY_SCRIPT_PATH, INVENTORY_SCRIPT_CONTENT, "Скрипт Инвентаря")
    write_file(UI_MANAGER_SCRIPT_PATH, UI_MANAGER_SCRIPT_CONTENT, "Скрипт UI Менеджера")
    print("\n--- ВСЕ ОПЕРАЦИИ ЗАВЕРШЕНЫ ---")