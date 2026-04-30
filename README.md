# RPG Game – The Way of The Ninja (Blocky Edition)

Semestrální projekt do předmětu Pokročilé nástroje pro vývoj (PN).

Jedná se o 2D dungeon crawler RPG hru vytvořenou v Pythonu pomocí knihovny **pygame**, postavenou na vlastním entity systému a MVC-like architektuře.

---

## O hře

Hráč ovládá ninju, který se pohybuje po mapě, bojuje s nepřáteli a postupuje jednotlivými úrovněmi.

### Hlavní prvky:
- pohyb v mřížce (grid-based movement)
- soubojový systém (útok mečem)
- NPC s jednoduchou AI
- více úrovní map
- menu a outro obrazovka
- kolizní systém
- entitní systém s dědičností

---

## Architektura projektu

Projekt je rozdělen do několika hlavních částí:

### `model`
Obsahuje všechny herní entity:
- Entity (základní abstrakce)
- MovableEntity (pohyb)
- Character (HP, boj)
- NPC, Player
- Map
- Nepřátelé: LightElf, Orc, Human
- objekty: Wall, Floor, Goal
- zbraně: Weapon, Sword

### `controller`
Logika hry:
- GameController (hlavní orchestrátor)
- PlayerController (vstupy)
- CollisionController (kolize)
- FileController (načítání map ze souboru)

### `view`
Renderovací vrstva:
- GameView (vykreslování hry)
- MenuView (operace s menu)
- SpriteLoader (načítání spritů)

---

## Technologie

- Python 3.x
- pygame
- Sphinx (dokumentace)
- JSON (mapy)

---

## Mapy

Mapy jsou definovány v JSON souborech a načítány pomocí `FileController`.

Symboly:
- `1` = zeď (Wall)
- `0` = podlaha (Floor)
- `2` = hráč
- `LE` = Light Elf
- `OR` = Orc
- `HU` = Human
- `G` = cíl (Goal)

---

## AI a NPC

NPC mají jednoduché chování:
- náhodný pohyb v intervalech
- pravděpodobnost pohybu
- základní bojová logika

---

## Soubojový systém

- hráč používá meč (`Sword`)
- útok má cooldown
- kolize řeší poškození
- NPC mohou útočit zpět (prostřednicvtím kolize s hráčem)

---

## Systém entit

Každý herní objekt je entita:
- má unikátní ID
- pozici (x, y)
- validaci parametrů
- hierarchii tříd

---

## Dokumentace

Projekt obsahuje plnou Sphinx dokumentaci:

Spuštění:
```bash
cd docs
make html
```
## Pytest unit testing
