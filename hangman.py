# Project Name: Hangman
# Version: 1.0
# Author: Brendan Langenhoff (brend-designs)
# Description: A simple game of Hangman using console/terminal

# TODO: Update to using a GUI instead of console

import random
import enum
from words import word_list


# Store game variables in a class/object, for easier passing between functions.
class Game:
    word = ""
    word_completion = ""
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    def __init__(self, word):
        self.word = word
        self.word_completion = "_" * len(word)


# Enum for types of guesses during the game
class GuessType(enum.Enum):
    LETTER = "letter"
    WORD = "word"


# Get a random word from a static list defined in words.py
def get_word(): return random.choice(word_list).upper()


# This function renders the game within the console
# Parameters:
#   "game": Reference to our game object
#   "starting": True if game is starting, else false
def render(game, starting):
    if starting:
        print("Let's play Hangman!")
    print(display_hangman(game.tries) + "\n"
          + game.word_completion + "\n")


# This function adds a letter or word, to the guessed letters or words list.
# Parameters:
#   "game": Reference to our game object
#   "guess_type": Type of guess (letter or word)
#   "guess": The letter or word that's been guessed
#   "count-try": Count this guess against their number of tries
def add_guess(game, guess_type, guess, count_try):
    if count_try:
        game.tries -= 1

    if guess_type == GuessType.LETTER:
        game.guessed_letters.append(guess)
    else:
        game.guessed_words.append(guess)


# This function updates the completion of the word
# Parameters:
#   "game": Reference to our game object
#   "guess_type": Type of guess (letter or word)
#   "guess": The letter or word that's been guessed
def update_word_completion(game, guess_type, guess):
    if guess_type == GuessType.WORD:
        game.word_completion = game.word
    else:
        word_as_list = list(game.word_completion)

        # Iterate through word to find the indexes of where this letter is within said word
        indices = [i for i, letter in enumerate(game.word) if letter == guess]

        for index in indices:  # Loop through indexes of the guessed letter within the word
            word_as_list[index] = guess
        game.word_completion = "".join(word_as_list)

    if "_" not in game.word_completion:  # Word has been guessed
        game.guessed = True


# This function handles the game (Hangman) logic.
# Parameter: "word": The random word that is trying to be guessed.
def play(word):
    game = Game(word)
    render(game, True)

    while not game.guessed and game.tries > 0:
        guess = input("Please guess a letter or word: ").upper()

        if len(guess) == 1 and guess.isalpha():
            guess_type = GuessType.LETTER

            if guess in game.guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                add_guess(game, guess_type, guess, True)
            else:
                print("Good job,", guess, "is in the word!")
                add_guess(game, guess_type, guess, False)
                update_word_completion(game, guess_type, guess)
        elif len(guess) == len(word) and guess.isalpha():
            guess_type = GuessType.WORD

            if guess in game.guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                add_guess(game, guess_type, guess, True)
            else:
                game.guessed = True
                update_word_completion(game, guess_type, guess)
        else:
            print("Not a valid guess.")
        render(game, False)  # Re-render Hangman

    if game.guessed:
        print("Congrats, you guessed the word! You win!")
    else:
        print("Sorry, you ran out of tries. The word was " +
              word + ". Maybe next time!")


# This function just lays out Hangman at a particular stage/try.
# Putting this towards the end as it's quite a long function.
def display_hangman(tries):
    stages = [  # Final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # Head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # Head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # Head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # Head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # Head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # Initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]


def main():
    word = get_word()
    play(word)
    while input("Play Again? (Y/N)").upper() == "Y":
        word = get_word()
        play(word)


if __name__ == "__main__":
    main()
