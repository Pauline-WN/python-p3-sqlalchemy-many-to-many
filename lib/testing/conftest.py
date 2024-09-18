#!/usr/bin/env python3

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Ensure this imports your Base from models

# Define the SQLite URL for the test database
package_dir = '/'.join(os.path.abspath(os.path.dirname(__file__)).split('/')[0:-1])
db_dir = os.path.join(package_dir, 'many_to_many.db')
SQLITE_URL = ''.join(['sqlite:///', db_dir])

@pytest.fixture(scope='function')
def db_engine():
    """Fixture to provide a database engine for testing."""
    engine = create_engine(SQLITE_URL)
    Base.metadata.create_all(engine)  # Create all tables
    yield engine
    Base.metadata.drop_all(engine)    # Drop all tables after test

@pytest.fixture(scope='function')
def db_session(db_engine):
    """Fixture to provide a database session for testing."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.close()

def pytest_itemcollected(item):
    """Customize test item names for better readability."""
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
