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
- 
# Search Functionality:
- when user search with game name related all game names are displayed
