document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("recommender-form");
    if (!form) return;

    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const game1 = encodeURIComponent(document.querySelector('[name="game1"]').value.trim());
        const game2 = encodeURIComponent(document.querySelector('[name="game2"]').value.trim());
        const game3 = encodeURIComponent(document.querySelector('[name="game3"]').value.trim());

        const query = new URLSearchParams();
        if (game1) query.append("game1", game1);
        if (game2) query.append("game2", game2);
        if (game3) query.append("game3", game3);

        window.location.href = `/recommendation?${query.toString()}`;
    });
});
