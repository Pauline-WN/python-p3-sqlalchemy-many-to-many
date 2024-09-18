import pytest
from models import Game, User, Review

class TestGame:

    def test_has_attributes(self, db_session):
        '''has attributes id, title, genre, platform, price, reviews, and users.'''
        
        game = Game(title="Corbin Air Drive")
        db_session.add(game)
        db_session.commit()

        assert hasattr(game, "id")
        assert hasattr(game, "title")
        assert hasattr(game, "genre")
        assert hasattr(game, "platform")
        assert hasattr(game, "price")
        assert hasattr(game, "reviews")
        assert hasattr(game, "users")

    def test_has_many_reviews(self, db_session):
        '''has an attribute "reviews" that is a sequence of Review records.'''

        review_1 = Review(score=8, comment="Good game!")
        review_2 = Review(score=6, comment="OK game.")
        db_session.add_all([review_1, review_2])
        db_session.commit()

        game = Game(title="Metric Prime Reverb")
        game.reviews.append(review_1)
        game.reviews.append(review_2)
        db_session.add(game)
        db_session.commit()

        assert game.reviews
        assert review_1 in game.reviews
        assert review_2 in game.reviews

    def test_has_many_users(self, db_session):
        '''has an attribute "users" that is a sequence of User records.'''

        user_1 = User(name="Ben")
        user_2 = User(name="Prabhdip")
        db_session.add_all([user_1, user_2])
        db_session.commit()
        
        game = Game(title="Super Marvin 128")
        game.users.append(user_1)
        game.users.append(user_2)
        db_session.add(game)
        db_session.commit()

        assert game.users
        assert user_1 in game.users
        assert user_2 in game.users
