// insert the stimuli
insertStimuli();

function makeURL(img_path) {
  // eslint-disable-next-line no-undef
  return browser.runtime.getURL(img_path);
}

// function insertStimuli() {
//   var like = document.createElement("img");
//   like.setAttribute("src", makeURL("icons/invert_like.png"));
//   like.className = "stimuli like";
//   document.body.appendChild(like);

//   var comment = document.createElement("img");
//   comment.setAttribute("src", makeURL("icons/invert_comment.png"));
//   comment.className = "stimuli comment";
//   document.body.appendChild(comment);

//   var up = document.createElement("img");
//   up.setAttribute("src", makeURL("icons/invert_up.png"));
//   up.className = "stimuli up";
//   document.body.appendChild(up);

//   var down = document.createElement("img");
//   down.setAttribute("src", makeURL("icons/invert_down.png"));
//   down.className = "stimuli down";
//   document.body.appendChild(down);
// }

function removeElement(element) {
  element.remove();
}

function hideStimuli() {
  removeElement(document.getElementsByClassName("like")[0]);
  removeElement(document.getElementsByClassName("comment")[0]);
  removeElement(document.getElementsByClassName("up")[0]);
  removeElement(document.getElementsByClassName("down")[0]);
}