document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("searchGames");
    const input = form.querySelector(".instant-search__input");

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        const query = input.value.trim();
        if (query.length < 3) {
            alert('Please enter at least 3 characters.');
            return;
        }
        // Redirect to the search results page with the query as a parameter
        window.location.href = `/search_results?q=${encodeURIComponent(query)}`;
    });
});