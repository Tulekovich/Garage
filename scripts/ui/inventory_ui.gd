# res://scripts/ui/inventory_ui.gd
# Версия 9.0: Финальная. Устанавливает минимальный размер для создаваемых слотов.
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
	
	# === ВОТ ФИНАЛЬНОЕ ИСПРАВЛЕНИЕ ===
	# Устанавливаем минимальный размер для всего слота, чтобы он не "схлопывался".
	# 64px - это примерная высота стандартной иконки + отступы.
	slot.custom_minimum_size.y = 64
	# =================================

	item_list.add_child(slot)

func _on_inventory_changed(id: String, amount: int):
	if is_visible():
		_redraw_inventory()

func _on_sell_button_pressed(resource_id: String):
	GameManager.sell_all_resources(resource_id)
