import p2app.events
import p2app.engine.country
import p2app.engine.main
import sqlite3
from p2app.events.continents import Continent



def search_for_continent(connection: sqlite3.Connection, event):
    """Searches for continent in database and yields ContinentSearchResultEvent"""
    continent_code_user = event.continent_code()
    continent_name = event.name()
    cursor = None
    try:
        if continent_name is None and continent_code_user is not None:
            cursor = connection.execute(
                "SELECT * FROM continent WHERE continent_code = ?", (continent_code_user,))
        elif continent_name is not None and continent_code_user is None:
            cursor = connection.execute(
                "SELECT * FROM continent WHERE name = ?", (continent_name,))
        elif continent_name is not None and continent_code_user is not None:
            cursor = connection.execute(
                "SELECT * FROM continent WHERE continent_code = ? AND name = ?",
                (continent_code_user, continent_name))
        rows = cursor.fetchall()
        if len(rows) == 0:
            pass
        else:
            for row in rows:
                row = Continent(row[0], row[1], row[2])
                yield p2app.events.continents.ContinentSearchResultEvent(row)
    except Exception as e:
        yield p2app.events.app.ErrorEvent(str(e))

def save_edited_continent(connection: sqlite3.Connection, event):
    """Saves Edited Continent: Generator Function Yields - ContinentSavedEvent"""
    edited_continent = event.continent()
    continent_id = edited_continent.continent_id
    continent_name = edited_continent.name
    continent_code = edited_continent.continent_code
    cursor = connection.cursor()
    try:
        if not check_if_continent_code_already_used(connection, event):
            cursor.execute(
                "UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?",
                (continent_code, continent_name, continent_id))
            connection.commit()
            if check_if_continent_exists(connection, event, continent_id):
                yield p2app.events.continents.ContinentSavedEvent(edited_continent)
            else:
                yield p2app.events.continents.SaveContinentFailedEvent(
                    'Continent was not Saved')
        else:
            yield p2app.events.continents.SaveContinentFailedEvent(
                'Continent with Corresponding ID and/or Code Already Exists')
    except sqlite3.IntegrityError as e:
        yield p2app.events.continents.SaveContinentFailedEvent(str(e))


def check_if_continent_exists(connection: sqlite3.Connection, event, continent_id):
    """Checks if continent Exists"""
    edited_continent = event.continent()
    continent_name = edited_continent.name
    continent_code = edited_continent.continent_code
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM continent WHERE continent_code = ? AND continent_id = ? AND name = ?",
        (continent_code, continent_id, continent_name))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


def save_new_continent(connection: sqlite3.Connection, event):
    """Saves New continent: returns ContinentSavedEvent"""
    try:
        new_continent = event.continent()
        continent_id = get_unique_continent_id(connection, event)
        continent_name = new_continent.name
        continent_code = new_continent.continent_code
        continent_instance = Continent(continent_id, continent_code, continent_name)
        cursor = connection.cursor()
        if continent_id is None:
            pass
        if not check_if_continent_ID_already_exists(connection,
                                                           continent_id) and not check_if_new_continent_code_already_used(
                connection, event):
            cursor.execute(
                "INSERT INTO continent (continent_code, name, continent_id) VALUES (?, ?, ?)",
                (continent_code, continent_name, continent_id))
            connection.commit()
            if check_if_continent_exists(connection, event, continent_id):
                yield p2app.events.continents.ContinentSavedEvent(continent_instance)
            else:
                yield p2app.events.continents.SaveContinentFailedEvent('Continent was not Saved')
        else:
            yield p2app.events.continents.SaveContinentFailedEvent(
                'Continent with Corresponding ID and/or Code Already Exists')
    except sqlite3.IntegrityError as e:
        yield p2app.events.continents.SaveContinentFailedEvent(str(e))


def check_if_continent_ID_already_exists(connection: sqlite3.Connection, continent_id):
    """Checks if continent ID already exists"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM continent WHERE continent_id = ?", (continent_id,))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


def check_if_continent_code_already_used(connection: sqlite3.Connection, event):
    """Checks if continent code already used by other continent in database"""
    new_continent = event.continent()
    continent_code = new_continent.continent_code
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM continent WHERE continent_code = ?", (continent_code,))
    result = cursor.fetchone()
    if p2app.Engine.loaded_continent.continent_code != continent_code:
        if result is not None:
            return True
        else:
            return False
    else:
        return False


def check_if_new_continent_code_already_used(connection: sqlite3.Connection, event):
    """Checks if new continent code already used in database"""
    new_continent = event.continent()
    continent_code = new_continent.continent_code
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM continent WHERE continent_code = ?", (continent_code,))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


def get_unique_continent_id(connection: sqlite3.Connection, event):
    """Generates unique continent ID"""
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(continent_id) FROM continent")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id else 1
    return new_id