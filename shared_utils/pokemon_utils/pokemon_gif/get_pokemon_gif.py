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

    # -------------------- Normalize input --------------------
    name_parts = input_name.lower().replace("_", "-").split()

    # -------------------- Detect special forms --------------------
    if "golden" in name_parts:
        golden = True
        name_parts.remove("golden")

    if "shiny" in name_parts:
        shiny = True
        name_parts.remove("shiny")

    # Join remaining parts
    remaining_name = "-".join(name_parts)

    # -------------------- Detect region forms --------------------
    regions = {"alolan": "-alola", "galarian": "-galar", "hisuian": "-hisui"}
    for region_prefix, suffix in regions.items():
        if remaining_name.startswith(region_prefix + "-"):
            region_suffix = suffix
            remaining_name = remaining_name[len(region_prefix) + 1 :]
            break

    # -------------------- Mega / Gigantamax --------------------
    if remaining_name.startswith("mega-"):
        form = "mega"
        remaining_name = remaining_name.replace("mega-", "")
    elif remaining_name.startswith(("gigantamax-", "gmax-")):
        form = "gmax"
        remaining_name = remaining_name.replace("gigantamax-", "").replace("gmax-", "")

    # Special Gmax aliases
    gmax_aliases = {"urshifu-rapidstrike": "urs", "urshifu-singlestrike": "uss"}
    if form == "gmax" and remaining_name in gmax_aliases:
        remaining_name = gmax_aliases[remaining_name]

    # -------------------- Base name --------------------
    base_name = f"{remaining_name}{region_suffix}".lower()

    # -------------------- Attribute names --------------------
    regular_attr_name = remaining_name.replace("-", "_")
    golden_attr_name = remaining_name.replace("-", "_")

    # -------------------- Determine GIF URL --------------------
    gif_url = None

    # 1️⃣ Local data
    if golden:
        gif_url = getattr(GOLDEN_POKEMON_URL, golden_attr_name, None)
    else:
        gif_url = getattr(REGULAR_POKEMON_URL, regular_attr_name, None)

    # 2️⃣ Gmax special handling
    if form == "gmax":
        gif_url = getattr(
            SHINY_GMAX_URL if shiny else REGULAR_GMAX_URL, regular_attr_name, gif_url
        )

    # 3️⃣ Fallback to Showdown
    if not gif_url:
        shiny_prefix = "ani-shiny" if shiny else "xyani"
        suffix = "" if form == "regular" else f"-{form}"
        gif_url = f"https://play.pokemonshowdown.com/sprites/{shiny_prefix}/{base_name}{suffix}.gif?quality=lossless"

    # -------------------- Error Handling --------------------
    error = None
    if not gif_url:
        error = f"Cannot find Pokémon GIF for '{original_input}'"

    return {
        "gif_url": gif_url,
        "form": form,
        "golden": golden,
        "shiny": shiny,
        "error": error,
    }
