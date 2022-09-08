// Hide the menu bar
hideElement(document.getElementsByClassName("_acum")[0]);
// Hide the sidebar
hideElement(document.getElementsByClassName("_aak6 _aak9")[0]);
// hideElement(document.getElementsByClassName("_ab6k _ab6m _aatb _aatc _aatd _aatf")[0]);
// new_html = "dit is toch al iet anders"
// editElement(document.getElementsByClassName("_ab8w  _ab94 _ab99 _ab9h _ab9m _ab9p _abcm")[0]);
// document.getElementById("content").innerHTML = "whatever";
// Get the posts
var posts = overlay_post_array();

// Go the first post and start the counter
posts[0].scrollIntoView();
var counter = 0;

var inter_p = find_interactive(posts);

editInteractive(inter_p);

// let fullURL = browser.runtime.getURL("icons/like_darkblue.png");

// var like_element = document.createElement('img');
// var like_element = document.createElement('div');
// like_element.className = "like_class";
// like_element.setAttribute("src", beastURL);
// // like_element.innerHTML = '<object type="text/html" data= fullURL ></object>';
// // like_element.innerHTML = "<img src=\"icons/like_darkblue.png\" width=\"150\" height=\"150\">";
// // clock_element.style.cssText = 'font-size:25px;position:fixed;width:105px;height:35px;left:1000px;top:100px;opacity:0.3;z-index:900;color:#d0d0d0;background:#404040';
// like_element.style.cssText = 'position:fixed;width:150;height:150;left:1000px;top:100px;z-index:900;color:#d0d0d0;background:#404040';

// document.body.appendChild(like_element);



// let url = browser.runtime.getURL("beasts/frog.jpg");
addImage(makeURL("icons/like_darkblue.png"));

let comment = document.createElement('img');
comment.setAttribute("src", makeURL("icons/comment_green.png"));
comment.style.cssText = 'position:fixed;width:150px;height:150px;left:900px;top:400px';
comment.className = "comment-image";
document.body.appendChild(comment);

let arrow_up = document.createElement('img');
arrow_up.setAttribute("src", makeURL("icons/up_red.png"));
arrow_up.style.cssText = 'position:fixed;width:150px;height:150px;left:1100px;top:200px';
arrow_up.className = "arrow_up-image";
document.body.appendChild(arrow_up);


let arrow_down = document.createElement('img');
arrow_down.setAttribute("src", makeURL("icons/down_lightblue.png"));
arrow_down.style.cssText = 'position:fixed;width:150px;height:150px;left:1100px;top:400px';
arrow_down.className = "arrow_down-image";
document.body.appendChild(arrow_down);


function makeURL(img_path) {
  return browser.runtime.getURL(img_path);
}

function addImage(img_url) {
  let like_element = document.createElement('img');
  like_element.setAttribute("src", img_url);
  like_element.style.cssText = 'position:fixed;width:150px;height:150px;left:900px;top:200px';
  like_element.className = "like-image";
  document.body.appendChild(like_element);
}
function hideElement(element) {
  element.style.display = "none";

}

function editElement(element) {
  // element.innerHTML = '<object type="text/html" data="popup.html" ></object>';; 
  element.innerHTML = "hier was een post";

}

function processPosts(posts) {}

function formatInteractiveElements(interactive_elements) {
  interactive_elements[0].style.display = "none";
  interactive_elements[3].style.display = "none";
  interactive_elements[4].style.display = "none";
  interactive_elements[5].style.display = "none";
}

function editInteractive(interactive_elements_posts) {
  interactive_elements_posts.map((p) => formatInteractiveElements(p));
}

function find_interactive(active_posts) {
  const interactive_elements = active_posts.map((post) =>
    toArray(post.getElementsByClassName("_abl-"))
  );
  return interactive_elements;
}

function overlay_post_array() {
  var posts = document.getElementsByClassName(
    "_ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p  _abc0 _abcm"
  );
  var post_array = toArray(posts);
  return post_array;
}

function toArray(collection) {
  let a = [];
  for (var i = 0; i < collection.length; i++) a.push(collection[i]);
  return a;
}

function findFirstChildByClass(element, className) {
  var foundElement = null,
    found;
  function recurse(element, className, found) {
    for (var i = 0; i < element.childNodes.length && !found; i++) {
      var el = element.childNodes[i];
      var classes = el.className != undefined ? el.className.split(" ") : [];
      for (var j = 0, jl = classes.length; j < jl; j++) {
        if (classes[j] == className) {
          found = true;
          foundElement = element.childNodes[i];
          break;
        }
      }
      if (found) break;
      recurse(element.childNodes[i], className, found);
    }
  }
  recurse(element, className, false);
  return foundElement;
}

function posY(elm) {
  var test = elm,
    top = 0;

  while (!!test && test.tagName.toLowerCase() !== "body") {
    top += test.offsetTop;
    test = test.offsetParent;
  }

  return top;
}

function viewPortHeight() {
  var de = document.documentElement;

  if (!!window.innerWidth) {
    return window.innerHeight;
  } else if (de && !isNaN(de.clientHeight)) {
    return de.clientHeight;
  }

  return 0;
}

function scrollY() {
  if (window.pageYOffset) {
    return window.pageYOffset;
  }
  return Math.max(document.documentElement.scrollTop, document.body.scrollTop);
}

function checkvisible(elm) {
  var vpH = viewPortHeight(), // Viewport Height
    st = scrollY(), // Scroll Top
    y = posY(elm);

  return y < vpH + st;
}

function removeItemAll(arr) {
  var i = 0;
  while (i < arr.length) {
    if (checkvisible(arr[i])) {
      arr.splice(i, 1);
    } else {
      ++i;
    }
  }
  return arr;
}
