let activation = document.getElementById("activation_button");
let hello = "I'm defined in a page script!";

activation.addEventListener("click", function () {
  if (activation.value == 0) {
    activation.value = 1;
  } else {
    activation.value = 0;
  }
});
browser.tabs.executeScript({
  file: "/content_script.js",
});
