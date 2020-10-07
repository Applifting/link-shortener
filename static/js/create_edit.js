//
let openAdvSettings = document.getElementById("advSettings");
var icon = document.getElementById("icon");
var open = false;
function toggleAdvSettings() {
  openAdvSettings &&
    openAdvSettings.addEventListener("click", function () {
      let modal = document.getElementById("advRequirements");
      if (modal.style.maxHeight) {
        modal.style.maxHeight = null;
      } else {
        modal.style.maxHeight = modal.scrollHeight + "px";
      }
      if (open) {
        icon.className = "rotate";
      } else {
        icon.className = "rotate open";
      }

      open = !open;
    });
}
// button disable
function disableBtn() {
  let orgLink = document.getElementById("orgUrl");
  let shortLink = document.getElementById("shortlink");
  let formInput = document.getElementsByClassName("formRequiredField");
  for (i = 0; i < formInput.length; i++) {
    submit.disabled = true;
    formInput &&
      formInput[i].addEventListener("keyup", function () {
        if (shortLink.value === "" || orgLink.value === "") {
          submit.disabled = true;
        } else {
          submit.disabled = false;
        }
      });
  }
}
// dynamic text update

function txtUpdateOnChange() {
  let shortLink = document.getElementById("shortlink");
  shortLink &&
    shortLink.addEventListener("keyup", function () {
      let printout = document.getElementById("fueledEndPoint");
      printout.innerHTML = "/" + shortLink.value;
    });
}

//copy inline
function copySingle() {
  let hoverCopy = document.getElementsByClassName("copyHoverSquare");
  var range = document.createRange();
  range.selectNode(document.getElementById("shortlinked"));
  window.getSelection().removeAllRanges(); // clear current selection
  window.getSelection().addRange(range); // to select text
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  hoverCopy[0].innerHTML = "copied!";
  setTimeout(function () {
    hoverCopy[0].innerHTML = "copy";
  }, 800);
}
