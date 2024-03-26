from pandas import read_csv
from random import randint
import os


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
        df = read_csv(filename, header=None)
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
            self.word_state += letter if letter in self.guessed_letters else "_"
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
        while len(self.failed_letters) < 6 and "_" in self.word_state:
            os.system("cls")
            self.print_game_board()
            guess = input("Guess a letter: ")
            if self.is_valid_guess(guess):
                guess = guess.lower()
                if guess in self.target_word:
                    self.guessed_letters.append(guess)
                    self.update_word_state()
                else:
                    self.failed_letters.append(guess)
                self.print_game_board()

        return "_" not in self.word_state

    def play(self) -> None:
        if self.get_number_of_words() >= 30:
            self.target_word = self.select_random_word()
            self.update_word_state()
            victory = self.game_loop()
            print("You won!" if victory else "The word was: '" + self.target_word + "'")
