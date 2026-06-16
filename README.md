# Deep Jungle

An endless beat-'em-up where a stickman fights infinite waves of jungle monkeys.

---

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

---

## Project layout

```
.
├── main.py                  Entry point — creates a Game and calls run()
├── requirements.txt         Python dependencies (pygame)
├── assets/
│   └── stickman.png         Player sprite (200×340 transparent PNG)
└── game/
    ├── config.py            All constants: screen size, FPS, colours, asset paths
    ├── logger.py            Returns a shared, timestamped logger used across modules
    ├── app.py               Game class — owns the window, clock, and main loop
    ├── input.py             TODO stub — will translate key state into game commands
    └── entities/
        └── player.py        Player class — loads + draws the stickman; move/attack stubs
```

### File responsibilities

| File | Responsible for |
|---|---|
| `main.py` | Single entry point; nothing else lives here |
| `game/config.py` | Every magic number or path in one place; import from here, never hard-code |
| `game/logger.py` | `get_logger()` — call it from any module for a consistent timestamped log |
| `game/app.py` | `Game` class: `__init__` sets up pygame, `run()` drives the loop, `update()` / `draw()` are called every frame |
| `game/input.py` | Will read pygame keyboard / gamepad state and return normalised command objects |
| `game/entities/player.py` | `Player` class: loads `stickman.png`, scales it, draws it; `move()` and `attack()` are stubs |

---

## Not yet implemented — TODO

The following gameplay systems are **scaffolded as stubs only**.
All logic for them still needs to be written:

- **Player movement** — walking left/right, `Player.move(direction)`
- **Jumping** — vertical velocity + gravity, landing on the ground
- **Melee combat** — `Player.attack()`, hit-box detection, combo timing
- **Enemy (monkey) entity** — sprite, AI state machine, patrol / chase / attack
- **Wave spawner** — generates enemy waves, scales difficulty over time
- **Collision system** — player vs. enemy, player vs. ground, knockback
- **Input handler** — `game/input.py`: map key state → commands consumed by entities
- **Scoring** — track kills and survival time, display HUD
- **Game-over / restart** — detect player death, show screen, reset state
- **Sound & music** — load and play SFX and background tracks
- **Background / parallax** — jungle scenery layers that scroll behind the action
