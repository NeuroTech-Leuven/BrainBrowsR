// Make it clear that the extension has loaded
document.body.style.border = "6px solid pink";

// wait a bit
setTimeout(editPage, 300);
// Set up the websockets
setUp();
// set the counter
var counter = 0;

function setUp() {
  try {
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
      getAndProcessPost(counter);
    });
  } catch (e) {
    console.log(e);
  }
}

function editPage() {
  // hide the menubar
  getAndHideElementByClassName("_acum");
  // hide the story menu
  getAndHideElementByClassName("_aac4 _aac5 _aac6");
  // hide the sidebar
  getAndHideElementByClassName("_aak6 _aak9");
  // hide the top bar
  getAndHideElementByClassName("_acbl");
  // scroll to the first post
  getAndProcessPost(0);
  // add the logo
  var logo = document.createElement("img");
  logo.setAttribute("src", makeURL("icons/logonutl.png"));
  logo.className = "logo";
  document.body.appendChild(logo);
}

/*
Hides an html element
*/
function hideElement(element) {
  element.style.display = "none";
}

/*
Gets an element by classname and then hides it if it exists
*/
function getAndHideElementByClassName(className) {
  var element = document.getElementsByClassName(className)[0];
  if (element) {
    hideElement(element);
  }
}

function makeURL(img_path) {
  // eslint-disable-next-line no-undef
  return browser.runtime.getURL(img_path);
}

function next() {
  console.log("Go to the next post");
  counter++;
}

function previous() {
  console.log("Go to the previous post");
  counter = counter ? counter - 1 : counter;
}

function getAndProcessPost(index) {
  var post = getPostByIndex(index);
  processPost(post);
}

function processPost(post) {
  const interactive_elements = post.getElementsByClassName("_abl-");
  formatInteractiveElements(interactive_elements);
  post.scrollIntoView({ behaviour: "smooth" });
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
