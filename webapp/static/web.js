

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

        let name = document.getElementById('name').value;
        if (name) params.push('name=' + encodeURIComponent(name));

        let age = document.getElementById('minAge').value;
        if (age) params.push('age=' + encodeURIComponent(age));

        let time = document.getElementById('time').value;
        if (time) params.push('time=' + encodeURIComponent(time));

        let mechanicsSelect = document.getElementById('mechanics');
        let selectedMechanics = Array.from(mechanicsSelect.selectedOptions)
            .map(opt => parseInt(opt.value) + 1); // shift by 1

        if (selectedMechanics.length > 0) {
            selectedMechanics.forEach(id => {
                params.push("mechanics=" + encodeURIComponent(id));
            });
        }
        let designer = document.getElementById('designer').value;
        if (designer) params.push('designer=' + encodeURIComponent(designer));

        let fullUrl = baseUrl + params.join('&');
        console.log("Final URL:", fullUrl);
        window.location.href = fullUrl;
    }

async function populateMechanicsDropdown() {
        try {
            const response = await fetch('/api/mechanics');
            
            if (!response.ok) {
                throw new Error('Failed to fetch mechanics');
            }

            const mechanics = await response.json();

            const selectElement = document.getElementById('mechanics');

            selectElement.innerHTML = '';

            // Populate dropdown with the mechanics from the API
            mechanics.forEach(mechanic => {
                const option = document.createElement('option');
                option.value = mechanic.id; 
                option.textContent = mechanic.name; 
                selectElement.appendChild(option);
            });
        } catch (error) {
            console.error('Error populating mechanics dropdown:', error);
        }
    }

    // we need some funky load order for populating then fancifying the dropdown
    document.addEventListener('DOMContentLoaded', populateMechanicsDropdown);