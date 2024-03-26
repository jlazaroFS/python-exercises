import pandas as pd
from random import randint
import os
import uuid
from datetime import datetime


class Hangman:
    """A class to represent a game of Hangman."""

    def __init__(self) -> None:
        """Default constructor, initializes the game and loads the CSV file with the words."""
        self.guessed_letters = []
        self.failed_letters = []
        filename = "words.csv"
        self.words = self.load(filename)

    def load(self, filename: str) -> list[str]:
        """Loads the words in the CSV file and stores them in a list."""
        df = pd.read_csv(filename, header=None)
        words_list = df[0].tolist()
        return words_list

    def get_number_of_words(self) -> int:
        """Counts the number of words on the file."""
        number_of_words = len(self.words)
        if number_of_words < 30:
            print("Not enough words. Game failed to start.")
        else:
            print("Words loaded. Ready!")
        return number_of_words

    def select_random_word(self) -> str:
        """Returns a word at random from the ones loaded."""
        random_index = randint(0, len(self.words) - 1)
        return self.words[random_index]

    def print_game_board(self) -> None:
        """Prints the game board."""
        self.print_hangman()
        print(self.failed_letters)

    def print_hangman(self) -> None:
        """Prints the hanged man depending on the number of failed guesses."""
        fails = len(self.failed_letters)

        head_art = "O"
        torso_art = "\\|/"
        legs_art = "/\\"
        pole = "  |        "

        hanged_art = (
            "  ----------\n"
            + pole
            + "|\n"
            + pole
            + (head_art if fails >= 1 else "")
            + "\n"
            + pole[:-1]
            + (torso_art[: fails - 1] if fails >= 2 else "")
            + "\n"
            + pole
            + (legs_art[: fails - 4] if fails >= 5 else "")
            + "\n"
            + "  |\n"
            + "-------\t\t"
            + self.word_state
        )

        print(hanged_art)

    def update_word_state(self):
        """Updates with the letters of the word that the user has guessed correctly."""
        self.word_state = ""
        for letter in self.target_word:
            self.word_state += letter if letter in self.guessed_letters else "·"
        self.word_state += " "

    def is_valid_guess(self, guess: str) -> bool:
        """Returns True if the guess is a new, single letter."""
        if len(guess) != 1:
            return False
        if not guess.isalpha():
            return False
        return guess.lower() not in self.guessed_letters + self.failed_letters

    def game_loop(self) -> bool:
        """Main game loop. Returns True if user guessed the word, False otherwise."""
        while len(self.failed_letters) < 6 and "·" in self.word_state:
            self.print_game_board()
            guess = input("Guess a letter: ")
            # os.system("cls")
            if self.is_valid_guess(guess):
                guess = guess.lower()
                if guess in self.target_word:
                    self.guessed_letters.append(guess)
                    self.update_word_state()
                else:
                    self.failed_letters.append(guess)
                self.print_game_board()
            else:
                print("Invalid guess. Try again.")

        return "·" not in self.word_state

    def play(self) -> None:
        """Starts a game of Hangman if there are at least 30 words."""
        if self.get_number_of_words() >= 30:
            username = input("What's your name? ")
            start_date = datetime.now()
            game_id = uuid.uuid1().int
            score = 0
            round_id = 1
            while round_id <= 3:
                self.failed_letters = []
                self.guessed_letters = []
                self.target_word = self.select_random_word()
                self.update_word_state()
                victory = self.game_loop()
                score += victory
                print(
                    "You won!"
                    if victory
                    else "The word was: '" + self.target_word + "'."
                )
                self.store_round_stats(
                    game_id,
                    self.target_word,
                    username,
                    round_id,
                    len(self.failed_letters),
                    victory,
                )
                round_id += 1

            end_date = datetime.now()
            self.store_game_stats(game_id, username, start_date, end_date, score)

    def store_round_stats(
        self, game_id, word, username, round_id, user_tries, victory
    ) -> None:
        """Stores the stats in rounds_in_games.csv"""
        if not os.path.exists("rounds_in_games.csv"):
            df = pd.DataFrame(
                columns=[
                    "game_id",
                    "word",
                    "username",
                    "round_id",
                    "user_tries",
                    "victory",
                ]
            )
            df.to_csv("rounds_in_games.csv", index=False)
        data = {
            "game_id": game_id,
            "word": word,
            "username": username,
            "round_id": round_id,
            "user_tries": user_tries,
            "victory": victory,
        }
        df = pd.DataFrame([data])
        df.to_csv(
            "rounds_in_games.csv",
            mode="a",
            index=False,
            header=not pd.read_csv("rounds_in_games.csv").empty,
        )

    def store_game_stats(
        self, game_id, username, start_date, end_date, final_score
    ) -> None:
        """Stores the stats in games.csv"""
        if not os.path.exists("games.csv"):
            df = pd.DataFrame(
                columns=["game_id", "username", "start_date", "end_date", "final_score"]
            )
            df.to_csv("games.csv", index=False)
        data = {
            "game_id": game_id,
            "username": username,
            "start_date": start_date,
            "end_date": end_date,
            "final_score": final_score,
        }
        df = pd.DataFrame([data])
        df.to_csv(
            "games.csv",
            mode="a",
            index=False,
            header=not pd.read_csv("games.csv").empty,
        )
