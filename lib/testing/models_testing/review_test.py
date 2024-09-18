import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models import Base, Game, User, Review
from conftest import SQLITE_URL

@pytest.fixture(scope='module')
def db_session():
    """Fixture to provide a database session."""
    engine = create_engine(SQLITE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_review_has_attributes(db_session):
    """Test attributes of the Review model."""
    review = Review(score=2, comment="Very bad!")
    db_session.add(review)
    db_session.commit()
    
    # Fetch the review from the database to assert its attributes
    fetched_review = db_session.query(Review).filter_by(id=review.id).one()
    
    assert fetched_review.id == review.id
    assert fetched_review.score == review.score
    assert fetched_review.comment == review.comment
    assert fetched_review.created_at is not None
    assert fetched_review.updated_at is not None

def test_review_relationships(db_session):
    """Test relationships of the Review model with Game and User."""
    # Create and add instances of Game and User
    game = Game(title="Game Title", genre="Genre", platform="Platform", price=50)
    user = User(name="User Name")
    
    db_session.add(game)
    db_session.add(user)
    db_session.commit()
    
    # Create a review related to the game and user
    review = Review(score=4, comment="Great game!", game_id=game.id, user_id=user.id)
    db_session.add(review)
    db_session.commit()
    
    # Fetch the review and check relationships
    fetched_review = db_session.query(Review).filter_by(id=review.id).one()
    
    assert fetched_review.game_id == game.id
    assert fetched_review.user_id == user.id
    assert fetched_review.game == game
    assert fetched_review.user == user
