export function getAndProcessPost(index) {
  var post = getPostByIndex(index);
  processPost(post);
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

function getPostByIndex(index) {
  const temp_posts = document.getElementsByTagName("article");
  return temp_posts[index];
}
