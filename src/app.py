"""
Smart Library Management System - Main Application
A Streamlit web application for book recommendations and library management
"""

import streamlit as st
import pandas as pd
from library_system import SmartLibrary

# Page Configuration
st.set_page_config(
    page_title="Smart Library System",
    page_icon="📚",
    layout="wide"
)

# Initialize library system
@st.cache_resource
def load_library():
    return SmartLibrary()

library = load_library()

# Custom CSS
st.markdown("""
    <style>
    .book-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    .metric-card {
        text-align: center;
        padding: 15px;
        border-radius: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📚 Smart Library")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🔍 Search Books", "💡 Get Recommendations", "📊 Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**About Smart Library**\n\n"
    "This system helps you discover books based on your preferences "
    "using content-based filtering algorithms."
)

# Main Content
if page == "🏠 Home":
    st.title("📚 Welcome to Smart Library Management System")
    st.markdown("### Discover Your Next Favorite Book")

    # Display statistics
    stats = library.get_statistics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="📖 Total Books", value=stats['total_books'])

    with col2:
        st.metric(label="✅ Available", value=stats['available_books'])

    with col3:
        st.metric(label="⭐ Avg Rating", value=stats['average_rating'])

    with col4:
        st.metric(label="📚 Genres", value=stats['genres'])

    st.markdown("---")

    # Top Rated Books
    st.subheader("⭐ Top Rated Books")
    top_books = library.get_top_rated_books(5)

    for idx, book in top_books.iterrows():
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown(f"**{book['title']}** by *{book['author']}*")
            st.caption(f"Genre: {book['genre']} | Pages: {book['pages']} | Year: {book['year']}")

        with col2:
            rating_color = "🟢" if book['rating'] >= 4.5 else "🟡"
            st.markdown(f"{rating_color} **{book['rating']}/5**")
            if book['available']:
                st.success("Available", icon="✅")
            else:
                st.error("Checked Out", icon="❌")

        st.markdown("---")

    # Genre Distribution
    st.subheader("📊 Books by Genre")
    genre_dist = pd.DataFrame(list(stats['genre_distribution'].items()),
                              columns=['Genre', 'Count'])
    st.bar_chart(genre_dist.set_index('Genre'))


elif page == "🔍 Search Books":
    st.title("🔍 Search Books")

    # Search box
    search_query = st.text_input("Search by title or author", placeholder="Enter book title or author name...")

    # Genre filter
    selected_genre = st.selectbox("Filter by Genre", ["All"] + library.genres)

    # Availability filter
    show_available_only = st.checkbox("Show only available books", value=False)

    # Get books
    if search_query:
        books = library.search_books(search_query)
        st.info(f"Found {len(books)} book(s) matching '{search_query}'")
    elif selected_genre != "All":
        books = library.get_books_by_genre(selected_genre)
    else:
        books = library.get_all_books()

    # Apply availability filter
    if show_available_only:
        books = books[books['available'] == True]

    st.markdown(f"### Showing {len(books)} book(s)")

    if len(books) == 0:
        st.warning("No books found matching your criteria.")
    else:
        # Display books in cards
        for idx, book in books.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.markdown(f"### {book['title']}")
                    st.markdown(f"**Author:** {book['author']}")
                    st.markdown(f"**Genre:** {book['genre']}")

                with col2:
                    st.markdown(f"**Pages:** {book['pages']}")
                    st.markdown(f"**Year:** {book['year']}")
                    st.markdown(f"**Rating:** ⭐ {book['rating']}/5")

                with col3:
                    if book['available']:
                        st.success("✅ Available")
                    else:
                        st.error("❌ Checked Out")

                    # Calculate reading time
                    reading_time = library.calculate_reading_time(book['pages'])
                    st.info(f"📖 ~{reading_time['total_hours']} hours")

                st.markdown("---")


elif page == "💡 Get Recommendations":
    st.title("💡 Get Personalized Book Recommendations")

    st.markdown("Select your favorite genres to get tailored book recommendations!")

    # Multi-select for genres
    favorite_genres = st.multiselect(
        "Select your favorite genres (choose 1-3):",
        library.genres,
        default=[]
    )

    # Number of recommendations
    num_recommendations = st.slider("Number of recommendations", 3, 10, 5)

    if st.button("Get Recommendations", type="primary"):
        if not favorite_genres:
            st.warning("Please select at least one genre to get recommendations.")
        else:
            st.success(f"Finding books in: {', '.join(favorite_genres)}")

            recommendations = library.recommend_books(favorite_genres, num_recommendations)

            if len(recommendations) == 0:
                st.info("No books found for selected genres. Try different genres!")
            else:
                st.markdown(f"### 📚 We found {len(recommendations)} book(s) for you!")

                for idx, book in recommendations.iterrows():
                    with st.expander(f"📖 {book['title']} - {book['author']}", expanded=True):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown(f"**Genre:** {book['genre']}")
                            st.markdown(f"**Pages:** {book['pages']}")
                            st.markdown(f"**Year:** {book['year']}")

                        with col2:
                            st.markdown(f"**Rating:** ⭐ {book['rating']}/5")

                            if book['available']:
                                st.success("✅ Available for checkout")
                            else:
                                st.warning("⏳ Currently checked out")

                        # Reading time estimation
                        reading_time = library.calculate_reading_time(book['pages'])
                        st.info(
                            f"📖 **Reading Time Estimate:**\n"
                            f"- Total: ~{reading_time['total_hours']} hours\n"
                            f"- At 30 min/day: ~{reading_time['days_30min']} days\n"
                            f"- At 1 hour/day: ~{reading_time['days_1hour']} days"
                        )

                        if book['rating'] >= 4.5:
                            st.success("🌟 Highly Recommended - Top Rated Book!")


elif page == "📊 Analytics":
    st.title("📊 Library Analytics")

    stats = library.get_statistics()

    # Overview metrics
    st.subheader("Library Overview")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Books in Collection",
            value=stats['total_books'],
            delta=None
        )

    with col2:
        availability_rate = (stats['available_books'] / stats['total_books']) * 100
        st.metric(
            label="Availability Rate",
            value=f"{availability_rate:.1f}%",
            delta=f"{stats['available_books']} available"
        )

    with col3:
        st.metric(
            label="Average Book Rating",
            value=f"{stats['average_rating']}/5",
            delta="⭐ High Quality"
        )

    st.markdown("---")

    # Genre Analysis
    st.subheader("📚 Genre Distribution")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Books per Genre:**")
        genre_df = pd.DataFrame(list(stats['genre_distribution'].items()),
                               columns=['Genre', 'Count'])
        st.dataframe(genre_df, use_container_width=True)

    with col2:
        st.markdown("**Most Popular Genre:**")
        st.info(f"🏆 {stats['most_popular_genre']}")

        st.markdown("**Genre Variety:**")
        st.success(f"📖 {stats['genres']} different genres available")

    # Chart
    st.bar_chart(genre_df.set_index('Genre'))

    st.markdown("---")

    # Availability Analysis
    st.subheader("📖 Availability Analysis")

    availability_data = pd.DataFrame({
        'Status': ['Available', 'Checked Out'],
        'Count': [stats['available_books'], stats['checked_out']]
    })

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(availability_data, use_container_width=True)

    with col2:
        st.bar_chart(availability_data.set_index('Status'))

    # Average pages by genre
    st.markdown("---")
    st.subheader("📄 Average Pages by Genre")

    all_books = library.get_all_books()
    avg_pages = all_books.groupby('genre')['pages'].mean().sort_values(ascending=False)

    st.bar_chart(avg_pages)

    # Rating distribution
    st.markdown("---")
    st.subheader("⭐ Rating Distribution")

    rating_bins = pd.cut(all_books['rating'], bins=[0, 4.0, 4.5, 5.0],
                         labels=['Good (< 4.0)', 'Great (4.0-4.5)', 'Excellent (4.5+)'])
    rating_dist = rating_bins.value_counts()

    st.bar_chart(rating_dist)


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Smart Library System v1.0**")
st.sidebar.caption("Built with Python & Streamlit")
