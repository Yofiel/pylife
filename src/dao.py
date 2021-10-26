import sqlite3
from os.path import join


def save_winner(winner):
    name = winner.name.upper()

    with sqlite3.connect(join("data", "games.db")) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM player WHERE name = ?", (name,))
            search_result = cursor.fetchone()

            if len(search_result) == 0:
                cursor.execute("INSERT INTO player VALUES (?, ?)", (name, 1))
            else:
                new_quantity = search_result[0][1] + 1
                cursor.execute(
                    "UPDATE player SET win_quantity = ? WHERE name = ?",
                    (name, new_quantity),
                )
        except Exception as error:
            print(error)

    connection.close()


def get_scores():
    search_result = []

    with sqlite3.connect(join("data", "games.db")) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM player")
            search_result = cursor.fetchall()

            print(search_result)
        except Exception as error:
            print(error)

    connection.close()

    return search_result
