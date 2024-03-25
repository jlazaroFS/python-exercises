import pandas as pd

class Hangman:
    """A class to represent a game of Hangman."""

    def __init__(self) -> None:
        """Default constructor, loads the CSV file containing the words."""
        filename = "words.csv"
        self.words = self.load(filename)
        if self.get_number_of_words() >= 30:
            print("Game loop (not yet implemented)")
    
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

