class WordleGame:
    def __init__(self, word: str) -> None:
        self.word = word
        self.guesses = []
        self.completed = False

    def guess(self, guess: str):
        self.guesses.append(guess)
        res = ''
        for idx, letter in enumerate(guess):
            if letter == self.word[idx]:
                res += '2'
            elif letter in self.word:
                res += '1'
            else:
                res += '0'
        if res == '22222':
            print(f"Game complete: Guessed {self.word} in {self.score()}")
            self.completed = True

        return res

    def score(self):
        return len(self.guesses)
