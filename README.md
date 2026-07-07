# GameArena 🎮
GameArena is a full-stack game tracking and recommendation platform built with Django.

Users can:
- Browse thousands of games
- Maintain a personal game library
- Create wishlists
- Rate games across multiple categories
- Receive personalized game recommendations

This project demonstrates backend development, REST APIs, MySQL, PostgreSQL, Docker, and recommendation system implementation.

# Live Demo 🚀
**Application:** https://gamebrain.onrender.com

Note: Hosted on Render (Free Tier). The application may take 30–60 seconds to wake after periods of inactivity.

## Screenshots

# Tech Stack
### Backend
- Python
- Django
- Django REST Framework

### Database
- PostgreSQL
- MySQL

### Frontend
- HTML
- CSS
- JavaScript
- AJAX

### Machine Learning
- scikit-learn
- Content-Based Recommendation

### DevOps
- Docker
- Docker Compose
- Gunicorn
- Render

# Run with Docker
#### 1. Clone the repo:
```
git clone git@github.com:Ajyothsna758/gamebrain.git
cd gamebrain

```
#### 2. create .env file:
```
cp .env.example .env
```
#### 3. Start containers
```
sudo docker compose down -v
sudo docker compose up --build
```
#### 4. Access the Application
**Application:** http://localhost:8000
# Game Tracking & Recommendations Application using Django + Mysql
- Fetch data from IGDB API
- Developed wishlist, library and rating functionality for games
- Recommended games for new and existing users
# WishList Feature:
- Enable users to add or remove games from their personal wishlist **without reloading the page**. This improves user experience and provides real-time feedback.
## Features:
- Users can add or remove games from their personal wishlist without page reload.
- Clicking the wishlist icon toggles the game in the database and updates the icon in real-time for logged in users.
- Clicking the wishlist icon while logged out redirects the user to the login page.
- Implemented using Django, JavaScript, and AJAX:
  - Backend: Django view `toggle_wishlist` handles add/remove logic.
  - Frontend: JavaScript fetch API sends POST requests and updates the icon dynamically.
  - CSRF token handled securely in AJAX headers.
- The icon changes visually when a game is in the wishlist.
## Implementation details:
- __Backend Django__
  - `toggle_wishlist` view handles add/remove logic and returns JSON response 
    - If the game is not in the wishlist → create entry → return `{"status": "added"}`
    - If the game is already in the wishlist → delete entry → return `{"status": "removed"}`
  - Stores wishlist entries in `WishList` model with `user` and `game` fields.
  - Added wishlist tab to display WishListed games.
- __Frontend JavaScript__
  - Listens for clicks on .wishlist-icon.
  - Sends a POST request to the backend with the game_id.
  - Includes the CSRF token for security.
  - Handles redirect to login if the user is not authenticated.
  - Updates the icon dynamically to show the current status.
# User Library Feature:
- Enable users to add or remove games from their User Library **without reloading the page**
- Users can choose different statuses for games in their library like:
  - Uncategorized
  - Not played
  - Currently playing
  - Completed 
  - Dropped
- Clicking the library icon toggles the game in the database and updates the icon in real-time for logged-in users.
- Clicking the library icon while logged out redirects the user to the login page.
- - Implemented using Django, JavaScript, and AJAX:
  - Backend: Django views handle toggle, status update, and removal logic. Used Django Template Language (DTL) to render dynamic library and status data on the frontend.
  - Frontend: JavaScript fetch API sends POST requests and updates the icon dynamically.
  - CSRF token handled securely in AJAX headers.
- The icon changes visually when a game is in the library.
## Features:
### 1. Add Games to Library:
- Users can click the library icon on a game card to add it to their library.
- Library icon changes dynamically to indicate state (active/inactive).
- When a game is added to the library:
  - The library icon becomes active.
  - The dropdown arrow becomes visible.
### 2. Open status popup:
- Clicking the active library icon or dropdown arrow opens a status popup.
- When the popup opens for the first time, “Uncategorized” is automatically active by default.
- Users can change the game status directly from the popup.
- The popup includes a "Remove from Library" option
### 3. Update status:
- Selecting the status updates the database instantly.
- Highlights the selected status.
- Removes the previous active state.
### 4. Remove from Library:
- User clicks Remove from Library option from status popup.
  - Remove from library.
  - closes status popup.
  - Deactivates library icons.
  - Hides library dropdown arrow.
- Wishlist and Library are mutually exclusive:
  - Adding to Wishlist removes it from Library.
  - Adding to Library removes it from Wishlist.
# Rating Feature:
- Enable users to rate games by clicking the Rate button on each game card.
- Clicking on the rate button -> popup opens for both logged-in users and anonymous or new users.
- Only authenticated users can submit ratings.
- Instead of using a traditional star‑based rating system, users  can choose from distinct rating types: 
  - Recommended
  - Excellent
  - Average
  - Skip
- Ratings are split into:
  - Overall Rating
  - Category Ratings (Gameplay, Visual, Audio, Story and Playability)
- Rating selections update the UI instantly and persist in the database without a page reload.
## Features:
### 1. Overall Rating:
- Clicking the "Rate" button opens the rating modal below the button
- Users can rate a game using predefined rating types (e.g., Excellent, Good, Average).
- Clicking the same rating type again removes it (toggle behavior).
- Clicking a different rating updates the existing one.
- The average rating and label update dynamically.
### 2. Category- Based Rating:
- Users can rate specific categories independently.
- Ratings are sent via AJAX fetch() requests to Django backend endpoints.
- CSRF tokens are included to secure the POST requests.
- Each category maintains its own average.
# Search Functionality:
- when user search with game name related all game names are displayed

# Recommendations Feature:
## For New Users
- for new users I used __Rule-based / content-based__ recommendations
- new users can select their preferences at onboarding:
  - Genres (RPG, Music, Action…)
  - Platforms (PC, PS5…)
  - Player perspectives (First-person, Third-person…)
  - Themes (Fantasy, Music…)
- for recommendations filter the games based on these preferences and sort them by rating (total_rating) as a score.
### Process:
- While user sign up or register (New user)
  - users can select their preferences(genres, platform, theme, plater_perspectives)
    - If user select his/her choices:
     - based on that choices display with high rated and recently released games
    - If user skip his/her choices:
     - high rated and recently released games are recommended
### Development:
- Created `UserPreference` model to store user preferred genres, platform, player perspective, theme and completed_onboarding flag
- created `onboarding_preferences` view to select preferences by user after sign up
- created related urls and templates
- created recommendations logic
  - If user selected his/her favorite genres filter the games with same genres and did same for remaining fields
  - If user didn't selected preferences ordered the games with rating and related fields
- Showed game recommendations in recommendations page  

## For Existing Users
- For existing users games recommendations I used __content based__ recommendations
- It suggests similar games based on wishlist and library games.
- This system uses games meta data like genres, platforms, player perspective, franchise, themes, game mode, developer and publisher
- The general idea behind these recommender systems is that if a person likes a particular game, he or she will also like an game that is similar to it.
- Added ML based Recommendation for existing users
### Development:
- First, I extracted user interactions such as library games, ratings, and wishlist using the `get_user_seed_games` function.
- Extracted structured metadata from a user’s seed games, which we use to build a user preference profile for content-based recommendations.
- Found all candidate games that match the user’s preferences
- Calculated a relevance score for a game based on how well it matches the user’s preferences, and provide reasons for the recommendation.
- Generated personalized game recommendations for an existing user based on the games they have previously interacted with
- Showed game recommendations in recommendations page

