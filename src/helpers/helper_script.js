/*
This function finds the next post from the current post and processes it
*/
function nextFromCurrent(current) {
    // If the current post is none, get the first one in the dom
    if (!current) {
        return getPostByIndex(0);
    }
    // get all the posts in the dom
    let tempPosts = getPosts();
    // find where the current posts is in the dom
    let ind = findByIndex(tempPosts, current);
    // calculate the next post
    let newCurrent = tempPosts[ind + 1];
    // process this post
    processPost(newCurrent);
    return newCurrent;
}

/*
This function finds the next post from the current post and processes it
*/
function previousFromCurrent(current) {
    // If the current post is none, get the first on in the dom
    if (!current) {
        return getPostByIndex(0);
    }
    // get all the posts in the dom
    let tempPosts = getPosts();
    // get the index of the current post in the dom
    let ind = findByIndex(tempPosts, current);
    // if already first, stay else go to previous
    let newCurrent;
    if (ind) {
        newCurrent = tempPosts[ind - 1];
    } else {
        newCurrent = current;
    }
    // process the post
    processPost(newCurrent);
    return newCurrent;
}

/*
Deprecated, gets a post by index and processes it
*/
function getAndProcessPost(index) {
    var post = getPostByIndex(index);
    if (post) {
        processPost(post);
        return post;
    }

}

/*
Processes a post in the following way, finds and formats the interactive elements, scrolls to the post and centers it in the page
*/
function processPost(post) {
    const interactive_elements = post.querySelectorAll("._abl-");
    formatInteractiveElements(interactive_elements);
    // scroll to the given post
    post.scrollIntoView({ behaviour: "smooth" });
    centerPost(post)
}

/*
Center a post in the page
*/
function centerPost(post){
    post.style.position = "static";
    post.style.left = "35%";
}

/*
Hides unused interactive elements
*/
function formatInteractiveElements(interactive_elements) {
    hideElement(interactive_elements[0]);
    hideElement(interactive_elements[3]);
    hideElement(interactive_elements[4]);
    hideElement(interactive_elements[5]);
}

/*
Get all the posts currently in the dom
*/
function getPosts() {
    return document.querySelectorAll("article")
}

/*
Deprecated: get the post in the dom with a given index
*/
function getPostByIndex(index) {
    const temp_posts = document.querySelectorAll("article");
    return temp_posts[index];
}

/*
Find the position of a given post in the dom
*/
function findByIndex(posts, current) {
    for (let i = 0; i < posts.length; i++) {
        if (current === posts[i]) {
        return i;
        }
    }
    return 0;
}

/*
Likes a post
TODO fix for English instagram
*/
function likePost(post) {

    post.querySelectorAll('svg[aria-label="Like"]').forEach(svg => svg.closest("button").click());

    post.querySelectorAll('svg[aria-label="Unlike"]').forEach(svg => svg.closest("button").click());

}


async function confirmAction(color) {
    setBackground(color)
    await sleep(500);
    setBackground("lightblue")

}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/*
This elements disables flickering of certain elements
*/
function enableFlicker() {
    var elts = document.querySelectorAll('._8ykn');
    for(i = 0; i < elts.length; i++) {      
      elts[i].classList.remove('_8ykn');
    }
  }

function testHeadset(data) {
    document.getElementsByClassName("test_headset")[0].innerHTML = data
}