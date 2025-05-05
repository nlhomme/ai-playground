import argparse
import asyncio
import os
import yaml
from logger import get_logger
from mistralai import Mistral

# VARIABLES
gameSelected: int
logger = ""
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
    If not, error is displayed
    """
    client = Mistral(api_key=apiKey)
    response = client.chat.complete(
        model=model,
        messages=[
             {
                  "role": "user",
                  "content": "Exprimes-toi en français. Ne dis rien d'autre que bonjour",
             },
        ],
    )

    # Return Mistral answer as validation
    return("Mistral: " + response.choices[0].message.content)

def game_loader():
    """
    List available games to the user

    User is asks to select a game
    Then its rules are returned to the main program
    """
    gameSelected: int = None

    # Opening the file containing games
    # and listing games
    logger.debug("Loading games from games/fr-games.yaml")
    with open('games/fr-games.yaml', 'r', encoding='utf-8') as file:
        games = yaml.safe_load(file)

        for list in games['games']:
            print(f"{list['number']} - {list['title']} - {list['summary']}")

    while True:
        logger.debug("Asking user to pick a game or quit")
        gameSelected = input("Saisir le numéro du jeu auquel jouer, ou 'quit' pour quitter: ")

        logger.debug("User chose " + gameSelected)

        if "quit" in gameSelected:
            print("A la prochaine!")
            logger.info("Program exit initiated by user")
            exit(0)

        # Finding the selected game and returning its rules
        try:
            for game in games['games']:
                if game['number'] == int(gameSelected):
                    logger.debug("User selected game" + game['title'])
                    return game['rules']
        except ValueError:
            logger.debug("Invalid value typed")
            continue

        # Returning an error message if invalid value or no value typed
        print("Il n'y a pas de jeu " + gameSelected)
        logger.debug("User selected game " + gameSelected + " which does not exists")
        print()

async def main():
    args = parse_arguments()

    # Initiating logger globally
    logLevel = args.logLevel
    global logger
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
        print(mistral_check(api_key))
    except Exception as error:
        logger.error(error)
        logger.error("Program exited due to error, check the error message above")
        exit(1)
    else:
        logger.debug("APY key seems valid, proceeding...")
        client = Mistral(api_key=api_key)

    # Getting games rules as the first prompt to Mistral
    userInput = "Jouons à ce jeu" + game_loader()

    while True:
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

        # Resetting the display and user input
        print()
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


if __name__ == "__main__":
    asyncio.run(main())