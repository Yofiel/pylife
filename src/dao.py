import sqlite3
from os.path import join


def save_winner(winner):
    name = winner.name

    with sqlite3.connect(join("data", "games.db")) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM player WHERE name = ?", (name,))
            search_result = cursor.fetchone()

            if not search_result:
                cursor.execute("INSERT INTO player VALUES (?, ?)", (name, 1))
            else:
                new_quantity = int(search_result[1]) + 1
                cursor.execute(
                    "UPDATE player SET win_quantity = ? WHERE name = ?",
                    (new_quantity, name),
                )
        except Exception as error:
            print(f"Error: {error}")

    connection.close()


def get_scores():
    search_result = []

    with sqlite3.connect(join("data", "games.db")) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM player ORDER BY win_quantity DESC")
            search_result = cursor.fetchmany(4)
        except Exception as error:
            print(f"Error: {error}")

    connection.close()

    return search_result
