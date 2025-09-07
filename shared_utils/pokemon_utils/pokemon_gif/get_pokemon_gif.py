from typing import Literal
from shared_utils.pokemon_utils.pokemon_gif.gif_data import *


async def get_pokemon_gif(input_name: str) -> dict[str, str | bool]:
    """
    Returns Pokémon GIF info, handling shiny, mega, gmax, alolan, galarian, hisuian, golden forms.
    """
    original_input = input_name
    shiny = False
    golden = False
    form: Literal["regular", "mega", "gmax"] = "regular"
    region_suffix = ""
    print("DEBUG: get_pokemon_gif.py loaded", flush=True)

    # -------------------- Normalize input --------------------
    name_parts = input_name.lower().replace("_", "-").split()
    print(f"DEBUG: name_parts after normalization = {name_parts}")

    # -------------------- Detect special forms --------------------
    if "golden" in name_parts:
        golden = True
        name_parts.remove("golden")
        print("DEBUG: Detected golden form")

    if "shiny" in name_parts:
        shiny = True
        name_parts.remove("shiny")
        print("DEBUG: Detected shiny form")

    # Join remaining parts
    remaining_name = "-".join(name_parts)
    print(f"DEBUG: remaining_name after normalization = {remaining_name}")

    # -------------------- Detect region forms --------------------
    regions = {"alolan": "-alola", "galarian": "-galar", "hisuian": "-hisui"}
    for region_prefix, suffix in regions.items():
        if remaining_name.startswith(region_prefix + "-"):
            region_suffix = suffix
            remaining_name = remaining_name[
                len(region_prefix) + 1 :
            ]  # remove prefix + dash
            print(
                f"DEBUG: Detected {region_prefix} form, remaining_name = {remaining_name}"
            )
            break

    # -------------------- Mega / Gigantamax --------------------
    if remaining_name.startswith("mega-"):
        form = "mega"
        remaining_name = remaining_name.replace("mega-", "")
        print("DEBUG: Detected mega form")
    elif remaining_name.startswith(("gigantamax-", "gmax-")):
        form = "gmax"
        remaining_name = remaining_name.replace("gigantamax-", "").replace("gmax-", "")
        print("DEBUG: Detected gmax form")

    # Special Gmax aliases
    gmax_aliases = {"urshifu-rapidstrike": "urs", "urshifu-singlestrike": "uss"}
    if form == "gmax" and remaining_name in gmax_aliases:
        remaining_name = gmax_aliases[remaining_name]
        print(f"DEBUG: Applied gmax alias, remaining_name = {remaining_name}")

    # -------------------- Base name --------------------
    base_name = f"{remaining_name}{region_suffix}".lower()
    print(f"DEBUG: base_name for Showdown URL = {base_name}")

    # -------------------- Attribute names --------------------
    regular_attr_name = remaining_name.replace("-", "_")
    golden_attr_name = remaining_name.replace("-", "_")
    print(
        f"DEBUG: regular_attr_name = {regular_attr_name}, golden_attr_name = {golden_attr_name}"
    )

    # -------------------- Determine GIF URL --------------------
    gif_url = None

    # 1️⃣ Local data
    if golden:
        gif_url = getattr(GOLDEN_POKEMON_URL, golden_attr_name, None)
        print(f"DEBUG: tried GOLDEN_POKEMON_URL.{golden_attr_name} -> {gif_url}")
    else:
        gif_url = getattr(REGULAR_POKEMON_URL, regular_attr_name, None)
        print(f"DEBUG: tried REGULAR_POKEMON_URL.{regular_attr_name} -> {gif_url}")

    # 2️⃣ Gmax special handling
    if form == "gmax":
        gif_url = getattr(
            SHINY_GMAX_URL if shiny else REGULAR_GMAX_URL, regular_attr_name, gif_url
        )
        print(f"DEBUG: GMAX URL fallback -> {gif_url}")

    # 3️⃣ Fallback to Showdown
    if not gif_url:
        shiny_prefix = "ani-shiny" if shiny else "xyani"
        suffix = "" if form == "regular" else f"-{form}"
        gif_url = f"https://play.pokemonshowdown.com/sprites/{shiny_prefix}/{base_name}{suffix}.gif?quality=lossless"
        print(f"DEBUG: Showdown fallback -> {gif_url}")

    # -------------------- Error Handling --------------------
    error = None
    if not gif_url:
        error = f"Cannot find Pokémon GIF for '{original_input}'"

    print(f"DEBUG: final gif_url = {gif_url}")
    print(f"DEBUG: form = {form}, shiny = {shiny}, golden = {golden}, error = {error}")

    return {
        "gif_url": gif_url,
        "form": form,
        "golden": golden,
        "shiny": shiny,
        "error": error,
    }
