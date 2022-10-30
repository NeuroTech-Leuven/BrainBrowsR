/*
Content scripts can not access the local files directly and have to do this through the browser runtime
*/
function makeURL(img_path) {
  return browser.runtime.getURL(img_path);
}

/*
Inserts the only GUI stimuli into the webpage
*/
function insertStimuli() {
  var like = document.createElement("img");
  like.setAttribute("src", makeURL("icons/test_like.png"));
  // like.setAttribute("src", makeURL("icons/invert_like.png"));
  like.className = "stimuli_gui like";
  document.body.appendChild(like);

  var comment = document.createElement("img");
  comment.setAttribute("src", makeURL("icons/test_on.png"));
  comment.className = "stimuli_gui comment";
  document.body.appendChild(comment);

  var up = document.createElement("img");
  up.setAttribute("src", makeURL("icons/test_up.png"));
  up.className = "stimuli_gui up";
  document.body.appendChild(up);

  var down = document.createElement("img");
  down.setAttribute("src", makeURL("icons/test_down.png"));
  down.className = "stimuli_gui down";
  document.body.appendChild(down);
}

function removeElement(element) {
  element.remove();
}


function hideStimuli() {
  hideElement(document.getElementsByClassName("like")[0]);
  // hideElement(document.getElementsByClassName("comment")[0]);
  hideElement(document.getElementsByClassName("up")[0]);
  hideElement(document.getElementsByClassName("down")[0]);
}

/*
Display the stimuli by name
*/
function displayStimuli() {
  displayElement(document.getElementsByClassName("like")[0]);
  displayElement(document.getElementsByClassName("comment")[0]);
  displayElement(document.getElementsByClassName("up")[0]);
  displayElement(document.getElementsByClassName("down")[0]);
}

function assign_stimulus(post, targetClassList, targetAriaList, period_list) {
  // First GUI elements
  if (targetClassList.length > 0) {
    for (let i = 0; i < targetClassList.length; i++) {
      var currentElement = document.body.querySelector(targetClassList[i]);
      //current_element.classList.add("non_gui_stimuli");
      //we let GUI elements start at higher
      const currentIndex = targetAriaList.length + i;
      currentElement.style.setProperty('--freq', period_list[currentIndex] + 's');
    }
  }
  // Then non-GUI elements via Aria labels
  if (targetAriaList.length > 0) {
    for (let i = 0; i < targetAriaList.length; i++) {
      if (targetAriaList[i].length > 1) {

        //get the parent element to transform
        var currentElement = post.querySelector(targetAriaList[i][0]);
        var stimulus = currentElement.closest(targetAriaList[i][targetAriaList[i].length-1]);

        //assign the frequency
        stimulus.classList.add("non_gui_stimuli");

        stimulus.style.setProperty('--freq', period_list[i] + 's');

        // choose a random color
        var colors = ['#ff0000', '#00ff00', '#0000ff'];
        var randomColor = colors[Math.floor(Math.random() * colors.length)];
        stimulus.style.setProperty('background-color', randomColor);
        stimulus.style.setProperty('z-index', 9999);
      } else {
        var stimulus = post.querySelector(targetAriaList[i][0]);
        stimulus.classList.add("non_gui_stimuli");

        stimulus.style.setProperty('--freq', period_list[i] + 's');

        // choose a random color
        var colors = ['#ff0000', '#00ff00', '#0000ff'];
        var randomColor = colors[Math.floor(Math.random() * colors.length)];
        stimulus.style.setProperty('background-color', randomColor);
        stimulus.style.setProperty('z-index', 9999);
      }
    }
  }


}
