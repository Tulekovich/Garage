# res://scripts/resources/GameResource.gd
# Базовый класс для всех игровых сущностей. Теперь с иконкой.
class_name GameResource
extends Resource

@export var id: String = ""
@export var display_name: String = ""
@export_multiline var description: String = ""
# [НОВОЕ] Теперь ЛЮБОЙ ресурс в игре будет иметь текстуру.
@export var texture: Texture2D 
