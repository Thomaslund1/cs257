
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
    let url = getAPIBaseURL() + '/name/';

    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function(result) {
            let selectorBody = '';
            for (let k = 0; k < result.name.length; k++) {
                let gameName = result.name[k];
                selectorBody += '<option value="' + gameName + '">' + gameName + '</option>\n';
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

    let url = getAPIBaseURL() + '/name/' + authorID;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(books) {
        let tableBody = '';
        for (let k = 0; k < books.length; k++) {
            let book = books[k];
            tableBody += '<tr>'
                            + '<td>' + book['title'] + '</td>'
                            + '<td>' + book['publication_year'] + '</td>'
                            + '</tr>\n';
        }

        // Put the table body we just built inside the table that's already on the page.
        let booksTable = document.getElementById('namesTable');
        if (booksTable) {
            booksTable.innerHTML = tableBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

