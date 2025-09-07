# put near top of your module
import ast
import os
import re
from typing import List, Optional, Tuple

import discord
from discord import app_commands

WEAKNESS_CHART_FILE = os.path.join(
    "shared_utils", "pokemon_utils", "pokemon_autocomplete", "weakness_chart.py"
)


def load_weakness_chart():
    with open(WEAKNESS_CHART_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    parsed = ast.parse(content)
    weakness_chart = None
    for node in parsed.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            if node.targets[0].id == "weakness_chart":
                weakness_chart = ast.literal_eval(node.value)

    if weakness_chart is None:
        raise ValueError("Could not find weakness_chart dict in the file.")

    return weakness_chart


WEAKNESS_CHART = load_weakness_chart()


# build quick indexes once (call at import)
def build_weakness_indexes(weakness_chart: dict):
    dex_to_key = {}
    key_normalized = {}  # normalized name -> key (helps matching)
    for key, data in weakness_chart.items():
        dex_raw = data.get("dex")
        try:
            dex_int = int(dex_raw) if dex_raw is not None else None
        except Exception:
            dex_int = None

        if dex_int is not None:
            dex_to_key[dex_int] = key

        # normalized variants for lookups
        norm = key.lower()
        norm = norm.replace("-", " ").replace("_", " ").strip()
        key_normalized[norm] = key
        # also store punctuation-free version
        simple = re.sub(r"[^\w\s]", "", norm)
        key_normalized[simple] = key

    return dex_to_key, key_normalized


# create indexes (replace WEAKNESS_CHART with your dict)
DEX_TO_KEY, KEY_NORMALIZED = build_weakness_indexes(WEAKNESS_CHART)


# -------------------------- Autocomplete function --------------------------
# -------------------------- Autocomplete function --------------------------
async def pokemon_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[app_commands.Choice[str]]:
    current = (current or "").lower().strip()
    results: list[app_commands.Choice[str]] = []

    # normalize user input once
    norm_current = re.sub(r"[^\w\s]", "", current)

    matched_keys: set[str] = set()

    # 🔹 1. Match dex numbers quickly
    if current.isdigit():
        dex = int(current)
        if dex in DEX_TO_KEY:
            matched_keys.add(DEX_TO_KEY[dex])

    # 🔹 2. Match by normalized name
    if norm_current in KEY_NORMALIZED:
        matched_keys.add(KEY_NORMALIZED[norm_current])
    else:
        # substring search in normalized keys
        for norm, key in KEY_NORMALIZED.items():
            if norm_current and norm_current in norm:
                matched_keys.add(key)
                if len(matched_keys) >= 25:  # limit early
                    break

    # 🔹 3. Build choices from matched keys
    for key in matched_keys:
        data = WEAKNESS_CHART.get(key, {})
        dex_raw = data.get("dex")
        try:
            dex_int = int(dex_raw) if dex_raw else None
        except ValueError:
            dex_int = None

        if dex_int:
            display = f"{key.title()} #{dex_int}"
        else:
            display = key.title()

        results.append(app_commands.Choice(name=display, value=key.title()))

        if len(results) >= 25:
            break

    # 🔹 4. Fallback if nothing matched
    return results or [
        app_commands.Choice(name="❌ No matches found", value="__invalid__")
    ]
