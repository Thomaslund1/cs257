document.addEventListener("DOMContentLoaded", function() {
  fetch('/api/game_names')
    .then(response => response.json())
    .then(boardGames => {
      autocomplete(document.getElementById("myInput"), boardGames);
    });
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
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          b = document.createElement("DIV");
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          b.addEventListener("click", function(e) {
              inp.value = this.getElementsByTagName("input")[0].value;
              closeAllLists();
              // Redirect to the game page for the selected name
              window.location.href = "/game/" + encodeURIComponent(inp.value);
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
        if (currentFocus > -1) {
          e.preventDefault(); // Only prevent default if selecting an autocomplete item
          if (x) x[currentFocus].click();
        } else if (x && x.length > 0) {
          // If no suggestion is highlighted, select the first one
          e.preventDefault();
          x[0].click();
        }
        // Otherwise, allow form to submit normally
      }
  });
  function addActive(x) {
    if (!x) return false;
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    x[currentFocus].classList.add("autocomplete-active");
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