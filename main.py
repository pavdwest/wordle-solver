from wordle_game import WordleGame

def get_most_common_letters(words):
    letter_frequencies = []
    letters_count = 0
    for i in range(26):
        letter_frequencies.append(
            {
                'letter': chr(i + 97),
                'frequency': 0,
                'score': 0
            }
        )

    for word in words:
        for letter in word:
            letters_count += 1
            try:
                idx = ord(letter) - 97
                if is_valid_letter(letter):
                    letter_frequencies[idx]['frequency'] += 1
            except:
                print(f"word: {word} | letter: {letter}")

    letter_frequencies_sorted = sorted(letter_frequencies, key=lambda d: d['frequency'], reverse=True)

    for l in letter_frequencies_sorted:
        l['score'] = l['frequency'] / letters_count

    return letter_frequencies_sorted


def get_words_scores(words, words_frequencies):
    words_scores = []
    for word in words:
        word_score = 0
        letters_used = []
        for letter in word:
            try:
                if not letter in letters_used:
                    word_score += words_frequencies[ord(letter) - 97]['score']
            except:
                print(f"word: {word} | letter: {letter}")
            letters_used.append(letter)


        words_scores.append({'word': word, 'score': word_score})

    words_scores_sorted = sorted(words_scores, key=lambda d: d['score'], reverse=True)
    print("=================")
    print("=== Top words ===")
    print("=================")
    print(words_scores_sorted[:30])
    return words_scores_sorted


def is_valid_letter(letter):
    return 97 <= ord(letter) <= 122


def load_words():
    words = []
    # with open('words.txt', newline='') as csvfile:
    # with open('wordlist.txt', newline='') as csvfile:
    with open('wordlist.txt', newline='') as csvfile:
        for row in csvfile.readlines():
            # word = (row.split(" ")[0]).lower().strip()
            word = row.lower().strip()
            if '.' in word:
                continue

            word = word.replace('\n', '')
            word = word.replace('-','')
            word = word.replace("'", '')
            word = word.replace("é", 'e')
            word = word.replace("ü", 'u')
            word = word.replace("ö", 'o')
            word = word.replace("ô", 'o')
            word = word.replace("ó", 'o')
            word = word.replace("ê", 'e')

            is_invalid = False
            for letter in word:
                if not is_valid_letter(letter):
                    is_invalid = True
                    continue

            # TODO: exclude words with characters occurring twice
            if(len(word) == 5 and not is_invalid):
                words.append(word)
    return words


def main():
    # exclude_previous_guesses = False
    exclude_previous_guesses = True
    words = load_words()
    letters_frequencies = get_most_common_letters(words)
    words_scores = get_words_scores(words, letters_frequencies)

    games = []
    # with open('results_pwn.csv', 'w') as f:
    # with open('results_pwn2.csv', 'w') as f:
    with open('results_bry.csv', 'w') as f:
        f.write('game,word,score,fallback\n')
        for idx, word in enumerate(words):
            print(f"Playing game {idx} of {len(words)}...")
            g = WordleGame(word)
            games.append(g)

            initial_guess = words_scores[0]['word']
            guesses = []
            guesses.append(
                {
                    'word': initial_guess,
                    'outcome': g.guess(initial_guess),
                }
            )

            # Second guess
            fallback = False
            if not g.completed:
                next_guess = get_next_most_likely_word(
                    words=words_scores,
                    guesses=guesses,
                    count=1,
                    exclude_previous_guesses=exclude_previous_guesses,
                )

                if exclude_previous_guesses and len(next_guess) < 1:
                    print("FALLBACK ON OTHER STRAT")
                    fallback = True
                    next_guess = get_next_most_likely_word(
                        words=words_scores,
                        guesses=guesses,
                        count=1,
                        exclude_previous_guesses=False,
                    )

                guesses.append(
                    {
                        'word': next_guess[0]['word'],
                        'outcome': g.guess(next_guess[0]['word']),
                    }
                )


            while not g.completed:
                next_guess = get_next_most_likely_word(
                    words=words_scores,
                    guesses=guesses,
                    count=1,
                    exclude_previous_guesses=False,
                )
                if len(next_guess) < 1:
                    import code; code.interact(local=dict(globals(), **locals()))
                guesses.append(
                    {
                        'word': next_guess[0]['word'],
                        'outcome': g.guess(next_guess[0]['word']),
                    }
                )

            f.write(f"{idx},{word},{g.score()},{'True' if fallback else 'False'}\n")


def get_next_most_likely_word(
    words,
    guesses,
    count=1,
    exclude_previous_guesses=False,
):
    excluded_letters = []
    places_letters = []
    excluded_words = []
    wrong_places = []

    for i in range(5):
        places_letters.append(
            {
                'pos': i,
                'known': None,
                'wrong_place': []
            }
        )

    for guess in guesses:
        excluded_words.append(guess['word'])
        for letter_idx, letter in enumerate(guess['word']):
            letter_outcome = guess['outcome'][letter_idx]
            if letter_outcome == '0':
                excluded_letters.append(letter)
            elif letter_outcome == '1':
                places_letters[letter_idx]['wrong_place'].append(letter)
            elif letter_outcome == '2':
                places_letters[letter_idx]['known'] = letter

    # Flatten wrong places to single list for lookups
    t = [i['wrong_place'] for i in places_letters]
    all_wrong_places = [i for sublist in t for i in sublist]
    letters_open_for_wrong_places = [s for s in places_letters if s['known'] is None]

    # print(f"places_letters: {places_letters}")
    # print(f"excluded_words: {excluded_words}")
    # print(f"excluded_letters: {excluded_letters}")
    # print(f"all_wrong_places: {all_wrong_places}")
    # print(f"slots_open_for_wrong_places: {letters_open_for_wrong_places}")

    words_found = []

    for word_ob in words:
        word = word_ob['word']
        # print(f"XXXXXXXXXXXXXXXX Current word: {word}")
        # print(f"opens {letters_open_for_wrong_places}")
        is_invalid = False

        # Word must not have been used in previous guesses
        if word in excluded_words:
            is_invalid = True
            continue

        if not exclude_previous_guesses:
            # All wrong place letters must be in the word
            if not all(i in list(word) for i in all_wrong_places):
                continue
        else:
            if all(i in list(word) for i in all_wrong_places):
                continue

        for letter_idx, letter in enumerate(word):
            # Word must not contain an excluded letter
            if letter in excluded_letters:
                is_invalid = True
                break

            # Word must contain all known letters in the correct places
            known_letter = places_letters[letter_idx]['known']

            # Optional don't use any previous info
            if exclude_previous_guesses:
                # If word contains any of the previous correct letters, skip it
                if letter == known_letter:
                    is_invalid = True
                    break    # Can actually skip whole word
            else:
                if known_letter is not None:
                    if letter != known_letter:
                        is_invalid = True
                        break    # Can actually skip whole word

            # Word must not have a wrong_place letter in the same wrong_place place
            if letter in places_letters[letter_idx]['wrong_place']:
                is_invalid = True
                continue

        if is_invalid:
            continue
        else:
            words_found.append(word_ob)
            # print(f"FOUND word: {word_ob}")
            if(len(words_found) > count):
                return words_found
    return words_found

if __name__ == "__main__":
    main()
