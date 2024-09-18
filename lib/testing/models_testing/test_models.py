import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Game, User, Review
from conftest import SQLITE_URL

@pytest.fixture(scope='module')
def setup_database():
    engine = create_engine(SQLITE_URL)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create Users
    user1 = User(name="Alice")
    user2 = User(name="Bob")
    session.add_all([user1, user2])
    session.commit()

    # Create Games
    game1 = Game(title="Game 1", genre="Action", platform="PC", price=50)
    game2 = Game(title="Game 2", genre="Adventure", platform="PS5", price=60)
    session.add_all([game1, game2])
    session.commit()

    # Create Reviews
    review1 = Review(score=9, comment="Great game!", game_id=game1.id, user_id=user1.id)
    review2 = Review(score=8, comment="Very fun!", game_id=game2.id, user_id=user2.id)
    session.add_all([review1, review2])
    session.commit()

    # Add Many-to-Many Relationships
    game1.users.append(user1)
    game2.users.append(user2)
    session.commit()

    yield {
        'session': session,
        'game1': game1,
        'game2': game2,
        'user1': user1,
        'user2': user2
    }

    session.close()
    engine.dispose()

def test_game_users(setup_database):
    game1 = setup_database['game1']
    game2 = setup_database['game2']
    user1 = setup_database['user1']
    user2 = setup_database['user2']

    assert user1 in game1.users
    assert user2 in game2.users

def test_user_games(setup_database):
    user1 = setup_database['user1']
    user2 = setup_database['user2']
    game1 = setup_database['game1']
    game2 = setup_database['game2']

    assert game1 in user1.games
    assert game2 in user2.games
