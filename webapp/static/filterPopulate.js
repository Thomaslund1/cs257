// Populate filter inputs from URL parameters
window.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);

    // Helper to set value if present
    function setInputValue(id, param) {
        const el = document.getElementById(id);
        if (el && params.has(param)) {
            el.value = params.get(param);
        }
    }

    setInputValue('numPlays', 'numPlays');
    setInputValue('name', 'name');
    setInputValue('minAge', 'minAge');
    setInputValue('time', 'time');
    setInputValue('designer', 'designer');

    // Mechanics (multi-select)
    if (params.has('mechanics')) {
        const mechanicsSelect = document.getElementById('mechanics');
        // mechanics param could be comma-separated or repeated
        let values = params.getAll('mechanics');
        if (values.length === 1 && values[0].includes(',')) {
            values = values[0].split(',');
        }
        for (const option of mechanicsSelect.options) {
            if (values.includes(option.value)) {
                option.selected = true;
            }
        }
    }
});
