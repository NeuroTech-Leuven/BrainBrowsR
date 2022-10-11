// Make it clear that the extension has loaded
document.body.style.border = "10px solid lightblue";

// wait a bit
setTimeout(main, 500);

function main() {
  editPage();
  setUp();
}


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
  addLogo("icons/logonutl.png")

  // document.body.style.backgroundColor = "lightblue";
  setBackground("lightblue");
}



