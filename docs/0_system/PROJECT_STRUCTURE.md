# СТРУКТУРА ПРОЕКТА "ГАРАЖ" (АКТУАЛЬНАЯ)
/ (res://)
├── _archive/
├── assets/
├── data/
│   ├── resources/
│   │   ├── item/
│   │   └── material/
│   └── zones/
├── scenes/
│   ├── components/
│   │   └── base_interactive_zone.tscn
│   ├── player/
│   ├── singletons/
│   │   └── GameManager.tscn
│   ├── ui/
│   │   ├── components/
│   │   │   └── inventory_slot.tscn
│   │   └── inventory_ui.tscn
│   └── world/
│       └── main_world.tscn
└── scripts/
    ├── components/
    │   └── base_interactive_zone.gd
    ├── player/
    ├── resources/
    │   ├── GameResource.gd
    │   ├── ItemResource.gd
    │   ├── MaterialResource.gd
    │   └── ZoneData.gd
    ├── singletons/
    │   └── GameManager.gd
    ├── ui/
    │   ├── inventory_ui.gd
    │   └── ui_manager.gd
    └── world/
        └── main_world.gd
