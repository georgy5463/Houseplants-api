"""
Django command to wait for the database to be available
"""
import time
from psycopg2 import OperationalError as Psycopg2Error
from psycopg2 import connect
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for db"""

    def handle(self, *args, **options):
        """Entry point for commands"""
        self.stdout.write('Waiting for database...')
        db_up = False
        while not db_up:
            try:
                self.check(databases=['default'])
                # Attempt to create a connection to the database
                connection = connect(
                    dbname='devdb',
                    user='devuser',
                    password='changeme',
                    host='db',
                    port='5432'
                )
                connection.close()
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable. Waiting 1 sec...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available'))
