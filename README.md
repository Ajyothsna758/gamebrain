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
- Enable users to add or remove games from their User Library **without reloading the page** and also user can choose different status like Uncategorized, Not played, Currently playing, Completed and Dropped
- Clicking the library icon toggles the game in the database and updates the icon in real-time for logged-in users.
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
# Search Functionality:
- when user search with game name related all game names are displayed
