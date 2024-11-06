import psycopg2
from config import load_config

import json


def insert_word(word):
    sql = """INSERT INTO words(word)
             VALUES(%s) RETURNING word_id;"""
    word_id = None
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (word,))
                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    word_id = rows[0]

                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return word_id


def insert_many_words(word_list):
    """ Insert multiple words into the words table  """

    sql = "INSERT INTO words(word) VALUES(%s) RETURNING *"
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.executemany(sql, word_list)

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def json_insert_words(words_dictionary):
    with open(words_dictionary, 'r') as f:
        data = json.load(f)
    config = load_config()
    conn = psycopg2.connect(**config)
    cursor = conn.cursor()
    print(conn, len(data))
    for word in data.keys():
        try:
            cursor.execute("INSERT INTO words (word) VALUES (%s) RETURNING word_id;",(word,))
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    conn.commit()
    cursor.close()
    conn.close()
#json_insert_words("words_dictionary.json")


if __name__ == '__main__':
    insert_word("aaaaahhhhghgg")
    #json_insert_words("/projects/english-words/words_dictionary.json")