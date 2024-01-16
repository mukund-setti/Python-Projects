import p2app.events
import p2app.engine
import sqlite3
from p2app.engine import continent
from p2app.engine import country
from p2app.events.regions import Region


def search_for_region(connection: sqlite3.Connection, event):
    """Searches for region in database: returns RegionSearchResultEvent"""
    region_code = event.region_code()
    region_name = event.name()
    region_local_code = event.local_code()
    cursor = None
    try:
        if region_code is not None and region_name is not None and region_local_code is not None:
            cursor = connection.execute(
                "SELECT * FROM region WHERE region_code = ? AND name = ? AND local_code = ?",
                (region_code, region_name, region_local_code))
        elif region_code is not None and region_name is not None and region_local_code is None:
            cursor = connection.execute("SELECT * FROM region WHERE region_code = ? AND name = ?",
                                             (region_code, region_name))
        elif region_code is not None and region_name is None and region_local_code is not None:
            cursor = connection.execute(
                "SELECT * FROM region WHERE region_code = ? AND local_code = ?",
                (region_code, region_local_code))
        elif region_code is not None and region_name is None and region_local_code is None:
            cursor = connection.execute("SELECT * FROM region WHERE region_code = ?",
                                             (region_code,))
        elif region_code is None and region_name is not None and region_local_code is not None:
            cursor = connection.execute("SELECT * FROM region WHERE name = ? AND local_code = ?",
                                             (region_name, region_local_code))
        elif region_code is None and region_name is not None and region_local_code is None:
            cursor = connection.execute("SELECT * FROM region WHERE name = ?", (region_name,))
        elif region_code is None and region_name is None and region_local_code is not None:
            cursor = connection.execute("SELECT * FROM region WHERE local_code = ?",
                                             (region_local_code,))
        rows = cursor.fetchall()

        if len(rows) == 0:
            pass
        else:
            for row in rows:
                row = Region(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                yield p2app.events.regions.RegionSearchResultEvent(row)
    except Exception as e:
        yield p2app.events.app.ErrorEvent(str(e))
def save_edited_region(connection: sqlite3.Connection, event):
    """Saves edited regions and returns RegionSavedEvent"""
    edited_region = event.region()
    region_id = edited_region.region_id
    region_name = edited_region.name
    region_code = edited_region.region_code
    region_local_code = edited_region.local_code
    country_id = edited_region.country_id
    continent_id = edited_region.continent_id
    wiki_link = edited_region.wikipedia_link
    keywords = edited_region.keywords
    if wiki_link == '':
        wiki_link = None
    if keywords == '':
        keywords = None
    region_instance = Region(region_id, region_code, region_local_code, region_name, continent_id,
                             country_id, wiki_link, keywords)
    cursor = connection.cursor()
    try:
        if p2app.engine.continent.check_if_continent_ID_already_exists(connection, continent_id):
            if p2app.engine.country.check_if_country_ID_already_exists(connection, country_id):
                if not check_if_region_code_already_used(connection, event):
                    cursor.execute(
                        "UPDATE region SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id = ?",
                        (region_code, region_local_code, region_name, continent_id, country_id,
                         wiki_link, keywords, region_id))
                    connection.commit()
                    if check_if_region_exists(connection, event, region_id):
                        yield p2app.events.regions.RegionSavedEvent(region_instance)
                    else:
                        yield p2app.events.regions.SaveRegionFailedEvent('Region was not Saved')
                else:
                    yield p2app.events.regions.SaveRegionFailedEvent(
                        'Region with Corresponding ID and/or Code Already Exists')
            else:
                yield p2app.events.regions.SaveRegionFailedEvent(
                    'Country with Corresponding ID Does not Exist')
        else:
            yield p2app.events.regions.SaveRegionFailedEvent(
                'Continent with Corresponding ID Does Not Exist')
    except sqlite3.IntegrityError as e:
        yield p2app.events.continents.SaveContinentFailedEvent(str(e))


def check_if_region_exists(connection: sqlite3.Connection, event, region_id):
    """Checks if region exists in database"""
    edited_region = event.region()
    region_name = edited_region.name
    region_code = edited_region.region_code
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM region WHERE region_code = ? AND region_id = ? AND name = ?",
                   (region_code, region_id, region_name))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


def check_if_region_code_already_used(connection: sqlite3.Connection, event):
    """Checks if region code already used"""
    new_region = event.region()
    region_code = new_region.region_code
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM region WHERE region_code = ?", (region_code,))
    result = cursor.fetchone()
    if p2app.Engine.loaded_region.region_code != region_code:
        if result is not None:
            return True
        else:
            return False
    else:
        return False


def check_if_new_region_code_already_used(connection: sqlite3.Connection, event):
    """Checks if new region code already used"""
    new_region = event.region()
    region_code = new_region.region_code
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM region WHERE region_code = ?", (region_code,))
    result = cursor.fetchone()
    if result is not None:
        return True
    else:
        return False


def save_new_region(connection: sqlite3.Connection, event):
    """Saves new region to database: """
    new_region = event.region()
    region_id = get_unique_region_id(connection, event)
    region_name = new_region.name
    region_code = new_region.region_code
    local_code = new_region.local_code
    continent_id = new_region.continent_id
    country_id = new_region.country_id
    wiki_link = new_region.wikipedia_link
    keywords = new_region.keywords
    if wiki_link == '':
        wiki_link = None
    if keywords == '':
        keywords = None
    region_instance = Region(region_id, region_code, local_code, region_name, continent_id,
                             country_id, wiki_link, keywords)
    cursor = connection.cursor()
    try:
        if region_id is None:
            pass
        if p2app.engine.continent.check_if_continent_ID_already_exists(connection, continent_id):
            if p2app.engine.country.check_if_country_ID_already_exists(connection, country_id):
                if not check_if_new_region_code_already_used(connection, event):
                    cursor.execute(
                        "INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (region_id, region_code, local_code, region_name, continent_id, country_id,
                         wiki_link, keywords))
                    connection.commit()
                    if check_if_region_exists(connection, event, region_id):
                        yield p2app.events.regions.RegionSavedEvent(region_instance)
                    else:
                        yield p2app.events.regions.SaveRegionFailedEvent('Region was not Saved')
                else:
                    yield p2app.events.regions.SaveRegionFailedEvent(
                        'Region with Corresponding ID and/or Code Already Exists')
            else:
                yield p2app.events.regions.SaveRegionFailedEvent(
                    'Country with Corresponding ID Does Not Exist')
        else:
            yield p2app.events.regions.SaveRegionFailedEvent(
                'Continent with Corresponding ID Does Not Exist')
    except sqlite3.IntegrityError as e:
        yield p2app.events.continents.SaveContinentFailedEvent(str(e))


def get_unique_region_id(connection: sqlite3.Connection, event):
    """Generates unique region ID"""
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("SELECT MAX(region_id) FROM region")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id else 1
    return new_id
