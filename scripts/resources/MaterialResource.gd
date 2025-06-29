# res://scripts/resources/MaterialResource.gd
# Специализированный ресурс для продаваемых материалов.
class_name MaterialResource
extends GameResource

@export var sell_value: int = 1
# [УДАЛЕНО] Строка '@export var texture: Texture2D' удалена, так как теперь она наследуется от GameResource.
