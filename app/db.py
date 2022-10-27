# connecting the cassandra database
import os
import pathlib

from dotenv import load_dotenv

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection


load_dotenv(dotenv_path=pathlib.Path(__file__).parent / '.env')


ASTRA_DB_CLIENTS_ID = os.getenv('ASTRA_DB_CLIENTS_ID')
ASTRA_DB_CLIENTS_SECRET = os.getenv('ASTRA_DB_CLIENTS_SECRET')


BASE_DIR = pathlib.Path(__file__).parent
CLUSTER_BUNDLE = str(BASE_DIR/"db_connector"/'connect-new-db.zip')


def get_cluster():
    cloud_config= {
         'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRA_DB_CLIENTS_ID, ASTRA_DB_CLIENTS_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster
    
      
def get_session():
    cluster = get_cluster()    
    session = cluster.connect("event_app")
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session


# users table
session = get_session()
def create_tables():
    session.execute("""
                    CREATE TABLE IF NOT EXISTS event_app.users (
                        user_id text,
                        email text,
                        username text,
                        fullname text,
                        phone_number text,
                        password text,
                        business_name text,
                        sector text,
                        PRIMARY KEY (user_id, email, username));
                    """)

create_tables()
row = session.execute("select release_version from system.local").one()
if row:
      print(row)
else:
      print("An error occurred.")

    

# event table
session = get_session()
def create_tables():
    session.execute("""
                    CREATE TABLE IF NOT EXISTS event_app.events (
                        event_id text,
                        user_id text ,
                        event_name text,
                        event_organizer text,
                        event_type text,
                        event_category text,
                        event_tags text,
                        event_location text,
                        event_datetime timestamp,
                        PRIMARY KEY (event_id, user_id, event_name));
                       
                    """)
create_tables()
row = session.execute("select release_version from system.local").one()
if row:
      print(row)
else:
      print("An error occurred.")

    

