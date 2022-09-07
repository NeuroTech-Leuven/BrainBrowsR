// Hide the menu bar
hideElement(document.getElementsByClassName("_acum")[0]);
// Hide the sidebar
hideElement(document.getElementsByClassName("_aak6 _aak9")[0]);
// Get the posts
var posts = overlay_post_array();
// Go the first post and start the counter
posts[0].scrollIntoView();
var counter = 0;

var inter_p = find_interactive(posts);
editInteractive(inter_p);

function hideElement(element) {
  element.style.display = "none";
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
    "_ab6k _ab6m _aatb _aatc _aate _aatf _aath _aati"
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
