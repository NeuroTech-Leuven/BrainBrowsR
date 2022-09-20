let activation = document.getElementById("activation_button");
let hello = "I'm defined in a page script!";

activation.addEventListener("click", function () {
  if (activation.value == 0) {
    activation.value = 1;
    browser.tabs.executeScript({
      file: "/display_stimuli.js",
    });
    activation.innerHTML = "Deactivate overlay"
  } else {
    activation.value = 0;
    browser.tabs.executeScript({
      file: "/hide_stimuli.js",
    });
    activation.innerHTML = "Activate overlay"
  }
})


