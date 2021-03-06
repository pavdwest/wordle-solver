from wordle_game import WordleGame


# Determines frequencies of letters in the given list of words.
# Frequencies over all letters sum to 1.0
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

    print(letter_frequencies_sorted)

    return letter_frequencies_sorted


# Assigns a score to each word based on the frequency distribution of the letters it's composed of
# e.g. 'If 'a' has a chance of 0.2 to occur and 's' has a chance of 0.12 to occur, 'ass' gets a score of 0.44
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


# Checks ASCII code of letter. Only use lower case.
def is_valid_letter(letter):
    return 97 <= ord(letter) <= 122


# Loads words from file and does some cleanup
def load_words(words_filename: str):
    words = []
    with open(words_filename, newline='') as csvfile:
        for row in csvfile.readlines():
            # word = (row.split(" ")[0]).lower().strip()
            word = row.lower().strip()
            if '.' in word:
                continue

            word = word.replace('\n', '')
            word = word.replace('-','')
            word = word.replace("'", '')
            word = word.replace("??", 'e')
            word = word.replace("??", 'u')
            word = word.replace("??", 'o')
            word = word.replace("??", 'o')
            word = word.replace("??", 'o')
            word = word.replace("??", 'e')

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
    import code; code.interact(local=dict(globals(), **locals()))
    # words_filename='words.txt'
    # words_filename='wordlist.txt'
    words_filename='wordle_history.txt'
    # words_filename='manual_list.txt'
    # words_filename='wordle_dictionary.txt'
    words = load_words(words_filename=words_filename)
    letters_frequencies = get_most_common_letters(words)
    words_scores = get_words_scores(words, letters_frequencies)

    # import code; code.interact(local=dict(globals(), **locals()))

    ##############
    ### Manual ###
    ##############
    exclude_previous_guesses = False
    # exclude_previous_guesses = True
    guesses = []
    guesses.append(
                {
                    'word': 'beach',
                    'outcome': '00100',
                }
            )

    guesses.append(
                {
                    'word': 'dogma',
                    'outcome': '00201',
                }
            )

    guesses.append(
                {
                    'word': 'angst',
                    'outcome': '10210',
                }
            )

    print("XXXXXXXXXXXXXXXXXXXXXXXX")
    print(get_next_most_likely_word(words_scores, guesses, count=10, exclude_previous_guesses=exclude_previous_guesses))
    ##############

    # ############
    # ### Auto ###
    # ############
    # exclude_previous_guesses = False
    # # exclude_previous_guesses = True
    # games = []
    # notify_every_n_games = 500
    # # with open('results/results_pwn.csv', 'w') as f:
    # # with open('results/results_pwn2.csv', 'w') as f:
    # with open('results/tmp.csv', 'w') as f:
    #     f.write('game,word,score,fallback\n')
    #     print("Starting simulation...")
    #     for idx, word in enumerate(words):
    #         # print(f"Playing game {idx} of {len(words)}...")

    #         if idx % notify_every_n_games == 0:
    #             print(f"Playing game {idx} of {len(words)}...")

    #         g = WordleGame(word)
    #         games.append(g)

    #         # Both strategies use the same initial guess
    #         initial_guess = words_scores[0]['word']
    #         guesses = []
    #         guesses.append(
    #             {
    #                 'word': initial_guess,
    #                 'outcome': g.guess(initial_guess),
    #             }
    #         )

    #         # Second guess
    #         fallback = False
    #         if not g.completed:
    #             next_guess = get_next_most_likely_word(
    #                 words=words_scores,
    #                 guesses=guesses,
    #                 count=1,
    #                 exclude_previous_guesses=exclude_previous_guesses,
    #             )

    #             # If this strategy doesn't produce a next guess we fall back to the initial strat.
    #             if exclude_previous_guesses and len(next_guess) < 1:
    #                 # print("FALLBACK ON OTHER STRAT")
    #                 fallback = True
    #                 next_guess = get_next_most_likely_word(
    #                     words=words_scores,
    #                     guesses=guesses,
    #                     count=1,
    #                     exclude_previous_guesses=False,
    #                 )

    #             guesses.append(
    #                 {
    #                     'word': next_guess[0]['word'],
    #                     'outcome': g.guess(next_guess[0]['word']),
    #                 }
    #             )

    #         # Keep playing until the game is complete
    #         while not g.completed:
    #             next_guess = get_next_most_likely_word(
    #                 words=words_scores,
    #                 guesses=guesses,
    #                 count=1,
    #                 exclude_previous_guesses=False,
    #             )
    #             if len(next_guess) < 1:
    #                 print(f"NEED TO GUESS: {word}")
    #                 print("How the fuck did we get here")
    #             guesses.append(
    #                 {
    #                     'word': next_guess[0]['word'],
    #                     'outcome': g.guess(next_guess[0]['word']),
    #                 }
    #             )
    #             if word == 'tight':
    #                 print(g.guesses)
    #             #     import code; code.interact(local=dict(globals(), **locals()))

    #         f.write(f"{idx},{word},{g.score()},{'True' if fallback else 'False'}\n")


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
                if known_letter is not None:
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

            # TODO: Ensure that all of this position's wrong places can be allocated to other unsolved positions
            allocs = []
            for wrong_place_letter_idx, wrong_place_letter in enumerate(places_letters[letter_idx]['wrong_place']):
                # print(f"wrong_place_letter_idx: {wrong_place_letter_idx}")
                for other_letter_idx in range(len(word)):
                    if other_letter_idx != letter_idx: #and places_letters[other_letter_idx]['known'] is None:
                        if wrong_place_letter not in places_letters[other_letter_idx]['wrong_place']:
                            # print(f"appended: {wrong_place_letter_idx} to {other_letter_idx}")
                            allocs.append(wrong_place_letter_idx)

            # print(f"word: {word}")
            # print(f"letter: {letter}")
            # print(f"letter_idx: {letter_idx}")
            # print(f"places_letters: {places_letters}")
            # print(f"allocs: {allocs}")
            allocs = list(dict.fromkeys(allocs))
            if len(allocs) != len(places_letters[letter_idx]['wrong_place']):
                import code; code.interact(local=dict(globals(), **locals()))
                is_invalid = True

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
