// Make it clear that the extension has loaded
document.body.style.border = "5px solid red";

// Set up the websockets
setUp();

// Hide the menu bar
hideElement(document.getElementsByClassName("_acum")[0]);
// Hide the sidebar
hideElement(document.getElementsByClassName("_aak6 _aak9")[0]);
// set the counter
var counter = 0;
// Get the first post
var first_post = getPostByIndex(counter);
processPost(first_post);

// Attempt to add stylesheet this way

// document.body.appendChild(like_element);
// const css = document.styleSheets[0];
// css.insertRule(`
// @keyframes blink {
//   0% {
//     opacity: 1;
//   }
//   50% {
//     opacity: 0;
//   }
//   100% {
//     opacity: 1;
//   }`, css.cssRules.length);

var like_element = document.createElement("img");
like_element.style.cssText =
  "position:fixed;width:150px;height:150px;left:950px;top:200px"; // comment this to work with css stylesheet

var link = document.createElement("link"); // link element to add stylesheet to img
// link.rel = 'stylesheet';
// link.type = 'text/css';
// link.href = makeURL('stimuli.css');
like_element.setAttribute("src", makeURL("icons/like_darkblue.png"));
// like_element.appendChild(link)
like_element.className = "like";
document.body.appendChild(like_element);

// var link = document.createElement('link');
// link.rel = 'stylesheet';
// link.type = 'text/css';
// link.href = makeURL("stimuli.css");
var comment = document.createElement("img");
comment.setAttribute("src", makeURL("icons/comment_green.png"));
comment.style.cssText =
  "position:fixed;width:150px;height:150px;left:950px;top:400px";
// comment.appendChild(link);
comment.className = "comment";
document.body.appendChild(comment);

var arrow_up = document.createElement("img");
arrow_up.setAttribute("src", makeURL("icons/up_red.png"));
arrow_up.style.cssText =
  "position:fixed;width:150px;height:150px;left:1150px;top:200px";
arrow_up.className = "arrow_up-image";
document.body.appendChild(arrow_up);

var arrow_down = document.createElement("img");
arrow_down.setAttribute("src", makeURL("icons/down_lightblue.png"));
arrow_down.style.cssText =
  "position:fixed;width:150px;height:150px;left:1150px;top:400px";
arrow_down.className = "arrow_down-image";
document.body.appendChild(arrow_down);

function makeURL(img_path) {
  return browser.runtime.getURL(img_path);
}

function hideElement(element) {
  element.style.display = "none";
}

function editElement(element) {
  // element.innerHTML = '<object type="text/html" data="popup.html" ></object>';;
  element.innerHTML = "hier was een post";
}

function next() {
  console.log("Go to the next post");
  counter++;
}
function previous() {
  console.log("Go to the previous post");
  counter = counter ? counter - 1 : counter;
}

function setUp() {
  const websocket = new WebSocket("ws://localhost:8002/");
  websocket.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    console.log(event);
    switch (event) {
      case "N":
        next();
        break;
      case "P":
        previous();
        break;
    }
    console.log(counter);
    let post = getPostByIndex(counter);
    console.log(post);
    processPost(post);
  });
}

function processPost(post) {
  const interactive_elements = document.getElementsByClassName("_abl-");
  formatInteractiveElements(interactive_elements);
  post.scrollIntoView();
}

function formatInteractiveElements(interactive_elements) {
  hideElement(interactive_elements[0]);
  hideElement(interactive_elements[3]);
  hideElement(interactive_elements[4]);
  hideElement(interactive_elements[5]);
}

function getPostByIndex(index) {
  const temp_posts = document.getElementsByTagName("article");
  return temp_posts[index];
}

function toArray(collection) {
  const a = [];
  for (let i = 0; i < collection.length; i++) a.push(collection[i]);
  return a;
}
