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
    if (post) {
        processPost(post);
        return post;
    }

}

function processPost(post) {
    const interactive_elements = post.querySelectorAll("._abl-");
    formatInteractiveElements(interactive_elements);
    post.scrollIntoView({ behaviour: "smooth" });
    // centerPost(post)
}

function centerPosts(){
    const posts = document.querySelectorAll("article");
    for(i = 0; i < posts.length; i++) {      
        posts[i].style.position = "relative";
        posts[i].style.left = "35%";    
      }
    post.style.position = "relative";
    post.style.left = "35%";
}

function formatInteractiveElements(interactive_elements) {
    hideElement(interactive_elements[0]);
    hideElement(interactive_elements[3]);
    hideElement(interactive_elements[4]);
    hideElement(interactive_elements[5]);
    // interactive_elements[0].classList.add("stimuli like")
    // interactive_elements[3].classList.add("stimuli like")
    // interactive_elements[4].classList.add("stimuli like")
    // interactive_elements[5].classList.add("stimuli like")
}

function getPosts() {
    // return document.getElementsByTagName("article");
    return document.querySelectorAll("article")

}

function getPostByIndex(index) {
    // const temp_posts = document.getElementsByTagName("article");
    const temp_posts = document.querySelectorAll("article");
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

    post.querySelectorAll('svg[aria-label="Vind ik leuk"]').forEach(svg => svg.closest("button").click());

    post.querySelectorAll('svg[aria-label="Vind ik niet meer leuk"]').forEach(svg => svg.closest("button").click());

}


async function confirmAction(color) {
    setBackground(color)
    await sleep(500);
    setBackground("lightblue")

}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function enableFlicker() {
    var elts = document.querySelectorAll('._8ykn');
    for(i = 0; i < elts.length; i++) {      
      elts[i].classList.remove('_8ykn');
    }
  }