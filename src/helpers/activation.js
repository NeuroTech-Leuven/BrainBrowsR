let activation_button = document.getElementById("activation_button");
var currentActivation = localStorage.getItem("activation_value");

// if (currentActivation == 0) {
  activation_button.innerHTML = "Start Experiment";
// } else {
  // activation_button.innerHTML = "Deactivate overlay";
// }

activation_button.addEventListener("click", function () {
  // if (currentActivation == 0) {
    currentActivation = 1;
    localStorage.setItem("activation_value", currentActivation);
    browser.tabs.executeScript({
      // file: "../stimuli/display_stimuli.js",
      file: "../stimuli/record_stimuli.js",
    });
    // activation_button.innerHTML = "Deactivate overlay";
  // } else {
    // curr/entActivation = 0;
    // localStorage.setItem("activation_value", currentActivation);
    // browser.tabs.executeScript({
    //   file: "../stimuli/hide_stimuli.js",
    // });
    // activation_button.innerHTML = "Activate overlay";
  // }
});
