

window.addEventListener("load", initialize);


function initialize() {
    document.getElementById('searchBut').addEventListener('click', onSearch);
}

// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/games?';
    return baseURL;
}

function getGameUrl() {
    let out = window.location.protocol + '//' + 
                window.location.hostname + ':' +
                window.location.port + '/game'
    return out;
}

function onSearch(event) {
    console.log("CLICKED")
    let baseUrl = getAPIBaseURL();
        event.preventDefault();
        let params = [];

        let numPlays = document.getElementById('numPlays').value;
        if (numPlays) params.push('numPlays=' + encodeURIComponent(numPlays));

        let complexity = document.getElementById('complexity').value;
        if (complexity) params.push('complexity=' + encodeURIComponent(complexity));

        let minAge = document.getElementById('minAge').value;
        if (minAge) params.push('minAge=' + encodeURIComponent(minAge));

        let time = document.getElementById('time').value;
        if (time) params.push('time=' + encodeURIComponent(time));

        let mechanicsSelect = document.getElementById('mechanics');
        let selectedMechanics = Array.from(mechanicsSelect.selectedOptions).map(opt => opt.value);
        if (selectedMechanics.length > 0) {
            params.push("mechanics=" + encodeURIComponent(selectedMechanics.join(',')));
        }
        let designer = document.getElementById('designer').value;
        if (designer) params.push('designer=' + encodeURIComponent(designer));

        let fullUrl = baseUrl + params.join('&');
        console.log("Final URL:", fullUrl);
        window.location.href = fullUrl;
    }