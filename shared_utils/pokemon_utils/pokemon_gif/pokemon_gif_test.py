# pokemon_gif_test.py
import asyncio
from shared_utils.pokemon_utils.pokemon_gif.get_pokemon_gif import get_pokemon_gif

async def main():

    # Take input from the user
    input_name = input("Enter Pokémon name (e.g., shiny charizard-mega): ").strip()

    # Get GIF info
    result = await get_pokemon_gif(input_name)

    # Display output in terminal
    print("\n✅ Pokémon GIF Info:")
    print(f"GIF URL : {result['gif_url']}")
    print(f"Form    : {result['form']}")
    print(f"Shiny   : {result['shiny']}")
    print(f"Golden  : {result['golden']}")
    if result["error"]:
        print(f"Error   : {result['error']}")


if __name__ == "__main__":
    asyncio.run(main())
