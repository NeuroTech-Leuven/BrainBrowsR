
var posts = document.getElementsByClassName("_ab8w  _ab94 _ab99 _ab9h _ab9m _ab9p _abcm")
var post_array = [].slice.call(posts);
var post_array_visible = removeItemAll(post_array);
console.log(post_array_visible);





function posY(elm) {
    var test = elm, top = 0;

    while(!!test && test.tagName.toLowerCase() !== "body") {
        top += test.offsetTop;
        test = test.offsetParent;
    }

    return top;
}

function viewPortHeight() {
    var de = document.documentElement;

    if(!!window.innerWidth)
    { return window.innerHeight; }
    else if( de && !isNaN(de.clientHeight) )
    { return de.clientHeight; }

    return 0;
}

function scrollY() {
    if( window.pageYOffset ) { return window.pageYOffset; }
    return Math.max(document.documentElement.scrollTop, document.body.scrollTop);
}

function checkvisible( elm ) {
    var vpH = viewPortHeight(), // Viewport Height
        st = scrollY(), // Scroll Top
        y = posY(elm);

    return (y < (vpH + st));
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
