import argparse
import asyncio
import os
from logger import get_logger
from mistralai import Mistral

# VARIABLES
userInput: str
model: str = "mistral-tiny"

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

def mistral_check(apiKey):
    """
    Check if Mistral API key is valid by sending it a 'bonjour' message

    If key is valid a welcome message is displayed
    """
    client = Mistral(api_key=apiKey)
    response = client.chat.complete(
        model=model,
        messages=[
             {
                  "role": "user",
                  "content": "Ne dis rien d'autre que bonjour",
             },
        ],
    )

    # Displaying Mistral answer as validation
    print("Mistral: ", end = "")
    print(response.choices[0].message.content)

async def main():
    args = parse_arguments()

    # Initiating logger
    logLevel = args.logLevel
    logger = get_logger("logs", "ai-playground", logLevel)
    logger.info("Program has started")

    # Retrieve the API key as an environment variable
    try:
        api_key = os.environ["MISTRAL_API_KEY"]
    except Exception:
        logger.error("Env var MISTRAL_API_KEY not found in PATH, exiting...")
        exit(1)

    # Initiate Mistral by checking if API Key is valid
    try:
        logger.debug("Initiating Mistral API key check")
        mistral_check(api_key) 
    except Exception as error:
        logger.error(error)
        logger.error("Program exited due to error, check the error message above")
        exit(1)
    else:

        logger.debug("APY key seems valid, proceeding...")

    client = Mistral(api_key=api_key)

    while True:
        # Resetting the user input value to avoid repeating
        userInput = None

        # Do nothing while user hasn't typed anything
        while not userInput:
            print("(écrire 'quit' pour quitter à tout moment)")
            print()
            userInput = input("Vous: ")

        # Quitting program properly
        if "quit" in userInput:
            print("A la prochaine!")
            logger.info("Program exit initiated by user")
            exit(0)

        # Sending the user input to Mistral and wait for its answer
        response = await client.chat.stream_async(
            model=model,
            messages=[
                 {
                      "role": "user",
                      "content": userInput,
                  },
            ],
        )
        logger.debug("User sended prompt :" + userInput)

        # Displaying Mistral answer
        print("Mistral: ", end = "")
        async for chunk in response:
            if chunk.data.choices[0].delta.content is not None:
                print(chunk.data.choices[0].delta.content, end="")

        # Resetting the display
        print()


if __name__ == "__main__":
    asyncio.run(main())