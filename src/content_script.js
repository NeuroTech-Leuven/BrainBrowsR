// Make it clear that the extension has loaded
document.body.style.border = "10px solid lightblue";


// wait a bit
setTimeout(main, 300);
// main();

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
          confirmAction("green");
          break;
        case "P":
          currentPost = previousFromCurrent(currentPost);
          confirmAction("green");
          break;
        case "L" :
          likePost(currentPost);
          confirmAction("green");
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
  // hide the side menu
  getAndHideElementByClassName("x1vjfegm xvb8j5");

  // scroll to the first post
  getAndProcessPost(0);

  // add the logo
  var logo = document.createElement("img");
  logo.setAttribute("src", makeURL("icons/logonutl.png"));
  logo.className = "logo";
  document.body.appendChild(logo);

  // document.body.style.backgroundColor = "lightblue";
  setBackground("lightblue");
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
  // Attempt at less hardcoded way to hide elements

  // else {
    // count ++;
  //   console.log(className, count);
  //   if (count > 20){
  //     return;
  //   }
  //   setTimeout(getAndHideElementByClassName(className, count), 1000); // try again in 300 milliseconds
  // }
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

function likePost(post) {
  try {
    post.querySelectorAll('svg[aria-label="Vind ik leuk"]').forEach(svg => svg.closest("button").click());
  }
  catch {
    post.querySelectorAll('svg[aria-label="Vind ik niet meer leuk"]').forEach(svg => svg.closest("button").click());
  }
}


async function confirmAction(color) {
  setBackground(color)
  await sleep(500);
  setBackground("lightblue")

}

function setBackground(color) {
  document.body.style.backgroundColor = color;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

