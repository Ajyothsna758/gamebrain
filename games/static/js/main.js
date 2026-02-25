console.log("JS loaded");
function getCookie(name) {
let cookieValue = null;
if(document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for(let cookie of cookies) {
        cookie = cookie.trim();
        if(cookie.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
}
return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded");
    // wishlist
    const wishlist_icon = document.querySelectorAll('.wishlist-icon');
    wishlist_icon.forEach(icon => {
        icon.addEventListener('click', function() {
            console.log("wishlish icon clicked")
            const game_card = icon.closest('.game-card'); //fetch parent game card
            const gameId = game_card.dataset.gameId; // game id from selected game card
            const url = icon.dataset.url;
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrftoken
                },
                body: new URLSearchParams({game_id: gameId})
            })
            .then(response => {
                if (response.redirected){
                    window.location.href = response.url;
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (data.status === "added") {
                    icon.classList.add('active');
                    // library removal
                    const userLibraryWrapper = game_card.querySelector(".library-wrapper");
                    if (userLibraryWrapper) {
                        const libraryIcon = userLibraryWrapper.querySelector(".library-icon");
                        const dropdownArrow = userLibraryWrapper.querySelector(".dropdown-toggle");
                        const statusPopup = userLibraryWrapper.querySelector(".library-popup");
                        if (libraryIcon) {
                            libraryIcon.classList.remove("active");
                            libraryIcon.src = "/static/img/icons/library_remove.svg";// remove active and icon change
                        }
                        if (dropdownArrow) {
                            dropdownArrow.classList.add("hidden");//hide dropdown arrow
                        }
                        if (statusPopup) {
                            statusPopup.classList.remove("show");
                        }
                    }
                } 
                else if (data.status === "removed") {
                    icon.classList.remove('active');
                }
                else {
                    console.log(data.message);
                }
            })
            .catch(err => console.error(err));
        });
    });
    // library
    document.addEventListener("click", function(e) {
        if (e.target.classList.contains("library-icon")) {
            const icon = e.target;
            const wrapper = icon.closest(".library-wrapper");
            const popup = wrapper.querySelector(".library-popup");
            const arrow = wrapper.querySelector(".dropdown-toggle");
            // already in library (active library icon)
            if (icon.classList.contains("active")) {
                closeAllPopups();
                popup.classList.toggle("show");
                return;
            }
            // first time add to library (library icon)
            fetch(icon.dataset.addUrl, {
                method: "POST",
                headers: { "X-CSRFToken": csrftoken }
            })
            .then(response => {
                    if (response.redirected){
                        window.location.href = response.url;
                        return;
                    }
                    return response.json();
            })
            .then(data => {
                if (data.in_library) {
                    icon.src = "/static/img/icons/library_add.svg";
                    icon.classList.add("active");
                    arrow.classList.remove("hidden");
                    // removed from wishlist
                    if (data.removed_from_wishlist) {
                        const wishlistIcon = wrapper.closest('.game-card').querySelector('.wishlist-icon');
                        if (wishlistIcon) wishlistIcon.classList.remove('active');
                    }
                    // Highlight Uncategorized or returned status_id
                    popup.querySelectorAll(".status-item").forEach(i => i.classList.remove("active"));
                    const selected = popup.querySelector(`.status-item[data-status-id="${data.status_id}"]`);  
                    if (selected) {
                        selected.classList.add("active");
                    }
                    else if (data.removed_from_library) {
                        icon.src = "/static/img/icons/library_remove.svg";
                        icon.classList.remove("active");
                        arrow.classList.add("hidden");
                    }
                }
            });
        }
        // dropdown arrow
        if (e.target.classList.contains("dropdown-toggle")) {
            const wrapper = e.target.closest(".library-wrapper");
            const popup = wrapper.querySelector(".library-popup");
            closeAllPopups();
            popup.classList.toggle("show");
            e.stopPropagation();
        }
        // status selection from popup
        const statusItem = e.target.closest(".status-item");
        if (statusItem) {
            const popup = statusItem.closest(".library-popup");
            fetch(statusItem.dataset.url, {
                method: "POST",
                headers: { "X-CSRFToken": csrftoken }
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    popup.querySelectorAll(".status-item").forEach(i => i.classList.remove("active")); // remove active from remaining
                    statusItem.classList.add("active"); //add active status
                }
            });
        }
        // remove from library
        if (e.target.classList.contains("remove-library")) {
            const wrapper = e.target.closest(".library-wrapper");
            const icon = wrapper.querySelector(".library-icon");
            const arrow = wrapper.querySelector(".dropdown-toggle");
            const popup = wrapper.querySelector(".library-popup");
            fetch(e.target.dataset.url, {
                method: "POST",
                headers: { "X-CSRFToken": csrftoken }
            })
            .then(res => res.json())
            .then(data => {
                if (data.removed) {
                    icon.src = "/static/img/icons/library_remove.svg";
                    icon.classList.remove("active");
                    arrow.classList.add("hidden");
                    popup.classList.remove("show");
                }
            });
        }
        // close popup click on x
        if (e.target.classList.contains("popup-close")) {
            e.target.closest(".library-popup").classList.remove("show");
        }
        // close popup when user clicks on outside popup
        document.querySelectorAll(".library-popup").forEach(popup => {
            if (!popup.contains(e.target) &&
                !e.target.classList.contains("library-icon") &&
                !e.target.classList.contains("dropdown-toggle")) {
                popup.classList.remove("show");
            }
        });
    });
    function closeAllPopups() {
        document.querySelectorAll(".library-popup")
            .forEach(p => p.classList.remove("show"));
    }
});
