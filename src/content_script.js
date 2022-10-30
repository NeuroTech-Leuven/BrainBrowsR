// Make it clear that the extension has loaded
document.body.style.border = "10px solid lightblue";
// wait a bit
setTimeout(main, 1000);
var stimuli_on = 0;

function main() {

   //for GUI elements, as specified in inserted CSS
  const targetClassList = [".down",".up",".like",".comment"];
   //for HTML non-GUI interactables, in pairs of The arialabel of the 
   // interactables and the type of element
  const targetAriaList = [['svg[aria-label="Like"]', 'svg[aria-label="Unlike"]','button'],['svg[aria-label="Comment"]','button'],['[aria-label="Add a comment…"]']];
  // change refreshrate here
  const refreshRate = 60;

  // setup control variable
  stimuli_on = 1;

  // generate frequencies automatically
  const period_list = generate_frequencies(targetClassList,targetAriaList, refreshRate);
  
  editPage(targetClassList,targetAriaList,period_list);
  setUp(targetClassList,targetAriaList,period_list);
}

/*
Starts the websockets connection that waits for messages from the server in server.py. When receiving a message it will perform an action
*/
function setUp(targetClassList,targetAriaList,period_list) {
  var currentPost = getAndProcessPost(0,targetClassList,targetAriaList,period_list);
  try {
    const websocket = new WebSocket("ws://localhost:8002/");
    websocket.addEventListener("message", ({ data }) => {
      const event = JSON.parse(data);
      console.log(event);
      switch (event) {
        case "3":
          currentPost = nextFromCurrent(currentPost,targetClassList,targetAriaList,period_list);
          confirmAction("green");
          testHeadset(event);
          break;
        case "2":
          currentPost = previousFromCurrent(currentPost,targetClassList,targetAriaList,period_list);
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
function editPage(targetClassList,targetAriaList,period_list) {
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


  // add the logo
  addLogo("icons/logonutl.png")

  // document.body.style.backgroundColor = "lightblue";
  setBackground("lightblue");

  // insert the GUI stimuli
  setTimeout(insertStimuli, 1000);

  //disable externally inserted classes that disable flickers
  enableFlicker();
  
  // scroll to the first post
  setTimeout(getAndProcessPost,1600,0,targetClassList,targetAriaList,period_list); 


  var test_headset = document.createElement("div");
  test_headset.innerHTML = "Waiting for headset data"
  test_headset.className = "test_headset";
  document.body.appendChild(test_headset);
}



