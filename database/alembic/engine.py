from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from alembic.autogenerate import compare_metadata

from alembic.migration import MigrationContext
from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from sqlalchemy.schema import SchemaItem
from sqlalchemy.types import TypeEngine
from sqlalchemy import (create_engine, MetaData, Column,
        Integer, String, Table)
import pprint

import os, sys
# CONNECT
instring = 'mysql+pymysql://root:Th3T3chBoy$@localhost/sofiat'


#Base = automap_base()
#Base.prepare(engine, reflect=True)

#Base.classes.keys()

class Engine(object):
    def __init__(self):
        self.keychain = {'mysql' : os.environ.get('mysql_key')}

        try:
            url = 'mysql+pymysql://root:{}@localhost/sofiat'.format(self.keychain.get('mysql'))
            self.engine = create_engine(url)

        except:
            print('Error connecting to database')


        self.base = automap_base()
        self.base.prepare(self.engine, reflect=True)

        self.models = api.DataBaseAPI.engine.base.keys()

        return

    def 
