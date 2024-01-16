import p2app.events
import p2app.engine
import sqlite3
from p2app.engine import continent
from p2app.events.countries import Country


def search_for_country(connection: sqlite3.Connection, event):
    """Searchs database for country, generator that yields CountrySearchResultEvent"""
    country_code_user = event.country_code()
    country_name = event.name()
    cursor = None
    try:
        if country_name is None and country_code_user is not None:
            cursor = connection.execute(
                "SELECT * FROM country WHERE country_code = ?", (country_code_user,))
        elif country_name is not None and country_code_user is None:
            cursor = connection.execute(
                "SELECT * FROM country WHERE name = ?", (country_name,))
        elif country_name is not None and country_code_user is not None:
            cursor = connection.execute(
                "SELECT * FROM country WHERE country_code = ? AND name = ?",
                (country_code_user, country_name))
        rows = cursor.fetchall()
        if len(rows) == 0:
            pass
        else:
            for row in rows:
                row = Country(row[0], row[1], row[2], row[3], row[4], row[5])
                yield p2app.events.countries.CountrySearchResultEvent(row)
    except Exception as e:
        yield p2app.events.app.ErrorEvent(str(e))





def save_edited_country(connection: sqlite3.Connection, event):
    """Saves edited country: generator function that yields CountrySavedEvent"""
    edited_country = event.country()
    country_id = edited_country.country_id
    country_name = edited_country.name
    country_code = edited_country.country_code
    continent_id = edited_country.continent_id
    wiki_link = edited_country.wikipedia_link
    keywords = edited_country.keywords
    if wiki_link is None:
        wiki_link = ''
    if keywords == '':
        keywords = None
    country_instance = Country(country_id, country_code, country_name, continent_id, wiki_link,
                               keywords)
    cursor = connection.cursor()
    try:
        if p2app.engine.continent.check_if_continent_ID_already_exists(connection, continent_id):
            if not check_if_country_code_already_used(connection, event):
                cursor.execute(
                    "UPDATE country SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ? WHERE country_id = ?",
                    (country_code, country_name, continent_id, wiki_link, keywords, country_id))
                connection.commit()
                if check_if_country_exists(connection, event, country_id):
                    yield p2app.events.countries.CountrySavedEvent(country_instance)
                else:
                    yield p2app.events.countries.SaveCountryFailedEvent('Country was not Saved')
            else:
                yield p2app.events.countries.SaveCountryFailedEvent(
                    'Country with Corresponding ID and/or Code Already Exists')
        else:
            yield p2app.events.countries.SaveCountryFailedEvent(
                'Continent with Corresponding ID Does Not Exist')
    except sqlite3.IntegrityError as e:
        yield p2app.events.continents.SaveContinentFailedEvent(str(e))


def check_if_country_exists(connection: sqlite3.Connection, event, country_id):
    """checks if country already exists in database using ID"""
    edited_country = event.country()
    country_name = edited_country.name
    country_code = edited_country.country_code
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM country WHERE country_code = ? AND country_id = ? AND name = ?",
                   (country_code, country_id, country_name))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


def check_if_country_code_already_used(connection: sqlite3.Connection, event):
    """Checks if original country code already used"""
    new_country = event.country()
    country_code = new_country.country_code
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM country WHERE country_code = ?", (country_code,))
    result = cursor.fetchone()
    if p2app.Engine.loaded_country.country_code != country_code:
        if result is not None:
            return True
        else:
            return False
    else:
        return False


def check_if_new_country_code_already_used(connection: sqlite3.Connection, event):
    """Checks if new country code already in use"""
    new_country = event.country()
    country_code = new_country.country_code
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM country WHERE country_code = ?", (country_code,))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


def save_new_country(connection: sqlite3.Connection, event):
    """Saves new country: generator function that yields CountrySavedEvent"""
    new_country = event.country()
    country_id = get_unique_country_id(connection, event)
    country_name = new_country.name
    country_code = new_country.country_code
    continent_id = new_country.continent_id
    wiki_link = new_country.wikipedia_link
    keywords = new_country.keywords
    if wiki_link is None:
        wiki_link = ''
    if keywords == '':
        keywords = None
    country_instance = Country(country_id, country_code, country_name, continent_id, wiki_link,
                               keywords)
    cursor = connection.cursor()
    try:
        if p2app.engine.continent.check_if_continent_ID_already_exists(connection, continent_id):
            if not check_if_new_country_code_already_used(connection, event):
                cursor.execute(
                    "INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?)",
                    (country_id, country_code, country_name, continent_id, wiki_link, keywords))
                connection.commit()
                if check_if_country_exists(connection, event, country_id):
                    yield p2app.events.countries.CountrySavedEvent(country_instance)
                else:
                    yield p2app.events.countries.SaveCountryFailedEvent('Country was not Saved')
            else:
                yield p2app.events.countries.SaveCountryFailedEvent(
                    'Country with Corresponding ID and/or Code Already Exists')
        else:
            yield p2app.events.countries.SaveCountryFailedEvent(
                'Continent with Corresponding ID Does Not Exist')
    except sqlite3.IntegrityError as e:
        yield p2app.events.continents.SaveContinentFailedEvent(str(e))


def get_unique_country_id(connection: sqlite3.Connection, event):
    """Generates unique country ID"""
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(country_id) FROM country")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id else 1
    return new_id


def check_if_country_ID_already_exists(connection: sqlite3.Connection, country_id):
    """Checks if country ID already exists in database"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM country WHERE country_id = ?", (country_id,))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False