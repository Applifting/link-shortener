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
  $("#search").keyup(function () {
    delay(function () {
      document.getElementById("forms").submit();
    });
  });
}
// persist checkbox value
function getParamValues() {
  const filterParam = window.location.search;
  const filter = {};

  for (const [key, value] of new URLSearchParams(filterParam).entries()) {
    filter[key] = value;
  }
  function persistStateOfFormValues() {
    $("#ownerFilter").val(filter.owner);
    $("#search").val(filter.search);
    $("#checkbox").prop("checked", filter.is_active);
  }
  persistStateOfFormValues();
  function colorSwitch() {
    if (filter.is_active) {
      $("#statusDisabled").css("color", "#CF7317");
      $("#statusActive").css("color", "#AAA9BC");
    } else {
      $("#statusDisabled").css("color", "#AAA9BC");
      $("#statusActive").css("color", "#1F7A78");
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
