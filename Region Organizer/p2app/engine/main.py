import p2app.events
import p2app.engine.country
import p2app.engine.continent
import p2app.engine.region
import sqlite3
from pathlib import Path
from p2app.events.continents import Continent
from p2app.events.countries import Country
from p2app.events.regions import Region

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """
    loaded_continent = None
    loaded_country = None
    loaded_region = None
    # class variables to hold information about loaded item to reference when editing item

    def __init__(self):
        """Initializes the engine"""
        self.connection = None

    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if isinstance(event, p2app.events.app.QuitInitiatedEvent):
            yield from Engine.end_application(self, event)
        if isinstance(event, p2app.events.database.OpenDatabaseEvent): #opendatabase event
            yield from Engine.connect_to_DB(self, event)
        if isinstance(event, p2app.events.database.CloseDatabaseEvent):
            yield from Engine.close_DB(self, event)
        if isinstance(event, p2app.events.continents.StartContinentSearchEvent):
            yield from p2app.engine.continent.search_for_continent(self.connection, event)
        if isinstance(event, p2app.events.countries.StartCountrySearchEvent):
            yield from p2app.engine.country.search_for_country(self.connection, event)
        if isinstance(event, p2app.events.regions.StartRegionSearchEvent):
            yield from p2app.engine.region.search_for_region(self.connection, event)
        if isinstance(event, p2app.events.continents.LoadContinentEvent):
            yield from Engine.load_continent_from_id(self, event)
        if isinstance(event, p2app.events.continents.SaveContinentEvent):
            yield from p2app.engine.continent.save_edited_continent(self.connection, event)
        if isinstance(event, p2app.events.continents.SaveNewContinentEvent):
            yield from p2app.engine.continent.save_new_continent(self.connection, event)
        if isinstance(event, p2app.events.countries.LoadCountryEvent):
            yield from Engine.load_country_from_id(self, event)
        if isinstance(event, p2app.events.countries.SaveCountryEvent):
            yield from p2app.engine.country.save_edited_country(self.connection, event)
        if isinstance(event, p2app.events.countries.SaveNewCountryEvent):
            yield from p2app.engine.country.save_new_country(self.connection, event)
        if isinstance(event, p2app.events.regions.LoadRegionEvent):
            yield from Engine.load_region_from_id(self, event)
        if isinstance(event, p2app.events.regions.SaveRegionEvent):
            yield from p2app.engine.region.save_edited_region(self.connection, event)
        if isinstance(event, p2app.events.regions.SaveNewRegionEvent):
            yield from p2app.engine.region.save_new_region(self.connection, event)


    def end_application(self, event):
        try:
            yield p2app.events.app.EndApplicationEvent()
        except Exception as e:
            yield p2app.events.app.ErrorEvent(str(e))

    def close_DB(self, event):
        try:
            yield p2app.events.database.DatabaseClosedEvent()
        except Exception as e:
            yield p2app.events.app.ErrorEvent(str(e))

    def connect_to_DB(self, event):
        """Connects program to database"""
        try:
            path = event.path()
            self.connection = sqlite3.connect(path)
            self.connection.execute("PRAGMA foreign_keys = ON;")
            cursor = self.connection.execute('SELECT name FROM sqlite_schema;')
            table_names_list = cursor.fetchall()
            if ('country',) in table_names_list and ('region',) in table_names_list and (
                    'continent',) in table_names_list:
                yield p2app.events.database.DatabaseOpenedEvent(Path(path))
            else:
                yield p2app.events.database.DatabaseOpenFailedEvent("Incorrect Database Contents\n")
        except sqlite3.Error:
            yield p2app.events.database.DatabaseOpenFailedEvent("Not a database file\n")

    def load_country_from_id(self, event):
        """Creates country namedtuple given a country ID"""
        try:
            country_id = event.country_id()
            cursor = None
            if country_id is not None:
                cursor = self.connection.execute("SELECT * FROM country WHERE country_id = ?",
                                                 (country_id,))
            rows = cursor.fetchall()
            if len(rows) == 0:
                pass
            else:
                for row in rows:
                    row = Country(row[0], row[1], row[2], row[3], row[4], row[5])
                    Engine.loaded_country = row
                    yield p2app.events.countries.CountryLoadedEvent(row)
        except Exception as e:
            yield p2app.events.app.ErrorEvent(str(e))

    def load_continent_from_id(self, event):
        """Loads continent given an ID"""
        try:
            continent_id = event.continent_id()
            cursor = None
            if continent_id is not None:
                cursor = self.connection.execute("SELECT * FROM continent WHERE continent_id = ?", (continent_id,))
            rows = cursor.fetchall()
            if len(rows) == 0:
                pass
            else:
                for row in rows:
                    row = Continent(row[0], row[1], row[2])
                    Engine.loaded_continent = row
                    yield p2app.events.continents.ContinentLoadedEvent(row)
        except Exception as e:
            yield p2app.events.app.ErrorEvent(str(e))


    def load_region_from_id(self, event):
        """Loads region given a region ID"""
        try:
            region_id = event.region_id()
            cursor = None
            if region_id is not None:
                cursor = self.connection.execute("SELECT * FROM region WHERE region_id = ?",(region_id,))
            rows = cursor.fetchall()
            if len(rows) == 0:
                pass
            else:
                for row in rows:
                    row = Region(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    Engine.loaded_region = row
                    yield p2app.events.regions.RegionLoadedEvent(row)
        except Exception as e:
            yield p2app.events.app.ErrorEvent(str(e))
