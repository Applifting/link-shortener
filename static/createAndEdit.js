//
let openmode = document.getElementById("advanced");
let orgUrl = document.getElementById("orgUrl");
let shortLink = document.getElementById("shortlink");
let tr = document.querySelectorAll(".tr");
let shortLinked = document.getElementById("shortlinked");
let shareBox = null;

let setopen = document.getElementById("settings");
var icon = document.getElementById("icon");
var open = false;
function toggleAdvSettings() {
  setopen &&
    setopen.addEventListener("click", function () {
      let modal = document.getElementById("extra");
      this.classList.toggle("active");
      if (modal.style.maxHeight) {
        modal.style.maxHeight = null;
      } else {
        modal.style.maxHeight = modal.scrollHeight + "px";
      }
      if (open) {
        icon.className = "fa fa-angle-right";
      } else {
        icon.className = "fa fa-angle-right open";
      }

      open = !open;
    });
}
// button disable
function disableBtn() {
  let inputs = document.getElementsByClassName("inputs");
  for (i = 0; i < inputs.length; i++) {
    submit.disabled = true;
    inputs &&
      inputs[i].addEventListener("keyup", function () {
        if (shortLink.value === "" || orgUrl.value === "") {
          submit.disabled = true;
        } else {
          submit.disabled = false;
        }
      });
  }
}
// dynamic text update

function txtUpdateOnChange() {
  shortLink &&
    shortLink.addEventListener("keyup", function () {
      let printout = document.getElementById("shortlinked");
      var x = shortLink.value;
      printout.innerHTML = "www.fueled.by/" + x;
    });

  if ($(".editAndCreate").length) {
    document.getElementById("shortlinked").style.color = "#AAA9BC";
    document.getElementById("shortlinked").style.fontWeight = "bold";
  }
}

//copy inline
function copySingle() {
  let hovercopy = document.getElementsByClassName("square");
  var range = document.createRange();
  range.selectNode(document.getElementById("shortlinked"));
  window.getSelection().removeAllRanges(); // clear current selection
  window.getSelection().addRange(range); // to select text
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
  hovercopy[0].innerHTML = "copied!";
  setTimeout(function () {
    hovercopy[0].innerHTML = "copy";
  }, 800);
}
// date picker
if ($(".editAndCreate").length) {
  function datePicker() {
    $(function () {
      $('input[name="birthday"]').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        minYear: 1901,
        maxYear: parseInt(moment().format("YYYY"), 10),
      });
    });
  }
}
