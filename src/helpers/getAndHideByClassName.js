import { hideElement } from "./hideElement";

export function getAndHideElementByClassName(className) {
  var element = document.getElementsByClassName(className)[0];
  if (element) {
    hideElement(element);
    console.log(className);
  }
}
