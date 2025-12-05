from database import SessionLocal
from models.models import Rating, User, Movie
from datetime import date
from sqlalchemy.orm import Session  # For type hints

class RatingService:
    """Service for adding movie ratings and comments"""

    def __init__(self):
        # Initialize a session dedicated to RatingService
        self.db = SessionLocal() 

    def add_rating(self, db: Session, user_name: str, movie_title: str, score: int, comment: str):
        # Check if user exists, add if not (Automatic user management)
        user = db.query(User).filter_by(user_name=user_name).first()
        if not user:
            # Note: email is required, so a default value is assigned.
            user = User(user_name=user_name, email=f"{user_name}@example.com") 
            db.add(user)
            db.commit()
            db.refresh(user)

        # Check if movie exists
        movie = db.query(Movie).filter_by(name=movie_title).first()
        if not movie:
            print(f"Movie '{movie_title}' not found. Please add it to the database first.")
            return None

        # Add rating
        new_rating = Rating(
            user_id=user.user_id,
            movie_id=movie.movie_id,
            score=score,
            comment=comment
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)

        print(f"✅ Added rating {score}/10 and comment for '{movie_title}'.")
        return new_rating

    def get_ratings_for_movie(self, movie_title: str):
        movie = self.db.query(Movie).filter_by(name=movie_title).first()
        if not movie:
            print(f"Movie '{movie_title}' not found.")
            return []

        ratings = self.db.query(Rating).filter_by(movie_id=movie.movie_id).all()
        return ratings

    # NEW METHOD: Helper function to get user input
    def get_user_input(self, prompt, is_rating=False):
        """Gets user input and validates rating if necessary."""
        while True:
            user_input = input(prompt).strip()
            if is_rating:
                try:
                    rating = int(user_input)
                    if 1 <= rating <= 10:
                        return rating
                    else:
                        print("Rating must be between 1 and 10. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 10.")
            else:
                return user_input

    # NEW METHOD: Prompt user for rating and comment, then save
    def prompt_and_add_rating(self, movie_title: str, user_name: str = "elif"):
        """Prompts the user for rating and comment, then calls add_rating."""
        
        print(f"\n--- Rating for Movie: '{movie_title}' ---")
        
        # Get rating
        score = self.get_user_input("Your rating (1-10): ", is_rating=True)
        
        # Get comment
        comment = self.get_user_input("Your comment (Optional, press Enter to skip): ")
        
        # Call add_rating using the service's session
        self.add_rating(self.db, user_name, movie_title, score, comment)

    def close(self):
        self.db.close()
