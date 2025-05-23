/*
 * games.js
 * 
 * A JavaScript file to fetch and display top board games data
 * using AJAX techniques similar to the books.js example.
 */

window.addEventListener("load", initialize);

function initialize() {
    var element = document.getElementById('games_button');
    element.onclick = onGamesButtonClicked;
}

// Returns the base URL of the API, onto which endpoint components can be appended.
function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api';
    return baseURL;
}

function onGamesButtonClicked() {
    var url = getAPIBaseURL() + '/games/';

    // Send the request to the Games API /games/ endpoint
    fetch(url, {method: 'get'})
    
    // Check if the response is ok before proceeding
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("Games list API response received");
        return response.json();
    })

    // Once you have your list of game dictionaries, use it to build
    // an HTML table displaying the game information.
    .then(function(gamesList) {
        console.log("Games list data:", gamesList);
        // Build the table header
        var tableBody = '<tr><th>Game Name</th><th>Year</th><th>Rating</th></tr>';
        
        // Build the table body
        for (var k = 0; k < gamesList.length; k++) {
            tableBody += '<tr>';
            
            // Game name with a link to get details
            tableBody += '<td><a onclick="getGameDetails(' + gamesList[k]['id'] + ",'"
                            + gamesList[k]['name'] + "')\">"
                            + gamesList[k]['name'] + '</a></td>';
            
            // Year published
            tableBody += '<td>' + gamesList[k]['yearpublished'] + '</td>';
            
            // Rating
            tableBody += '<td>' + gamesList[k]['average'] + '</td>';
            
            tableBody += '</tr>';
        }

        // Put the table body we just built inside the table that's already on the page.
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = tableBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.error("Error fetching games list:", error);
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = '<tr><td colspan="3">Error loading games: ' + error.message + '</td></tr>';
        }
    });
}

function getGameDetails(gameID, gameName) {
    // Fetch and display details for a specific game
    var url = getAPIBaseURL() + '/games/' + gameID;

    fetch(url, {method: 'get'})
    
    // Check if the response is ok before proceeding
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        console.log("Game details API response received for ID:", gameID);
        return response.json();
    })

    .then(function(gameDetails) {
        console.log("Game details data:", gameDetails);
        var tableBody = '<tr><th colspan="2">' + gameName + ' Details</th></tr>';
        
        // Display various game details
        tableBody += '<tr><td>Designer</td><td>' + gameDetails['designer'] + '</td></tr>';
        tableBody += '<tr><td>Publisher</td><td>' + gameDetails['publisher'] + '</td></tr>';
        tableBody += '<tr><td>Year Published</td><td>' + gameDetails['yearpublished'] + '</td></tr>';
        tableBody += '<tr><td>Average Rating</td><td>' + gameDetails['average'] + '</td></tr>';
        tableBody += '<tr><td>Min Players</td><td>' + gameDetails['minplayers'] + '</td></tr>';
        tableBody += '<tr><td>Max Players</td><td>' + gameDetails['maxplayers'] + '</td></tr>';
        tableBody += '<tr><td>Playing Time</td><td>' + gameDetails['playingtime'] + ' minutes</td></tr>';
        
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = tableBody;
        }
    })

    .catch(function(error) {
        console.error("Error fetching game details:", error);
        var resultsTableElement = document.getElementById('results_table');
        if (resultsTableElement) {
            resultsTableElement.innerHTML = '<tr><td colspan="2">Error loading game details: ' + error.message + '</td></tr>';
        }
    });
}

