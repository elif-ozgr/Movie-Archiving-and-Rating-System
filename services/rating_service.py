from database import SessionLocal
from models.models import Rating, User, Movie
from datetime import date
from sqlalchemy.orm import Session # Tip ipucu için

class RatingService:
    """Film puanlama ve yorum ekleme servisi"""

    def __init__(self):
        # Session'ı sadece RatingService'e özel başlatıyoruz
        self.db = SessionLocal() 

    def add_rating(self, db: Session, user_name: str, movie_title: str, score: int, comment: str):
        # Kullanıcı var mı kontrol et, yoksa ekle (Otomatik kullanıcı yönetimi)
        user = db.query(User).filter_by(user_name=user_name).first()
        if not user:
            # Not: email alanı zorunlu olduğu için varsayılan bir değer atandı.
            user = User(user_name=user_name, email=f"{user_name}@example.com") 
            db.add(user)
            db.commit()
            db.refresh(user)

        # Film var mı kontrol et
        movie = db.query(Movie).filter_by(name=movie_title).first()
        if not movie:
            print(f"Film '{movie_title}' bulunamadı. Önce veritabanına ekleyin.")
            return None

        # Rating ekle
        new_rating = Rating(
            user_id=user.user_id,
            movie_id=movie.movie_id,
            score=score,
            comment=comment
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)

        print(f"✅ '{movie_title}' için {score}/10 puan ve yorum eklendi.")
        return new_rating

    def get_ratings_for_movie(self, movie_title: str):
        movie = self.db.query(Movie).filter_by(name=movie_title).first()
        if not movie:
            print(f"Film '{movie_title}' bulunamadı.")
            return []

        ratings = self.db.query(Rating).filter_by(movie_id=movie.movie_id).all()
        return ratings

    # YENİ METOT: Kullanıcıdan girdi almak için yardımcı fonksiyon
    def get_user_input(self, prompt, is_rating=False):
        """Kullanıcıdan girdi alır ve gerekirse puanı doğrular."""
        while True:
            user_input = input(prompt).strip()
            if is_rating:
                try:
                    rating = int(user_input)
                    if 1 <= rating <= 10:
                        return rating
                    else:
                        print("Puan 1 ile 10 arasında olmalıdır. Lütfen tekrar girin.")
                except ValueError:
                    print("Geçersiz giriş. Lütfen 1-10 arasında bir sayı girin.")
            else:
                return user_input

    # YENİ METOT: Kullanıcıdan puan ve yorum alıp kaydetmek için
    def prompt_and_add_rating(self, movie_title: str, user_name: str = "elif"):
        """Kullanıcıdan puan ve yorum alıp add_rating metodunu çağırır."""
        
        print(f"\n--- Film: '{movie_title}' için Puanlama ---")
        
        # Puanlama
        score = self.get_user_input("Puanınız (1-10): ", is_rating=True)
        
        # Yorumlama
        comment = self.get_user_input("Yorumunuz (Opsiyonel, boş bırakmak için Enter'a basın): ")
        
        # Mevcut add_rating metodunu kendi Session'ımızla çağırıyoruz
        self.add_rating(self.db, user_name, movie_title, score, comment)


    def close(self):
        self.db.close()