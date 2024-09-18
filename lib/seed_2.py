#!/usr/bin/env python3

from faker import Faker
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Game, Review, User, game_user  # Import the association table

if __name__ == '__main__':
    engine = create_engine('sqlite:///many_to_many.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data
    session.query(Game).delete()
    session.query(Review).delete()
    session.query(User).delete()

    fake = Faker()

    # Define genres and platforms
    genres = ['action', 'adventure', 'strategy',
        'puzzle', 'first-person shooter', 'racing']
    platforms = ['nintendo 64', 'gamecube', 'wii', 'wii u', 'switch',
        'playstation', 'playstation 2', 'playstation 3', 'playstation 4',
        'playstation 5', 'xbox', 'xbox 360', 'xbox one', 'pc']

    # Create games
    games = []
    for i in range(50):
        game = Game(
            title=fake.unique.name(),
            genre=random.choice(genres),
            platform=random.choice(platforms),
            price=random.randint(5, 60)
        )

        session.add(game)
        session.commit()

        games.append(game)

    # Create users
    users = []
    for i in range(25):
        user = User(
            name=fake.name(),
        )

        session.add(user)
        session.commit()

        users.append(user)

    # Create reviews and establish many-to-many relationships
    for game in games:
        for i in range(random.randint(1,5)):
            user = random.choice(users)

            review = Review(
                score=random.randint(0, 10),
                comment=fake.sentence(),
                game_id=game.id,
                user_id=user.id,
            )

            session.add(review)

            # Establish the many-to-many relationship
            if game not in user.games:
                user.games.append(game)

            # Add and commit review
            session.commit()

    session.close()
