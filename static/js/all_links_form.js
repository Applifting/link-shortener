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

const param = window.location.search;
const filter = {};

for (const [key, value] of new URLSearchParams(param).entries()) {
  filter[key] = value;
}
//use case switch
let popUp = document.getElementById("pop");
let values = filter.status;
switch (values) {
  case "updated":
    popUp.style.display = "flex";
    popUp.innerHTML = "Link updated";
    break;
  case "created":
    popUp.style.display = "flex";
    popUp.innerHTML = "Link created";
    break;
  case "deleted":
    popUp.style.display = "flex";
    popUp.innerHTML = "Link deleted";
    break;
  case "duplicate":
    popUp.style.display = "flex";
    popUp.innerHTML = "This shortlink already exists";
    break;
  case "form-invalid":
    popUp.style.display = "flex";
    popUp.innerHTML = "Form invalid";
    break;
  case "not-allowed":
    popUp.style.display = "flex";
    popUp.innerHTML = "Name in URL is not allowed";
    break;
}

let pop = document.getElementById("popEdit");
let value = filter.status;
switch (value) {
  case "activated":
    pop.style.display = "flex";
    pop.innerHTML = "Link activated";
    break;
  case "deactivated":
    pop.style.display = "flex";
    pop.innerHTML = "Link disabled";
    break;
  case "form-invalid":
    pop.style.display = "flex";
    pop.innerHTML = "Form Invalid";
    break;
  case "reset":
    pop.style.display = "flex";
    pop.innerHTML = "Password reset";
    break;
  case "not-allowed":
    pop.style.display = "flex";
    pop.innerHTML = "Name in URL is not allowed";
    break;
}

let passwordBorder = document.getElementsByClassName("container1__border")[0];
let valuess = filter.status;
switch (valuess) {
  case "incorrect-password":
    passwordBorder.classList.add("container1__red__border");
    document.getElementsByClassName(
      "container1__incorrectPass"
    )[0].style.display = "block";
    break;
}
