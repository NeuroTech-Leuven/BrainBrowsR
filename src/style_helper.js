/*
Hides an html element
*/
function hideElement(element) {
    element.style.display = "none";
  }
function displayElement(element) {
    element.style.display = "initial";
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
    return browser.runtime.getURL(img_path);
}

function addLogo(logo_png) { 
    var logo = document.createElement("img");
    logo.setAttribute("src", makeURL(logo_png));
    logo.className = "logo";
    document.body.appendChild(logo);
}


function setBackground(color) {
    document.body.style.backgroundColor = color;
}


function centerPost(post){
    post.style.position = "relative";
    post.style.left = "35%";
}
    