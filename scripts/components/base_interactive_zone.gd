@tool
extends Node2D

signal zone_interacted(zone_id: String)

@export var zone_id: String = ""
@export var texture: Texture2D:
	set(new_texture):
		texture = new_texture
		if not is_inside_tree():
			await ready
		sprite_2d.texture = texture
		update_collision_from_sprite()

# [НОВОЕ] Переменная для хранения начального масштаба
var initial_scale: Vector2 = Vector2.ONE

@onready var sprite_2d: Sprite2D = $Sprite2D
@onready var area_2d: Area2D = $Area2D
@onready var collision_polygon_2d: CollisionPolygon2D = $Area2D/CollisionPolygon2D

func _ready() -> void:
	# [НОВОЕ] Запоминаем масштаб, установленный в редакторе, при запуске.
	initial_scale = self.scale
	
	if not Engine.is_editor_hint():
		area_2d.input_event.connect(_on_area_2d_input_event)


func update_collision_from_sprite() -> void:
	if sprite_2d.texture == null: return
	if not is_inside_tree():
		await ready

	var texture_size = sprite_2d.texture.get_size()
	var half_size = texture_size / 2.0
	var polygon_points = PackedVector2Array([
		Vector2(-half_size.x, -half_size.y), Vector2(half_size.x, -half_size.y),
		Vector2(half_size.x, half_size.y), Vector2(-half_size.x, half_size.y)
	])
	collision_polygon_2d.polygon = polygon_points

func _on_area_2d_input_event(_viewport, event, _shape_idx) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.is_pressed():
		if zone_id.is_empty():
			printerr("ERROR: zone_id is not set for ", self.name)
			return
		
		play_click_animation()
		zone_interacted.emit(zone_id)

func play_click_animation() -> void:
	var tween = create_tween()
	tween.set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_SINE)
	# [ИЗМЕНЕНО] Анимируем масштаб ОТНОСИТЕЛЬНО начального.
	tween.tween_property(self, "scale", initial_scale * 0.9, 0.1)
	# [ИЗМЕНЕНО] Возвращаем объект к его ИСХОДНОМУ масштабу.
	tween.tween_property(self, "scale", initial_scale, 0.1)
