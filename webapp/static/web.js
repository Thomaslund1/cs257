

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
        if (numPlays) params.push('plays=' + encodeURIComponent(numPlays));

        let complexity = document.getElementById('complexity').value;
        if (complexity) params.push('complexity=' + encodeURIComponent(complexity));

        let minAge = document.getElementById('minAge').value;
        if (minAge) params.push('age=' + encodeURIComponent(minAge));

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

async function populateMechanicsDropdown() {
        try {
            // Fetch mechanics from the /api/mechanics endpoint
            const response = await fetch('/api/mechanics');
            
            // Check if the response is OK (status code 200)
            if (!response.ok) {
                throw new Error('Failed to fetch mechanics');
            }

            // Parse the JSON response
            const mechanics = await response.json();

            // Get the select element
            const selectElement = document.getElementById('mechanics');

            // Clear existing options
            selectElement.innerHTML = '';

            // Populate dropdown with the mechanics from the API
            mechanics.forEach(mechanic => {
                const option = document.createElement('option');
                option.value = mechanic.id;  // Assuming mechanic object has an 'id' and 'name' field
                option.textContent = mechanic.name;  // Display mechanic name
                selectElement.appendChild(option);
            });
        } catch (error) {
            console.error('Error populating mechanics dropdown:', error);
        }
    }

    // Call the function to populate the mechanics dropdown when the page loads
    document.addEventListener('DOMContentLoaded', populateMechanicsDropdown);