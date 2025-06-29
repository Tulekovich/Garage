# res://scripts/world/main_world.gd
# Очищен от неверной логики.
extends Node2D

var game_manager

func _ready() -> void:
	game_manager = get_node("/root/GameManager")
	# [УДАЛЕНО] Ошибочное подключение к кнопке.

func _on_zone_interacted(zone_id: String) -> void:
	var zone_data = game_manager.zone_database.get(zone_id)
	
	if not zone_data:
		printerr("ERROR: No data found for zone_id '", zone_id, "' in GameManager.zone_database")
		return
	
	if game_manager.spend_stamina(zone_data.stamina_cost):
		match zone_data.zone_type:
			"resource_generator":
				game_manager.add_resource(zone_data.produced_resource_id, zone_data.produced_amount)
			"item_crafter":
				game_manager.add_item(zone_data.produced_resource_id, zone_data.produced_amount)
			_:
				printerr("ERROR: Unknown zone type '", zone_data.zone_type, "' for zone_id '", zone_id, "'")
