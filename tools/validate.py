#!/usr/bin/env python3
"""Checks the pack: JSON syntax, Apoli type IDs, origin -> power links and lang keys."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Verified against Apoli 2.9.2+mc.1.20.1 (apace100/apoli) and Origins 1.10.2+mc.1.20.1.
POWER_TYPES = {
    "apoli:modify_damage_taken", "apoli:multiple", "apoli:modify_velocity",
    "apoli:attribute", "apoli:modify_jump", "apoli:modify_falling",
    "apoli:action_over_time", "apoli:action_on_callback", "apoli:resource",
    "apoli:action_when_damage_taken", "apoli:action_on_item_use", "apoli:conditioned_attribute",
}
ENTITY_CONDITIONS = {
    "apoli:and", "apoli:or", "apoli:fluid_height", "apoli:sneaking",
    "apoli:swimming", "apoli:fall_flying", "apoli:submerged_in", "apoli:equipped_item",
    "apoli:relative_health", "apoli:health", "apoli:resource",
}
DAMAGE_CONDITIONS = {"apoli:and", "apoli:or", "apoli:name", "apoli:in_tag", "apoli:attacker"}
ITEM_CONDITIONS = {"apoli:or", "apoli:ingredient", "apoli:food"}
ENTITY_ACTIONS = {"apoli:gain_air", "apoli:execute_command", "apoli:and", "apoli:if_else_list",
                  "apoli:change_resource", "apoli:damage", "apoli:play_sound"}
BIENTITY_ACTIONS = {"apoli:add_velocity"}

POWER_META_KEYS = {"type", "name", "description", "hidden", "condition", "loading_priority", "badges"}

errors = []


def err(path, msg):
    errors.append(f"{path.relative_to(ROOT)}: {msg}")


def load(path):
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        err(path, f"invalid JSON: {e}")
        return None


def check_type(path, obj, allowed, kind):
    t = obj.get("type") if isinstance(obj, dict) else None
    if t not in allowed:
        err(path, f"unknown/unverified {kind} type {t!r}")


def walk_condition(path, cond, allowed, kind, nested=None):
    check_type(path, cond, allowed, kind)
    for sub in cond.get("conditions", []):
        walk_condition(path, sub, allowed, kind, nested)
    if nested:
        for key, (sub_allowed, sub_kind, sub_nested) in nested.items():
            if key in cond:
                walk_condition(path, cond[key], sub_allowed, sub_kind, sub_nested)


ITEM_NESTED = {}
ENTITY_NESTED = {"item_condition": (ITEM_CONDITIONS, "item condition", ITEM_NESTED)}
DAMAGE_NESTED = {"entity_condition": (ENTITY_CONDITIONS, "entity condition", ENTITY_NESTED)}


def walk_entity_action(path, action):
    check_type(path, action, ENTITY_ACTIONS, "entity action")
    for sub in action.get("actions", []):
        if action.get("type") == "apoli:if_else_list":
            walk_condition(path, sub.get("condition"), ENTITY_CONDITIONS, "entity condition", ENTITY_NESTED)
            walk_entity_action(path, sub.get("action", {}))
        else:
            walk_entity_action(path, sub)


def check_power(path, power, top_level):
    check_type(path, power, POWER_TYPES, "power")
    if "condition" in power:
        walk_condition(path, power["condition"], ENTITY_CONDITIONS, "entity condition", ENTITY_NESTED)
    if "item_condition" in power:
        walk_condition(path, power["item_condition"], ITEM_CONDITIONS, "item condition", ITEM_NESTED)
    if "damage_condition" in power:
        walk_condition(path, power["damage_condition"], DAMAGE_CONDITIONS, "damage condition", DAMAGE_NESTED)
    for key in power:
        if key == "entity_action" or key.startswith("entity_action_"):
            walk_entity_action(path, power[key])
    if "bientity_action" in power:
        check_type(path, power["bientity_action"], BIENTITY_ACTIONS, "bi-entity action")
    if power.get("type") == "apoli:multiple":
        for key, sub in power.items():
            if key not in POWER_META_KEYS:
                check_power(path, sub, False)
    return power


def main():
    for path in sorted(ROOT.rglob("*.json")) + sorted(ROOT.rglob("*.mcmeta")):
        if ".git" not in path.parts and "dist" not in path.parts:
            load(path)

    meta = load(ROOT / "pack.mcmeta")
    if meta and meta.get("pack", {}).get("pack_format") != 15:
        err(ROOT / "pack.mcmeta", "pack_format must be 15 for Minecraft 1.20.1")

    lang = load(ROOT / "assets/pooltoy/lang/en_us.json") or {}
    used_keys = set()

    layer = load(ROOT / "data/origins/origin_layers/origin.json") or {}
    if layer.get("replace") is not False:
        err(ROOT / "data/origins/origin_layers/origin.json", '"replace" must be false')

    for origin_id in layer.get("origins", []):
        ns, name = origin_id.split(":")
        origin_path = ROOT / f"data/{ns}/origins/{name}.json"
        origin = load(origin_path) if origin_path.exists() else err(origin_path, "missing origin file")
        if not origin:
            continue
        used_keys.update([origin.get("name"), origin.get("description")])
        for power_id in origin.get("powers", []):
            pns, pname = power_id.split(":")
            power_path = ROOT / f"data/{pns}/powers/{pname}.json"
            if not power_path.exists():
                err(origin_path, f"references missing power {power_id}")
                continue
            power = load(power_path)
            if not power:
                continue
            check_power(power_path, power, True)
            if power.get("hidden") is not False:
                err(power_path, '"hidden" should be false so it shows in the origin tooltip')
            for key in ("name", "description"):
                expected = f"power.{pns}.{pname}.{key}"
                if power.get(key) != expected:
                    err(power_path, f"{key} should be {expected!r}")
                used_keys.add(expected)

    for dt_path in sorted((ROOT / "data").glob("*/damage_type/*.json")):
        used_keys.add(f"death.attack.{(load(dt_path) or {}).get('message_id')}")

    for key in sorted(k for k in used_keys if k):
        if key not in lang:
            err(ROOT / "assets/pooltoy/lang/en_us.json", f"missing translation {key!r}")
    for key in sorted(set(lang) - used_keys):
        err(ROOT / "assets/pooltoy/lang/en_us.json", f"unused translation {key!r}")

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    print("OK: all JSON valid, all type IDs verified, all links and translations present.")


if __name__ == "__main__":
    main()
