import asyncio
import sys
import os
import importlib

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the module itself
module_name = "shared_utils.pokemon_utils.pokemon_gif.get_pokemon_gif"
get_pokemon_gif_module = importlib.import_module(module_name)
importlib.reload(get_pokemon_gif_module)
get_pokemon_gif = get_pokemon_gif_module.get_pokemon_gif


async def main():
    input_name = input("Enter Pokémon name (e.g., shiny charizard-mega): ").strip()
    result = await get_pokemon_gif(input_name)
    print("\n✅ Pokémon GIF Info:")
    print(f"Input Name : {input_name}")
    print(f"GIF URL    : {result}")


if __name__ == "__main__":
    asyncio.run(main())
