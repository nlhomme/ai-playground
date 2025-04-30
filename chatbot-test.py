import argparse
import asyncio
import os
from logger import get_logger
from mistralai import Mistral

# VARIABLES
userInput: str

def parse_arguments():
    """
    Allow user to manually set the log level beetween DEBUG, INFO (default value), WARNING, ERROR AND CRITICAL

    Example:
    ```
        chatbot-test.py --logLevel DEBUG
    ```

    Show a help message via the '-t' argument
    """
    parser = argparse.ArgumentParser(description="Requirements to use the AI playground chatbot")
    parser.add_argument("--logLevel", required=False, type=str, default="INFO", help="Log level between DEBUG, INFO, WARNING, ERROR AND CRITICAL (default set to INFO)")
    return parser.parse_args()

async def main():
    args = parse_arguments()

    # Initiating logger
    logLevel = args.logLevel
    logger = get_logger("logs", "ai-playground", logLevel)
    logger.info(f"Program has started")

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
            logger.info(f"Program exit initiated by user")
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
        logger.debug(f"User sended prompt :" + userInput)

        # Display Mistral answer
        print("Mistral: ", end = "")
        async for chunk in response:
            if chunk.data.choices[0].delta.content is not None:
                print(chunk.data.choices[0].delta.content, end="")

        # Reset the display
        print()


if __name__ == "__main__":
    asyncio.run(main())