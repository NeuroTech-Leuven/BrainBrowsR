hideStimuli();


function removeElement(element) {
    element.remove();
  }

function hideStimuli() {
    removeElement(document.getElementsByClassName("like")[0]);
    removeElement(document.getElementsByClassName("comment")[0]);
    removeElement(document.getElementsByClassName("up")[0]);
    removeElement(document.getElementsByClassName("down")[0]);
}