// Make it clear that the extension has loaded
document.body.style.border = "6px solid pink";

// wait a bit
setTimeout(main, 300);

function setUp() {
  var currentPost = getAndProcessPost(0);
  try {
    const websocket = new WebSocket("ws://localhost:8002/");
    websocket.addEventListener("message", ({ data }) => {
      const event = JSON.parse(data);
      console.log(event);
      switch (event) {
        case "N":
          currentPost = nextFromCurrent(currentPost);
          break;
        case "P":
          currentPost = previousFromCurrent(currentPost);
          break;
      }
    });
  } catch (e) {
    console.log(e);
  }
}

// TODO clean up the code below with imports

function main() {
  editPage();
  setUp();
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

function nextFromCurrent(current) {
  if (!current) {
    return getPostByIndex(0);
  }
  let tempPosts = getPosts();
  let ind = findByIndex(tempPosts, current);
  let newCurrent = tempPosts[ind + 1];
  processPost(newCurrent);
  return newCurrent;
}

function previousFromCurrent(current) {
  if (!current) {
    return getPostByIndex(0);
  }
  let tempPosts = getPosts();
  let ind = findByIndex(tempPosts, current);
  let newCurrent;
  if (ind) {
    newCurrent = tempPosts[ind - 1];
  } else {
    newCurrent = current;
  }
  processPost(newCurrent);
  return newCurrent;
}

function getAndProcessPost(index) {
  var post = getPostByIndex(index);
  processPost(post);
  return post;
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

function getPosts() {
  return document.getElementsByTagName("article");
}

function getPostByIndex(index) {
  const temp_posts = document.getElementsByTagName("article");
  return temp_posts[index];
}

function findByIndex(posts, current) {
  for (let i = 0; i < posts.length; i++) {
    if (current === posts[i]) {
      return i;
    }
  }
  return 0;
}
