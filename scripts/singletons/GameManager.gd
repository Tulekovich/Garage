# GameManager.gd (v4.4 с механикой продажи)
extends Node

signal state_initialized
signal currency_updated(new_amount: int)
signal resource_updated(resource_id: String, new_amount: int)
signal item_updated(item_id: String, new_amount: int)
signal stamina_updated(current_stamina: float, max_stamina: int)

var resource_database: Dictionary = {}
var zone_database: Dictionary = {}

var player_state: Dictionary = {
	"currency": 0, "resources": {}, "items": {}, "upgrades": {},
	"current_stamina": 0.0, "max_stamina": 50
}
var stamina_regen_rate: float

func _ready():
	_load_all_game_data()
	_initialize_player_state()
	print("GameManager: %d ресурсов и %d зон загружено." % [resource_database.size(), zone_database.size()])

func _process(delta: float):
	if player_state.current_stamina < player_state.max_stamina:
		player_state.current_stamina = min(player_state.current_stamina + stamina_regen_rate * delta, player_state.max_stamina)
		stamina_updated.emit(player_state.current_stamina, player_state.max_stamina)

# --- PUBLIC API ---
func add_resource(id: String, amount: int):
	if not player_state.resources.has(id): return
	player_state.resources[id] += amount
	var resource_name = resource_database[id].display_name
	print("Получен ресурс: %s. Количество: %d. Всего в инвентаре: %d" % [resource_name, amount, player_state.resources[id]])
	resource_updated.emit(id, player_state.resources[id])

func add_item(id: String, amount: int):
	if not player_state.items.has(id): return
	player_state.items[id] += amount
	var item_name = resource_database[id].display_name
	print("Получен предмет: %s. Количество: %d. Всего в инвентаре: %d" % [item_name, amount, player_state.items[id]])
	item_updated.emit(id, player_state.items[id])

func spend_stamina(amount: int) -> bool:
	if player_state.current_stamina >= amount:
		player_state.current_stamina -= amount
		stamina_updated.emit(player_state.current_stamina, player_state.max_stamina)
		return true
	return false

func sell_all_resources(resource_id: String):
	var amount_to_sell = player_state.resources.get(resource_id, 0)
	if amount_to_sell == 0:
		print("Нечего продавать.")
		return

	var resource_data = resource_database.get(resource_id)
	if not resource_data or not resource_data is MaterialResource:
		printerr("Попытка продать не-материальный ресурс: ", resource_id)
		return

	var price_per_unit = resource_data.sell_value
	var total_earned = amount_to_sell * price_per_unit

	player_state.resources[resource_id] = 0
	player_state.currency += total_earned

	print("Продано %d x '%s' за %d Монет." % [amount_to_sell, resource_data.display_name, total_earned])

	resource_updated.emit(resource_id, 0)
	currency_updated.emit(player_state.currency)


# --- PRIVATE FUNCTIONS ---
func _initialize_player_state():
	for resource_id in resource_database:
		var resource = resource_database[resource_id]
		if resource is MaterialResource: player_state.resources[resource_id] = 0
		elif resource is ItemResource: player_state.items[resource_id] = 0
	
	player_state.max_stamina = 50
	player_state.current_stamina = float(player_state.max_stamina)
	stamina_regen_rate = 0.5
	
	state_initialized.emit()

func _load_all_game_data():
	_load_data_recursively("res://data/resources/")
	_load_data_recursively("res://data/zones/")

func _load_data_recursively(path: String):
	var dir = DirAccess.open(path)
	if dir:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			if dir.current_is_dir() and file_name != "." and file_name != "..":
				_load_data_recursively(dir.get_current_dir().path_join(file_name))
			elif file_name.ends_with(".tres"):
				var resource = load(dir.get_current_dir().path_join(file_name))
				if not resource is GameResource or resource.id.is_empty():
					printerr("Ошибка загрузки: ", file_name)
					file_name = dir.get_next()
					continue
				
				if resource is MaterialResource or resource is ItemResource:
					resource_database[resource.id] = resource
				elif resource is ZoneData:
					zone_database[resource.id] = resource
			file_name = dir.get_next()
	else:
		printerr("Не удалось открыть директорию: ", path)
