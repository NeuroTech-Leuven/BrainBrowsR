// Make it clear that the extension has loaded
document.body.style.border = "6px solid pink";



hideElement(document.getElementsByClassName("_aak6 _aak9")[0]);

hideElement(document.getElementsByClassName("_aac4 _aac5 _aac6")[0]);

hideElement(document.getElementsByClassName("bdao358l nu7423ey alzwoclg cmg2g80i lk0hwhjd nfcwbgbd mivixfar i54nktwv z2vv26z9 c7y9u1f0 jez8cy9q cqf1kptm oq7qnk0t o9w3sbdw mx6umkf4 t5n4vrf6 jjot6st7 ff443qle ekq1a7f9 km253p1d afopkvs9")[0]);

// Set up the websockets
setUp();

// Hide the menu bar
// hideElement(document.getElementsByClassName("_acum")[0]);
// Hide the sidebar
var logo = document.createElement("img");
logo.setAttribute("src", makeURL("icons/logonutl.png"));
logo.className = "logo";
document.body.appendChild(logo);

// set the counter
var counter = 0;
// Get the first post
var first_post = getPostByIndex(counter);
processPost(first_post);


function makeURL(img_path) {
  // eslint-disable-next-line no-undef
  return browser.runtime.getURL(img_path);
}

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
  const interactive_elements = post.getElementsByClassName("_abl-");
  console.log(interactive_elements);
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
