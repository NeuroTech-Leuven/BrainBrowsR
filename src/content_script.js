// Make it clear that the extension has loaded
document.body.style.border = "10px solid lightblue";

// wait a bit
setTimeout(main, 1000);
var stimuli_on = 0;

function main() {
  editPage();
  stimuli_on = 1;
  setUp();
  
}

/*
Starts the websockets connection that waits for messages from the server in server.py. When receiving a message it will perform an action
*/
function setUp() {
  var currentPost = getAndProcessPost(0);
  try {
    const websocket = new WebSocket("ws://localhost:8002/");
    websocket.addEventListener("message", ({ data }) => {
      const event = JSON.parse(data);
      console.log(event);
      switch (event) {
        case "3":
          currentPost = nextFromCurrent(currentPost);
          confirmAction("green");
          testHeadset(event);
          break;
        case "2":
          currentPost = previousFromCurrent(currentPost);
          confirmAction("green");
          testHeadset(event);
          break;
        case "0" :
          likePost(currentPost);
          confirmAction("green");
          testHeadset(event);
          break;
        case "1" :
          if (stimuli_on == 0) {
            stimuli_on = 1;
            displayStimuli();           
          } else {
            stimuli_on = 0;
            hideStimuli();          
          } 
          testHeadset(event);
                   
          confirmAction("green");
          break;
      } 
    });
  } catch (e) {
    console.log(e);
  }
}

/*
Edit the page on startup of the extension. This removes some of the bars in instagram and inserts the stimuli
*/
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

  setTimeout(insertStimuli, 1000);
  enableFlicker();
  // centerPosts();

  var test_headset = document.createElement("div");
  test_headset.innerHTML = "Waiting for headset data"
  test_headset.className = "test_headset";
  document.body.appendChild(test_headset);
}



