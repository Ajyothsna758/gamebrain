console.log("Library JS loaded");
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
                    // change wishlist icon if user clicks on library icon
                    const libraryIcon= game_card.querySelector(".library-icon")
                    if (libraryIcon){
                        libraryIcon.src= "/static/img/icons/library_remove.svg"
                    }

                } else if (data.status === "removed") {
                    icon.classList.remove('active');
                } else {
                    console.log(data.message);
                }
            })
            .catch(err => console.error(err));
        });
    });
    // library
    const library_icons= document.querySelectorAll(".library-icon");
    library_icons.forEach(icon => {
        icon.addEventListener("click", function(){
            console.log("icon clicked")
            const game_card = icon.closest('.game-card');
            const url= icon.dataset.url;
            fetch(url, {
                method:"POST",
                headers:{
                    "X-CSRFToken": csrftoken
                }
            })
            .then(response => {
                if (response.redirected){
                    window.location.href = response.url;
                    return;
                }
                return response.json();
            })
            .then(data =>{
                if(data.in_library){
                    icon.src= "/static/img/icons/library_add.svg";
                    const wishlistIcon= game_card.querySelector(".wishlist-icon")
                    if (wishlistIcon){
                        wishlistIcon.classList.remove("active")
                    }
                }
                else{
                    icon.src= "/static/img/icons/library_remove.svg";
                }
            })
            .catch(console.error);
        });
    });
    // update library status
//     const status_items= document.querySelectorAll(".status-items");
//   status_items.forEach(item => {
//     item.addEventListener('click', function(e) {
//         e.preventDefault();
//         const url = item.dataset.url;

//         fetch(url, {
//             method: "POST",
//             headers: {
//                 "X-CSRFToken": csrftoken
//             }
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 console.log("Status updated:", data.status_name);
//                 // optionally update the UI
//             }
//         })
//         .catch(console.error);
//     });
// });
});