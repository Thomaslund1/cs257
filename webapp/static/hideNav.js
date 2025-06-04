/* When the user scrolls down, hide the navbar. When the user scrolls up, show the navbar 
adapted from https://www.w3schools.com/howto/howto_js_navbar_hide_scroll.asp*/
var prevScrollpos = window.pageYOffset;
var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-80px";
  }
  prevScrollpos = currentScrollPos;
} 