/*
Content scripts can not access the local files directly and have to do this through the browser runtime
*/
function makeURL(img_path) {
  return browser.runtime.getURL(img_path);
}

/*
Inserts the stimuli into the webpage
*/
function insertStimuli() {
  var like = document.createElement("img");
  like.setAttribute("src", makeURL("icons/test_like.png"));
  // like.setAttribute("src", makeURL("icons/invert_like.png"));
  like.className = "stimuli like";
  document.body.appendChild(like);

  var comment = document.createElement("img");
  comment.setAttribute("src", makeURL("icons/test_on.png"));
  comment.className = "stimuli comment";
  // document.body.appendChild(comment);

  var up = document.createElement("img");
  up.setAttribute("src", makeURL("icons/test_up.png"));
  up.className = "stimuli up";
  document.body.appendChild(up);

  var down = document.createElement("img");
  down.setAttribute("src", makeURL("icons/test_down.png"));
  down.className = "stimuli down";
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

