import asyncio
import os

from mistralai import Mistral

# VARIABLES
userInput: str


async def main():
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-tiny"

    client = Mistral(api_key=api_key)

    print("Welcome")
    print()

    while True:
        # Reset the user input value to avoid repeating
        userInput = None

        # Do nothing while user hasn't typed anything
        while not userInput:
            print("(écrire 'quit' pour quitter à tout moment)")
            print()
            userInput = input("Vous: ")


        # Quit program properly
        if "quit" in userInput:
            print("A la prochaine!")
            exit(0)

        # Send user input to Mistral and wait for its answer
        response = await client.chat.stream_async(
            model=model,
            messages=[
                 {
                      "role": "user",
                      "content": userInput,
                  },
            ],
        )

        # Display Mistral answer
        print("Mistral: ", end = "")
        async for chunk in response:
            if chunk.data.choices[0].delta.content is not None:
                print(chunk.data.choices[0].delta.content, end="")

        # Reset the display
        print()


if __name__ == "__main__":
    asyncio.run(main())