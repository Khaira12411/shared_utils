# -------------------- Pokemon GIF Retriever --------------------
from typing import Literal
from .gif_data import *


async def get_pokemon_gif(
    input_name: str,
) -> dict[str, str | bool]:
    """
    Returns Pokémon GIF info instead of directly modifying an embed.
    Handles shiny, mega, gmax, alolan, galarian, golden forms.

    Returns a dict:
    {
        "gif_url": str | None,
        "form": "regular" | "mega" | "gmax",
        "golden": bool,
        "shiny": bool,
        "error": str | None
    }
    """
    original_input = input_name
    shiny = False
    golden = False
    form: Literal["regular", "mega", "gmax"] = "regular"
    region_suffix = ""

    # Normalize
    name_parts = input_name.lower().replace("_", "-").split()

    # Detect golden
    if "golden" in name_parts:
        golden = True
        name_parts.remove("golden")

    # Detect shiny
    if "shiny" in name_parts:
        shiny = True
        name_parts.remove("shiny")

    # Regional forms
    if "alolan" in name_parts:
        region_suffix = "-alola"
        name_parts.remove("alolan")
    elif "galarian" in name_parts:
        region_suffix = "-galar"
        name_parts.remove("galarian")

    # Mega / Gigantamax
    remaining_name = "-".join(name_parts)
    if remaining_name.startswith("mega-"):
        form = "mega"
        remaining_name = remaining_name.replace("mega-", "")
    elif remaining_name.startswith("gigantamax-") or remaining_name.startswith("gmax-"):
        form = "gmax"
        remaining_name = remaining_name.replace("gigantamax-", "").replace("gmax-", "")

    base_name = remaining_name + region_suffix

    # Special Gmax cases
    gmax_aliases = {"urshifu-rapidstrike": "urs", "urshifu-singlestrike": "uss"}
    if form == "gmax" and remaining_name in gmax_aliases:
        remaining_name = gmax_aliases[remaining_name]

    # -------------------- Determine GIF URL --------------------
    gif_url = None

    # 1️⃣ Try to fetch from class based on golden/regular
    if golden:
        normalized_name = remaining_name.replace("-", "_")
        gif_url = getattr(GOLDEN_POKEMON_URL, normalized_name, None)
    else:
        gif_url = getattr(REGULAR_POKEMON_URL, remaining_name, None)

    # 2️⃣ Handle Gmax separately using hardcoded maps
    if form == "gmax":
        if shiny:
            gif_url = getattr(SHINY_GMAX_URL, remaining_name, None)
        else:
            gif_url = getattr(REGULAR_GMAX_URL, remaining_name, None)

    # 3️⃣ Fallback to Showdown URL
    if not gif_url:
        shiny_prefix = "ani-shiny" if shiny else "xyani"
        suffix = "" if form == "regular" else f"-{form}"
        gif_url = f"https://play.pokemonshowdown.com/sprites/{shiny_prefix}/{base_name}{suffix}.gif?quality=lossless"

    # Error handling
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
