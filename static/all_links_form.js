//clear filter
function clearFilters() {
  window.history.replaceState({}, document.title, "/" + "links/all");
  location.reload();
  return false;
}
// getting unique owners
function addOwnersToSelection() {
  let ownerarr = [];
  let owners = document.getElementsByClassName("rowowner");
  let ownerfilter = document.getElementById("ownerfilter");
  for (i = 0; i < owners.length; i++) {
    ownerarr.push(owners[i].innerHTML);
  }
  let ownernew = [...new Set(ownerarr)];
  for (i = 0; i < ownernew.length; i++) {
    let opt = document.createElement("option");
    opt.appendChild(document.createTextNode(ownernew[i]));
    ownerfilter.appendChild(opt);
  }
}
addOwnersToSelection();
//delay search
function delayTextSearch() {
  var delay = (function () {
    var timer = 0;
    return function (callback, ms) {
      clearTimeout(timer);
      timer = setTimeout(callback, ms);
      console.log(timer);
    };
  })();

  $("#search").keyup(function () {
    delay(function () {
      document.getElementById("forms").submit();
    }, 800);
  });
}
delayTextSearch();
// persist checkbox value
function persistCheck() {
  const filterParam = window.location.search;
  const filter = {
    disable: false,
    owner: "",
    search: "",
  };

  for (const [key, value] of new URLSearchParams(filterParam).entries()) {
    filter[key] = value;
  }
  $("#ownerfilter").val(filter.owner);
  $("#search").val(filter.search);
  function colorSwitch() {
    $("#checkbox").prop("checked", filter.disable);
    if (filter.disable) {
      $("#statusdisabled").css("color", "#CF7317");
      $("#statusactive").css("color", "#AAA9BC");
    } else {
      $("#statusdisabled").css("color", "#AAA9BC");
      $("#statusactive").css("color", "#1F7A78");
    }
  }
  colorSwitch();
}
persistCheck();
//

// copy
function copyLink(rowid) {
  let hovercopy = document.getElementsByClassName("square-" + rowid);
  var range = document.createRange();
  range.selectNode(document.getElementById("shortlinked-" + rowid));
  window.getSelection().removeAllRanges(); // clear current selection
  window.getSelection().addRange(range); // to select text
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  hovercopy[i].innerHTML = "copied!";
  setTimeout(function () {
    hovercopy[i].innerHTML = "copy";
  }, 800);
}
//show social media links

function toggleShareBox(rowid) {
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
