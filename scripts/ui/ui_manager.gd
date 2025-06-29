# res://scripts/ui/ui_manager.gd
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
