# Pooltoy Origin

A custom origin for the [Origins](https://modrinth.com/mod/origins) mod: the **Pooltoy**, an inflatable that bounces, floats and drifts, but pops easily.

**Targets:** Minecraft **1.20.1** with Origins. It works on **Fabric** (Origins 1.10.x, which includes Apoli 2.9.x) and on **Forge** (the Origins Forge port by EdwinMindcraft, which includes the Forge Apoli). `pack_format` is **15**, the same number for data packs and resource packs on 1.20.1.

It ships as **one mod file**, `Pooltoy-<version>.jar`, which works on Forge, NeoForge and Fabric. It contains the origin and its powers (`data/`) and the English names (`assets/`). Separate data pack and resource pack zips are also built, for anyone who would rather not add a mod.

## Powers

| Power | File | Effect | Apoli type(s) |
|---|---|---|---|
| Inflated | `wide.json` | Looks 1.25× as wide, hitbox 1.66× as wide (about 1 block). Needs **Pehkui**; does nothing without it | `apoli:action_on_callback` + `apoli:execute_command` (`scale set pehkui:model_width 1.25` / `pehkui:hitbox_width 1.66`, reset on removal, reapplied on respawn) |
| Deflating | `deflate.json` | Height and speed shrink with health: 100% at ≥90% health, then per 10% health lost −5% height (Pehkui) and −3.8% speed; 55% height / 66% speed below 10% | `apoli:multiple` → `apoli:action_over_time` (every 10 ticks, `apoli:if_else_list` on `apoli:relative_health` → `scale set pehkui:height …`) + `apoli:action_on_callback` (delay set / reset) + 9× `apoli:conditioned_attribute` (`generic.movement_speed` per health band) |
| Leaky | `leak.json` | A piercing hit (same hits as Puncturable) starts a leak: −1 health/second (`pooltoy:leak` damage, ignores armor) until you eat any food. Stops at 2 health or less, so it never kills | `apoli:multiple` → `apoli:resource` (flag) + `apoli:action_when_damage_taken` + `apoli:action_over_time` + `apoli:action_on_item_use` |
| Squishy | `squishy.json` | Squash-and-stretch (Pehkui `model_height`/`model_width`/`eye_height`, hitbox unchanged) when landing or hit; squishes down and wider while crouching. Each squish plays `entity.fox.ambient` (hit squeak comes from Squeaky). Landings under 2 blocks get a small, quieter squish; 2+ blocks get the full squash and bounce you back up (not while sneaking). Needs **Pehkui** | `apoli:multiple` → `apoli:action_on_land`, `apoli:action_when_damage_taken`, `apoli:action_over_time` (`rising_action`/`falling_action` on `apoli:sneaking`), `apoli:delay` + `apoli:if_else` sequencing |
| Squeaky | `squeaky.json` | Fox squeak (`entity.fox.ambient`) when hurt (on top of the normal hurt sound) | `apoli:action_when_damage_taken` + `apoli:play_sound` |
| Bouncy | `bouncy.json` | No fall damage | `apoli:modify_damage_taken` |
| Buoyant | `buoyant.json` | Can't go underwater: forced back up whenever water is above chest height or over your head; +50% horizontal speed in water | `apoli:multiple` → 3× `apoli:modify_velocity` (`min_total` on Y: a floor on upward movement) |
| Floaty Jump | `floaty_jump.json` | +25% jump velocity; slow fall (sneak to fall normally) | `apoli:multiple` → `apoli:modify_jump` + `apoli:modify_falling` |
| Air Reserve | `air_reserve.json` | Air runs out half as fast underwater | `apoli:action_over_time` + `apoli:gain_air` |
| Puncturable | `weakness_sharp.json` | +50% damage from arrows, tridents, sword/axe hits, thorns, cactus, berry bushes, bee stings, dripstone | `apoli:modify_damage_taken` |
| Meltable | `weakness_fire.json` | Double damage from fire, lava, magma blocks, fireballs | `apoli:modify_damage_taken` |
| Lightweight | `weakness_knockback.json` | Knockback resistance is removed and each hit adds extra knockback | `apoli:multiple` → `apoli:attribute` + `apoli:modify_damage_taken` |

The "sharp" damage sources are listed in `data/pooltoy/tags/damage_type/sharp.json`. Edit that file to add or remove sources.

## Install (Windows)

### CurseForge app

1. **Create Custom Profile** → Minecraft **1.20.1** → pick **Forge**, **NeoForge** or **Fabric**.
2. In the profile, use **Add Content** to install **Origins** (the Forge version, or Fabric Origins plus **Fabric API**) and **Pehkui**. Pehkui is optional, but the Inflated, Deflating and Squishy powers need it.
3. Click **⋯ → Open Folder**, open the `mods` folder, and drop `Pooltoy-<version>.jar` in.
4. Press **Play**.

### Vanilla launcher

1. Install the mod loader and Origins:
   - **Forge / NeoForge:** install Forge (or NeoForge) for 1.20.1, then put **Origins (Forge, 1.20.1)** and the mods it lists as required in `%APPDATA%\.minecraft\mods`.
   - **Fabric:** install Fabric Loader for 1.20.1, then put **Fabric API** and **Origins (Fabric, 1.20.1)** in `%APPDATA%\.minecraft\mods`.

   Origins already includes Apoli. Also add **Pehkui** for your loader on 1.20.1. It's optional, but Inflated, Deflating and Squishy need it.
2. Download `Pooltoy-<version>.jar` from the [Releases page](https://github.com/Jayty07/PooltoyOrigin/releases), or build it (see below), and drop it into the same `mods` folder.
3. Start the game and open any world. Pooltoy shows up in the origin selection screen. In a world where you've already picked an origin, run `/origin gui @s` (needs cheats/op).

**Servers:** put the jar in the server's `mods` folder too. Every player needs it, since it also carries the text.

**Upgrading from the zips:** remove `Pooltoy-datapack.zip` from your world's `datapacks` folder and `Pooltoy-resourcepack.zip` from `resourcepacks`. The jar replaces both.

### Uploading to CurseForge

Upload the jar as a **Mod** file and tick **1.20.1** plus the **Forge**, **NeoForge** and **Fabric** loaders. Under related projects, mark **Origins** as a required dependency and **Pehkui** as optional. On Fabric, Fabric API is also required.

### Without the mod (data pack + resource pack)

1. Copy `Pooltoy-datapack.zip` into `%APPDATA%\.minecraft\saves\<YourWorld>\datapacks\`.
2. Copy `Pooltoy-resourcepack.zip` into `%APPDATA%\.minecraft\resourcepacks\` and turn it on under **Options → Resource Packs**.

## Build it yourself

Requires [Python 3](https://www.python.org/downloads/). Open a terminal in this folder and run:

```
python tools/validate.py
python tools/build.py
```

`validate.py` checks that every JSON file is valid, that every Apoli type ID is in the verified 1.20.1 list, that the origin's powers exist, and that every name/description has a translation. `build.py` writes the mod jar and both zips to `dist/`. The mod metadata lives in `mod/`: `fabric.mod.json` for Fabric, and `META-INF/mods.toml` for Forge/NeoForge, using the `lowcodefml` loader for mods that contain no code.

## Notes on Apoli 1.20.1

These were checked against [apace100/apoli `2.9.2+mc.1.20.1`](https://github.com/apace100/apoli/tree/2.9.2+mc.1.20.1) and [EdwinMindcraft/origins-architectury](https://github.com/EdwinMindcraft/origins-architectury):

- **`apoli:swimming` is not used.** On 1.20.1 it lets you swim through the *air* while sprinting. It does not make you float.
- **Swim speed uses `apoli:modify_velocity` rather than an attribute.** Fabric Apoli 1.20.1 registers `apoli:modify_swim_speed` but never applies it. The swim-speed attribute is named `additionalentityattributes:generic.water_speed` on Fabric and `additionalentityattributes:water_speed` on Forge, so neither name works on both loaders. `modify_velocity` does work on both.
- **Forge:** every power, condition and action ID used here also exists in [EdwinMindcraft/apoli `1.20.x/forge`](https://github.com/EdwinMindcraft/apoli/tree/1.20.x/forge), with the same field names.
- **Jump uses `apoli:modify_jump`, not an attribute.** Players don't have a jump-strength attribute until 1.20.5.
- **Knockback resistance can't go below 0**, so reducing the attribute alone doesn't add knockback. It's set to ×0 (which also cancels Netherite's resistance) and an extra push is added on each hit.
- **Air Reserve:** Apoli has no "water breathing" power type. Origins' Merling gills are handled in Origins' own Java code. Air Reserve refunds 1 air every 2 ticks while underwater instead.
