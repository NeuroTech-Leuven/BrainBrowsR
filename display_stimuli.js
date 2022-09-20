// insert the stimuli
insertStimuli();


function makeURL(img_path) {
  // eslint-disable-next-line no-undef
  return browser.runtime.getURL(img_path);
}

function hideElement(element) {
  element.style.display = "none";
}

function insertStimuli() {
  var like = document.createElement("img");
  like.setAttribute("src", makeURL("icons/like_darkblue.png"));
  like.className = "like";
  document.body.appendChild(like);

  var comment = document.createElement("img");
  comment.setAttribute("src", makeURL("icons/comment_green.png"));
  comment.className = "comment";
  document.body.appendChild(comment);

  var up = document.createElement("img");
  up.setAttribute("src", makeURL("icons/up_red.png"));
  up.className = "up";
  document.body.appendChild(up);

  var down = document.createElement("img");
  down.setAttribute("src", makeURL("icons/down_lightblue.png"));
  down.className = "down";
  document.body.appendChild(down);
}
