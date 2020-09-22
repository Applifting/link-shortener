//clear filter
function clearFilters() {
  window.history.replaceState({}, document.title, "/" + "links/all");
  location.reload();
  return false;
}
//delay search
function makeDelay(ms) {
  var timer = 0;
  return function (callback) {
    clearTimeout(timer);
    timer = setTimeout(callback, ms);
  };
}

function delayTextSearch() {
  var delay = makeDelay(800);
  if (window.location.pathname == "/links/all") {
    document.getElementById("search").addEventListener("keyup", function () {
      delay(function () {
        document.getElementById("forms").submit();
      });
    });
  }
}
// persist checkbox value
function getParamValues() {
  const filterParam = window.location.search;
  const filter = {};

  for (const [key, value] of new URLSearchParams(filterParam).entries()) {
    filter[key] = value;
  }
  function persistStateOfFormValues() {
    if (window.location.pathname == "/links/all") {
      document.getElementById("checkbox").checked = filter.is_active;
      if (filter.search == undefined) {
        document.getElementById("search").value = "";
      } else {
        document.getElementById("search").value = filter.search;
      }
      if (filter.owner == undefined) {
        document.getElementById("ownerFilter").value = "";
      } else {
        document.getElementById("ownerFilter").value = filter.owner;
      }
    }
  }
  persistStateOfFormValues();
  function colorSwitch() {
    if (window.location.pathname == "/links/all") {
      if (filter.is_active) {
        document
          .getElementById("statusDisabled")
          .classList.add("orangeDisable");
        document.getElementById("statusActive").classList.add("grey");
      } else {
        document.getElementById("statusDisabled").classList.add("grey");
        document.getElementById("statusActive").classList.add("greenActive");
      }
    }
  }
  colorSwitch();
}
//

// copy

function copyShortLink(rowid) {
  let hoverCopy = document.getElementsByClassName("square-" + rowid);
  var range = document.createRange();
  range.selectNode(document.getElementById("shortlinked-" + rowid));
  window.getSelection().removeAllRanges(); // clear current selection
  window.getSelection().addRange(range); // to select text
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  hoverCopy[i].innerHTML = "copied!";
  setTimeout(function () {
    hoverCopy[i].innerHTML = "copy";
  }, 800);
}

//show social media links
function toggleShareBox(rowid) {
  let shareBox = null;

  let clickedBox = document.getElementById("box-" + rowid);
  if (shareBox && clickedBox !== shareBox) {
    shareBox.style.display = "none";
  }
  shareBox = clickedBox;
  if (shareBox.style.display === "block") {
    shareBox.style.display = "none";
  } else {
    shareBox.style.display = "block";
  }
}
