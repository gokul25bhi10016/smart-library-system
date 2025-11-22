"""
Smart Library Management System
Simple book recommendation engine using content-based filtering
"""

import pandas as pd
import random


class SmartLibrary:
    """Simple library system with book recommendations"""

    def __init__(self):
        """Initialize library with sample book data"""
        self.books = self._create_sample_books()
        self.genres = ['Fiction', 'Science', 'History', 'Technology', 'Biography',
                      'Fantasy', 'Mystery', 'Romance', 'Self-Help', 'Business']

    def _create_sample_books(self):
        """Create sample book dataset"""
        books_data = [
            # Fiction
            {'id': 1, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee', 'genre': 'Fiction',
             'pages': 324, 'rating': 4.8, 'available': True, 'year': 1960},
            {'id': 2, 'title': '1984', 'author': 'George Orwell', 'genre': 'Fiction',
             'pages': 328, 'rating': 4.7, 'available': True, 'year': 1949},
            {'id': 3, 'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'genre': 'Fiction',
             'pages': 432, 'rating': 4.6, 'available': False, 'year': 1813},

            # Science
            {'id': 4, 'title': 'A Brief History of Time', 'author': 'Stephen Hawking', 'genre': 'Science',
             'pages': 256, 'rating': 4.5, 'available': True, 'year': 1988},
            {'id': 5, 'title': 'Cosmos', 'author': 'Carl Sagan', 'genre': 'Science',
             'pages': 384, 'rating': 4.7, 'available': True, 'year': 1980},
            {'id': 6, 'title': 'The Selfish Gene', 'author': 'Richard Dawkins', 'genre': 'Science',
             'pages': 360, 'rating': 4.4, 'available': True, 'year': 1976},

            # Technology
            {'id': 7, 'title': 'Clean Code', 'author': 'Robert Martin', 'genre': 'Technology',
             'pages': 464, 'rating': 4.6, 'available': True, 'year': 2008},
            {'id': 8, 'title': 'The Pragmatic Programmer', 'author': 'David Thomas', 'genre': 'Technology',
             'pages': 352, 'rating': 4.5, 'available': False, 'year': 1999},
            {'id': 9, 'title': 'Code Complete', 'author': 'Steve McConnell', 'genre': 'Technology',
             'pages': 960, 'rating': 4.4, 'available': True, 'year': 2004},

            # History
            {'id': 10, 'title': 'Sapiens', 'author': 'Yuval Noah Harari', 'genre': 'History',
             'pages': 443, 'rating': 4.8, 'available': True, 'year': 2011},
            {'id': 11, 'title': 'Guns, Germs, and Steel', 'author': 'Jared Diamond', 'genre': 'History',
             'pages': 528, 'rating': 4.3, 'available': True, 'year': 1997},

            # Biography
            {'id': 12, 'title': 'Steve Jobs', 'author': 'Walter Isaacson', 'genre': 'Biography',
             'pages': 656, 'rating': 4.5, 'available': True, 'year': 2011},
            {'id': 13, 'title': 'Becoming', 'author': 'Michelle Obama', 'genre': 'Biography',
             'pages': 448, 'rating': 4.7, 'available': False, 'year': 2018},

            # Fantasy
            {'id': 14, 'title': 'The Hobbit', 'author': 'J.R.R. Tolkien', 'genre': 'Fantasy',
             'pages': 310, 'rating': 4.7, 'available': True, 'year': 1937},
            {'id': 15, 'title': 'Harry Potter and the Sorcerer\'s Stone', 'author': 'J.K. Rowling',
             'genre': 'Fantasy', 'pages': 309, 'rating': 4.8, 'available': True, 'year': 1997},

            # Mystery
            {'id': 16, 'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'genre': 'Mystery',
             'pages': 489, 'rating': 4.2, 'available': True, 'year': 2003},
            {'id': 17, 'title': 'Gone Girl', 'author': 'Gillian Flynn', 'genre': 'Mystery',
             'pages': 422, 'rating': 4.3, 'available': True, 'year': 2012},

            # Self-Help
            {'id': 18, 'title': 'Atomic Habits', 'author': 'James Clear', 'genre': 'Self-Help',
             'pages': 320, 'rating': 4.8, 'available': True, 'year': 2018},
            {'id': 19, 'title': 'The 7 Habits of Highly Effective People', 'author': 'Stephen Covey',
             'genre': 'Self-Help', 'pages': 381, 'rating': 4.5, 'available': True, 'year': 1989},

            # Business
            {'id': 20, 'title': 'Good to Great', 'author': 'Jim Collins', 'genre': 'Business',
             'pages': 300, 'rating': 4.4, 'available': False, 'year': 2001},
        ]
        return pd.DataFrame(books_data)

    def get_all_books(self):
        """Return all books as DataFrame"""
        return self.books

    def search_books(self, query):
        """Search books by title or author"""
        query = query.lower()
        results = self.books[
            self.books['title'].str.lower().str.contains(query) |
            self.books['author'].str.lower().str.contains(query)
        ]
        return results

    def get_books_by_genre(self, genre):
        """Get all books in a specific genre"""
        return self.books[self.books['genre'] == genre]

    def recommend_books(self, favorite_genres, num_recommendations=5):
        """
        Recommend books based on favorite genres

        Args:
            favorite_genres (list): List of user's favorite genres
            num_recommendations (int): Number of books to recommend

        Returns:
            DataFrame: Recommended books
        """
        if not favorite_genres:
            # Return top-rated available books if no preferences
            recommendations = self.books[self.books['available'] == True].nlargest(num_recommendations, 'rating')
        else:
            # Filter books by favorite genres
            genre_books = self.books[self.books['genre'].isin(favorite_genres)]

            # Filter only available books
            available_books = genre_books[genre_books['available'] == True]

            if len(available_books) >= num_recommendations:
                # Sort by rating and return top N
                recommendations = available_books.nlargest(num_recommendations, 'rating')
            else:
                # If not enough available books, include unavailable ones
                recommendations = genre_books.nlargest(num_recommendations, 'rating')

        return recommendations

    def calculate_reading_time(self, pages, reading_speed=40):
        """
        Estimate reading time based on pages

        Args:
            pages (int): Number of pages
            reading_speed (int): Pages per hour (default 40)

        Returns:
            dict: Reading time breakdown
        """
        hours = pages / reading_speed
        days_30min = (hours * 60) / 30  # If reading 30 min per day

        return {
            'total_hours': round(hours, 1),
            'days_30min': round(days_30min, 1),
            'days_1hour': round(days_30min / 2, 1)
        }

    def get_book_by_id(self, book_id):
        """Get book details by ID"""
        book = self.books[self.books['id'] == book_id]
        if not book.empty:
            return book.iloc[0].to_dict()
        return None

    def get_statistics(self):
        """Get library statistics"""
        total_books = len(self.books)
        available_books = len(self.books[self.books['available'] == True])
        avg_rating = self.books['rating'].mean()

        genre_counts = self.books['genre'].value_counts().to_dict()
        most_popular_genre = max(genre_counts, key=genre_counts.get)

        return {
            'total_books': total_books,
            'available_books': available_books,
            'checked_out': total_books - available_books,
            'average_rating': round(avg_rating, 2),
            'genres': len(self.genres),
            'most_popular_genre': most_popular_genre,
            'genre_distribution': genre_counts
        }

    def get_top_rated_books(self, n=5):
        """Get top N rated books"""
        return self.books.nlargest(n, 'rating')

    def get_available_books(self):
        """Get all available books"""
        return self.books[self.books['available'] == True]
