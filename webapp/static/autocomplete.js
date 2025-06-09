document.addEventListener("DOMContentLoaded", function() {
  fetch('/api/game_names')
    .then(response => response.json())
    .then(boardGames => {
      autocomplete(document.getElementById("myInput"), boardGames);
    });

  // Redirect search to /games?name=QUERY
  const searchForm = document.querySelector('.search-container');
  if (searchForm) {
    searchForm.addEventListener('submit', function(e) {
      const input = document.getElementById("myInput");
      if (input && input.value.trim() !== "") {
        e.preventDefault();
        window.location.href = "/games?name=" + encodeURIComponent(input.value.trim());
      }
    });
  }
});

// adapted from W3Schools autocomplete function
// https://www.w3schools.com/howto/howto_js_autocomplete.asp
// Autocomplete function to suggest board game names
// based on user input in the input field with id "myInput"
// and the provided array of board game names. 
function autocomplete(inp, arr) {
  let currentFocus;
  inp.addEventListener("input", function(e) {
      let a, b, i, val = this.value;
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      this.parentNode.appendChild(a);
      for (i = 0; i < arr.length; i++) {
        // Added Case-insensitive match
        let matchIndex = arr[i].toUpperCase().indexOf(val.toUpperCase());
        if (matchIndex !== -1) {
          b = document.createElement("DIV");
          b.innerHTML = arr[i].substr(0, matchIndex)
            + "<strong>" + arr[i].substr(matchIndex, val.length) + "</strong>"
            + arr[i].substr(matchIndex + val.length);
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          b.addEventListener("click", function(e) {
              inp.value = this.getElementsByTagName("input")[0].value;
              closeAllLists();
              window.location.href = "/games?name=" + encodeURIComponent(inp.value);
          });
          a.appendChild(b);
        }
      }
  });
  inp.addEventListener("keydown", function(e) {
      let x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        currentFocus++;
        addActive(x);
      } else if (e.keyCode == 38) {
        currentFocus--;
        addActive(x);
      } else if (e.keyCode == 13) {
        if (x && currentFocus > -1) {
          e.preventDefault();
          // Redirect to /games?name= on enter
          inp.value = x[currentFocus].getElementsByTagName("input")[0].value;
          closeAllLists();
          window.location.href = "/games?name=" + encodeURIComponent(inp.value);
        } else if (x && x.length > 0) {
          e.preventDefault();
          inp.value = x[0].getElementsByTagName("input")[0].value;
          closeAllLists();
          window.location.href = "/games?name=" + encodeURIComponent(inp.value);
        }
      }
  });
  function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("autocomplete-active");
    x[currentFocus].scrollIntoView({ block: "nearest" });
  }
  function removeActive(x) {
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    let x = document.getElementsByClassName("autocomplete-items");
    for (let i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}