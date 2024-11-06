import itertools
import psycopg2
from config import load_config  

letters = "leajnby"

def find_valid_words(letters):
    letters = letters.lower()
    alphabet = parse_alpha(letters)
    first_letter = letters[0]

    config = load_config() 
    conn = psycopg2.connect(**config)
    cur = conn.cursor()

    cur.execute("SELECT word FROM words WHERE word LIKE %s AND LENGTH(word) >= 4" , (f"%{first_letter}%",))
    #cur.execute("SELECT word FROM words WHERE word LIKE %s AND LENGTH(word) >= 4" , (f"%diatomic%",))
    words_letter = [row[0] for row in cur.fetchall()]
    #print(words_letter)
    i=0
    while i < (len(words_letter)):
        if any(char in words_letter[i] for char in alphabet):
            words_letter.pop(i)
        else: i += 1 

    cur.close()
    conn.close()
    print(words_letter)
    return words_letter






def parse_alpha(letters):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    i=0
    while i < (len(letters)):
        alphabet = alphabet.replace(letters[i],"")
        #print(alphabet)
        i += 1
    return alphabet

find_valid_words(letters)



