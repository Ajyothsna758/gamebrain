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

const csrfToken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", function() {
    document.addEventListener("click", function(e) {
        // Check if the clicked element is a wishlist button
        if (e.target.closest(".wishlist-btn")) {
            e.stopPropagation(); // prevent bubbling if needed

            const button = e.target.closest(".wishlist-btn");
            const parentDiv = button.closest(".wishlist-btn-detail");
            const gameId = parentDiv.dataset.gameId;
            const url = parentDiv.dataset.url;

            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie('csrftoken')
                },
                body: new URLSearchParams({ "game_id": gameId })
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
                    parentDiv.innerHTML = `
                        <button class="wishlist-added wishlist-btn">
                            <img src="/static/img/icons/w_add.svg" class="wishlist-icon-remove">
                            Added to Wishlist ${data.wishlist_count}
                        </button>
                    `;
                } else if (data.status === "removed") {
                    parentDiv.innerHTML = `
                        <button class="wishlist-add wishlist-btn">
                            <img src="/static/img/icons/w_add.svg" class="wishlist-icon-remove">
                            Add to Wishlist ${data.wishlist_count}
                        </button>
                    `;
                }
            })
            .catch(err => console.error(err));
        }
    });
});