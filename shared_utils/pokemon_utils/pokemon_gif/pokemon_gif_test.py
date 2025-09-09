# pokemon_gif_test.py
import asyncio
import sys
import os

# -------------------- Force fresh import --------------------
# Add project root to sys.path to avoid import conflicts
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Remove cached module
sys.modules.pop("shared_utils.pokemon_utils.pokemon_gif", None)

# Import the module fresh
from shared_utils.pokemon_utils import pokemon_gif

get_pokemon_gif = pokemon_gif.get_pokemon_gif


# -------------------- Test runner --------------------
async def main():
    input_name = input("Enter Pokémon name (e.g., shiny charizard-mega): ").strip()

    # Call the function (debug prints inside get_pokemon_gif will show)
    result = await get_pokemon_gif(input_name)

    print("\n✅ Pokémon GIF Info:")
    print(f"Input Name : {input_name}")
    print(f"GIF Name   : {result.get('gif_name')}")
    print(f"GIF URL    : {result['gif_url']}")
    print(f"Form       : {result['form']}")
    print(f"Shiny      : {result['shiny']}")
    print(f"Golden     : {result['golden']}")
    if result["error"]:
        print(f"Error      : {result['error']}")


if __name__ == "__main__":
    asyncio.run(main())
