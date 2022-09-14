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

function hideElement(element) {
  element.style.display = "none";
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
