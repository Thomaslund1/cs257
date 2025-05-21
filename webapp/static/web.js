
window.addEventListener("load", initialize);

function initialize() {
    loadAuthorsSelector();

    let element = document.getElementById('nameSelect');
    if (element) {
        element.onchange = onAuthorsSelectionChanged;
    }
}

// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function loadAuthorsSelector() {
    let url = getAPIBaseURL() + '/designer';

    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function(result) {
            console.log("Designer result:", result);
            let selectorBody = '';
            for (let k = 0; k < result.length; k++) {
                let gameEntry = result[k];
                selectorBody += '<option value="' + gameEntry.author + '">' + gameEntry.author + '</option>\n';
            }

            let selector = document.getElementById('nameSelect');
            if (selector) {
                selector.innerHTML = selectorBody;
            }
        })
        .catch(function(error) {
            console.log(error);
        });
}


function onAuthorsSelectionChanged() {
    let element = document.getElementById('nameSelect');
    if (!element) {
        return;
    }
    let authorID = element.value; 

    let url = getAPIBaseURL() + '/designer/' + authorID;
    console.log("Fetching:", url);

    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function(result) {
            let tableBody = '';
            for (let k = 0; k < result.length; k++) {
                let book = result[k];  // Each book object
                tableBody += '<tr><td>' + book.name + '</td><td>' + book.author + '</td></tr>\n';
            }

            let booksTable = document.getElementById('namesTable');
            if (booksTable) {
                booksTable.innerHTML = tableBody;
            }
        })
        .catch(function(error) {
            console.log(error);
        });
}

