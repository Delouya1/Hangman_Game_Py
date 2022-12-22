import requests as requests


def check_win(secret_word, old_letters_guessed):
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True


def show_hidden_word(secret_word, old_letters_guessed):
    hidden_word = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            hidden_word += letter
        else:
            hidden_word += "_"
    return hidden_word


def check_valid_input(letter_guessed, old_letters_guessed):
    if len(letter_guessed) != 1:
        return False
    if not letter_guessed.isalpha():
        return False
    if letter_guessed in old_letters_guessed:
        return False
    return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    return False


def choose_word(file_path, index):
    with open(file_path, 'r') as f:
        words = f.readlines()
        return words[index].strip()


def create_file():
    url = 'https://random-word-api.herokuapp.com/word?number=1000'
    response = requests.get(url)
    words = response.json()
    with open("words.txt", "w") as f:
        for word in words:
            f.write(word + "\n")


def print_hangman(tries):
    hangman_photos = {
        1: """x-------x""", 2: """
x-------x
|
|
|
|
|""", 3: """
x-------x
|       |
|       0
|
|
|""", 4: """
x-------x
|       |
|       0
|       |
|
|""", 5: """
x-------x
|       |
|       0
|      /|\\
|
|""", 6: """
x-------x
|       |
|       0
|      /|\\
|      /
|""", 7: """
x-------x
|       |
|       0
|      /|\\
|      / \\
|"""}
    print(hangman_photos[tries])


HANGMAN_ASCII_ART = """
    _    _
    | |  | |
    | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
    |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \\
    | |  | | (_| | | | | (_| | | | | | | (_| | | | |
    |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                            __/ |
                            |___/"""


def play_hangman():
    max_tries = 6
    print(HANGMAN_ASCII_ART)
    print("Welcome to Hangman Game!")
    print("I chose a word for you, try to guess it!")
    secret_word = choose_word("words.txt", 0)
    # explain your code
    old_letters_guessed = []
    tries = 1
    while tries <= max_tries:
        print("Tries left: " + str(max_tries - tries + 1))
        print(show_hidden_word(secret_word, old_letters_guessed))
        letter_guessed = input("Guess a letter: ")
        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            if letter_guessed in secret_word:
                print("Good job :)")
            else:
                print(":((")
                tries += 1
                print_hangman(tries)
        else:
            print("X")
            print(" -> ".join(sorted(old_letters_guessed)))
        if check_win(secret_word, old_letters_guessed):
            print("WIN")
            break
    if tries > max_tries:
        print("LOSE")
        print("The word was: " + secret_word)


create_file()
play_hangman()
