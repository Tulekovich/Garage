# ТЕХНИЧЕСКИЙ ЖУРНАЛ (АКТУАЛЬНЫЙ)
## РАЗДЕЛ 1: УТВЕРЖДЕННАЯ АРХИТЕКТУРА
- **Data-Driven Design:** Данные в `.tres` файлах.
- **Слабая Связанность:** Взаимодействие через сигналы.
- **Единый Источник Истины:** `GameManager` хранит состояние.
- **Физические Слои:** Интерактивные зоны (`Area2D`) находятся на Слое 1 и используют Маску 1 для детекции ввода.

## РАЗДЕЛ 2: СТРУКТУРА КЛЮЧЕВЫХ СЦЕН
### inventory_ui.tscn (Финальная)
- **InventoryUI (PanelContainer)** [Layout: Center]
    - **VBoxContainer**
        - **TitleLabel (Label)**
        - **ScrollContainer** [Size Flags Vertical: Fill, Expand]
            - **ItemList (VBoxContainer)**
        - **CloseButton (Button)** [Process Mode: Always]
