# Pooltoy Origin

A custom origin for the [Origins](https://modrinth.com/mod/origins) mod: the **Pooltoy**, an inflatable that bounces, floats and drifts, but pops easily.

**Targets:** Minecraft **1.20.1** with Origins. It works on **Fabric** (Origins 1.10.x, which includes Apoli 2.9.x) and on **Forge** (the Origins Forge port by EdwinMindcraft, which includes the Forge Apoli). `pack_format` is **15**, the same number for data packs and resource packs on 1.20.1.

It comes in two parts:

| Part | Folder | What it does |
|---|---|---|
| Data pack | `data/` | Adds the origin and its powers. Needed for the origin to exist. |
| Resource pack | `assets/` | English names and descriptions. Without it you'll see raw keys like `origin.pooltoy.pooltoy.name`. |

## Powers

| Power | File | Effect | Apoli type(s) |
|---|---|---|---|
| Bouncy | `bouncy.json` | No fall damage | `apoli:modify_damage_taken` |
| Buoyant | `buoyant.json` | Can't go underwater: forced back up whenever water is above chest height or over your head; +50% horizontal speed in water | `apoli:multiple` → 3× `apoli:modify_velocity` (`max_total` on Y) |
| Floaty Jump | `floaty_jump.json` | +25% jump velocity; slow fall (sneak to fall normally) | `apoli:multiple` → `apoli:modify_jump` + `apoli:modify_falling` |
| Air Reserve | `air_reserve.json` | Air runs out half as fast underwater | `apoli:action_over_time` + `apoli:gain_air` |
| Puncturable | `weakness_sharp.json` | +50% damage from arrows, tridents, sword/axe hits, thorns, cactus, berry bushes, bee stings, dripstone | `apoli:modify_damage_taken` |
| Meltable | `weakness_fire.json` | Double damage from fire, lava, magma blocks, fireballs | `apoli:modify_damage_taken` |
| Lightweight | `weakness_knockback.json` | Knockback resistance is removed and each hit adds extra knockback | `apoli:multiple` → `apoli:attribute` + `apoli:modify_damage_taken` |

The "sharp" damage sources are listed in `data/pooltoy/tags/damage_type/sharp.json`. Edit that file to add or remove sources.

## Install (Windows)

1. **Fabric:** install Fabric Loader for 1.20.1, then put **Fabric API** and **Origins (Fabric, 1.20.1)** in your `mods` folder.
   **Forge:** install Forge for 1.20.1, then put **Origins (Forge, 1.20.1)** and the mods it lists as required in your `mods` folder.
   Origins already includes Apoli on both.
2. Get `Pooltoy-datapack.zip` and `Pooltoy-resourcepack.zip`. Download them from the [Releases page](https://github.com/Jayty07/PooltoyOrigin/releases) if a release has been published, or build them yourself (see below).
3. **Data pack:** copy `Pooltoy-datapack.zip` into your world's `datapacks` folder:
   `%APPDATA%\.minecraft\saves\<YourWorld>\datapacks\`
   For a new world, click **Data Packs** on the Create World screen and drag the zip in.
4. **Resource pack:** copy `Pooltoy-resourcepack.zip` into `%APPDATA%\.minecraft\resourcepacks\`, then turn it on under **Options → Resource Packs**.
5. Open the world. Pooltoy shows up in the origin selection screen. To pick again in an existing world, run `/origin gui @s` (needs cheats/op).

On a server, put the data pack in `world/datapacks/`. Each player installs the resource pack themselves, or you set it as the server resource pack.

## Build the zips yourself

Requires [Python 3](https://www.python.org/downloads/). Open a terminal in this folder and run:

```
python tools/validate.py
python tools/build.py
```

`validate.py` checks that every JSON file is valid, that every Apoli type ID is in the verified 1.20.1 list, that the origin's powers exist, and that every name/description has a translation. `build.py` writes both zips to `dist/`.

## Notes on Apoli 1.20.1

These were checked against [apace100/apoli `2.9.2+mc.1.20.1`](https://github.com/apace100/apoli/tree/2.9.2+mc.1.20.1) and [EdwinMindcraft/origins-architectury](https://github.com/EdwinMindcraft/origins-architectury):

- **`apoli:swimming` is not used.** On 1.20.1 it lets you swim through the *air* while sprinting. It does not make you float.
- **Swim speed uses `apoli:modify_velocity` rather than an attribute.** Fabric Apoli 1.20.1 registers `apoli:modify_swim_speed` but never applies it. The swim-speed attribute is named `additionalentityattributes:generic.water_speed` on Fabric and `additionalentityattributes:water_speed` on Forge, so neither name works on both loaders. `modify_velocity` does work on both.
- **Forge:** every power, condition and action ID used here also exists in [EdwinMindcraft/apoli `1.20.x/forge`](https://github.com/EdwinMindcraft/apoli/tree/1.20.x/forge), with the same field names.
- **Jump uses `apoli:modify_jump`, not an attribute.** Players don't have a jump-strength attribute until 1.20.5.
- **Knockback resistance can't go below 0**, so reducing the attribute alone doesn't add knockback. It's set to ×0 (which also cancels Netherite's resistance) and an extra push is added on each hit.
- **Air Reserve:** Apoli has no "water breathing" power type. Origins' Merling gills are handled in Origins' own Java code. Air Reserve refunds 1 air every 2 ticks while underwater instead.
