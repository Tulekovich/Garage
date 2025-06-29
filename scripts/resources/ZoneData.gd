# res://scripts/resources/ZoneData.gd
# Ресурс для хранения статических данных об интерактивной зоне.
class_name ZoneData
extends GameResource

# Тип зоны для логического роутера (resource_generator, item_crafter, project_completer)
@export var zone_type: String = "resource_generator"

# Сколько выносливости тратится на использование зоны
@export var stamina_cost: int = 1

# ID ресурса/предмета, который производит зона
@export var produced_resource_id: String = ""

# Количество производимого ресурса/предмета
@export var produced_amount: int = 1
