from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine import connection
import pathlib
from . import config

BASE_DIR = pathlib.Path(__name__).resolve().parent

ASTRADB_CONNECT_BUNDLE = BASE_DIR/'app'/'connect_db'/'astra_db.zip'

ASTRADB_CLIENT_ID = config.get_settings().db_client_id
ASTRADB_CLIENT_SECRET = config.get_settings().db_client_secret

def get_session():


    cloud_config = {
        'secure_connect_bundle': ASTRADB_CONNECT_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    # print(ASTRADB_CONNECT_BUNDLE)
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))
    # print(ASTRADB_CONNECT_BUNDLE)
    return session