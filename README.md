# Smart Library Management System 📚

## Domain
Education & Information Management

## Problem Statement
Libraries and reading enthusiasts face challenges in discovering books that match their interests and reading preferences. With thousands of books available, users often struggle to find relevant recommendations based on their reading history and genre preferences. Traditional library systems lack personalized recommendations and smart search capabilities.

The goal is to build a simple yet effective library management system that provides personalized book recommendations based on user preferences and helps readers discover books using content-based filtering.

## Solution Approach
To address the book discovery problem, we use a **Content-Based Filtering** recommendation system.

### What is Content-Based Filtering?
Content-based filtering recommends items similar to what a user has previously liked or shown interest in. The system analyzes the attributes (features) of items and matches them with user preferences.

In our library system:
1. **User Preferences**: Users select their favorite genres (e.g., Science, Fiction, Technology)
2. **Book Attributes**: Each book has attributes like genre, author, rating, pages, and year
3. **Recommendation Logic**: The system filters books matching user's favorite genres and ranks them by rating
4. **Smart Features**: Reading time estimation, availability tracking, and search functionality

Our approach:
1. **Book Database**: A curated collection of 20 diverse books across 10 genres
2. **Genre-Based Filtering**: Recommend books based on user's favorite genres
3. **Rating-Based Ranking**: Sort recommendations by book ratings to suggest the best books first
4. **Reading Time Calculator**: Estimate how long it will take to read a book based on page count
5. **Search & Analytics**: Enable search by title/author and provide library statistics

## Technologies Used
- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **Streamlit**: Web-based user interface
- **Content-Based Filtering**: Simple recommendation algorithm

## Project Structure
```
smart-library/
│
├── src/
│   ├── app.py              # Main Streamlit application
│   └── library_system.py   # Book recommendation engine
│
├── screenshot/
│   └── image.png          # Application screenshot
│
├── statement.md           # Detailed problem statement
├── README.md              # This file
└── requirements.txt       # Python dependencies
```

## How to Run
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd smart-library
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application:**
   ```bash
   streamlit run src/app.py
   ```

4. **Open your browser** and navigate to the provided local URL (usually `http://localhost:8501`)

## Features

### 1. Home Dashboard
- View library statistics (total books, available books, average rating)
- Browse top-rated books
- See genre distribution chart

### 2. Search Books
- Search by book title or author
- Filter by genre
- Filter by availability status
- View book details including rating, pages, year, and estimated reading time

### 3. Get Recommendations
- Select your favorite genres (1-3 genres)
- Choose number of recommendations (3-10 books)
- Get personalized book suggestions ranked by rating
- View reading time estimates:
  - Total hours required
  - Days if reading 30 min/day
  - Days if reading 1 hour/day

### 4. Analytics Dashboard
- Library overview metrics
- Genre distribution analysis
- Availability statistics
- Average pages by genre
- Rating distribution charts

## Functional Requirements

### Module 1: Book Management
- Store and manage book information (title, author, genre, pages, rating, year, availability)
- Search books by title or author
- Filter books by genre and availability
- Display book details

### Module 2: Recommendation Engine
- Content-based filtering using genre preferences
- Rating-based ranking of recommendations
- Configurable number of recommendations
- Availability-aware suggestions

### Module 3: Analytics & Insights
- Calculate library statistics
- Track genre distribution
- Monitor book availability rates
- Generate reading time estimates
- Visualize data with charts

## Non-Functional Requirements

1. **Performance**: Fast recommendation generation (< 1 second for 20 books)
2. **Usability**: Simple, intuitive interface requiring no training
3. **Reliability**: Consistent recommendations with accurate data
4. **Maintainability**: Clean, well-documented code with clear structure
5. **Security**: Input validation and safe data handling

## Algorithm: Content-Based Filtering

### Recommendation Logic
```python
def recommend_books(favorite_genres, num_recommendations):
    # Step 1: Filter books by user's favorite genres
    filtered_books = books[books['genre'] in favorite_genres]

    # Step 2: Filter only available books
    available_books = filtered_books[filtered_books['available'] == True]

    # Step 3: Sort by rating (highest first)
    sorted_books = available_books.sort_by('rating', descending=True)

    # Step 4: Return top N recommendations
    return sorted_books.head(num_recommendations)
```

### Reading Time Estimation
```python
def calculate_reading_time(pages, reading_speed=40):
    # Average reading speed: 40 pages/hour
    total_hours = pages / reading_speed
    days_30min = (total_hours * 60) / 30
    days_1hour = days_30min / 2

    return {
        'total_hours': total_hours,
        'days_30min': days_30min,
        'days_1hour': days_1hour
    }
```

## Sample Book Dataset
The system includes 20 carefully selected books across 10 genres:
- Fiction (3 books)
- Science (3 books)
- Technology (3 books)
- History (2 books)
- Biography (2 books)
- Fantasy (2 books)
- Mystery (2 books)
- Self-Help (2 books)
- Business (1 book)

## Results
The system successfully provides:
- **Fast Recommendations**: Instant book suggestions based on genre preferences
- **Accurate Estimates**: Reading time calculations help users plan their reading
- **Easy Discovery**: Search and filter features make finding books effortless
- **Insightful Analytics**: Statistics help understand library collection and usage

## Future Enhancements
- User accounts with reading history tracking
- Collaborative filtering (recommendations based on similar users)
- Book ratings and reviews from users
- Integration with external book APIs (Google Books, Open Library)
- Machine learning-based recommendations
- Book reservation system
- Mobile app version

## Author
**Your Name** - 25BHI10016
VIT University
Course: [Your Course Name]

## Acknowledgments
- VITyarthi platform for project guidelines
- Streamlit community for excellent documentation
- Classic literature and modern bestsellers for inspiration

---

*This project demonstrates software engineering principles including data structures, algorithms (content-based filtering), user interface design, and data visualization.*
