document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const query = urlParams.get('q');
    const resultsTable = document.getElementById('results_table');
    console.log(query)
    if (!query || query.length < 3) {
        resultsTable.innerHTML = '<tr><td colspan="7">Please enter at least 3 characters.</td></tr>';
        return;
    }

    fetch(`/api/search_games?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            const gamesList = data.results;
            if (!gamesList || gamesList.length === 0) {
                resultsTable.innerHTML = '<tr><td colspan="7">No results found.</td></tr>';
                return;
            }
            // Build the table header
            let tableBody = `
                <tr>
                    <th>Game Name</th>
                    <th>Year</th>
                    <th>Rating</th>
                    <th>Playing Time</th>
                    <th>Min Age</th>
                    <th>Players</th>
                    <th>Designer</th>
                </tr>
            `;
            // Build the table body
            for (let k = 0; k < gamesList.length; k++) {
                const game = gamesList[k];
                tableBody += `<tr>
                    <td><a href="/game?id=${game.id}">${game.name}</a></td>
                    <td>${game.yearpublished || ''}</td>
                    <td>${game.average || ''}</td>
                    <td>${game.playingtime || ''}</td>
                    <td>${game.age || ''}</td>
                    <td>${game.minplayers || ''}${game.maxplayers && game.minplayers !== game.maxplayers ? ' - ' + game.maxplayers : ''}</td>
                    <td>${game.designer || ''}</td>
                </tr>`;
            }
            resultsTable.innerHTML = tableBody;
        })
        .catch(error => {
            resultsTable.innerHTML = `<tr><td colspan="7">Error: ${error.message}</td></tr>`;
        });
});