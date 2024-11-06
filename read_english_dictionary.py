def load_words():
    i = 1
    while i < 20:
        with open('words_alpha.txt') as word_file:
            valid_words = set(word_file.read().split())
        i +=1

    return valid_words


if __name__ == '__main__':
    english_words = load_words()
    # demo print
    print('fate' in english_words)
    print(type(english_words))


