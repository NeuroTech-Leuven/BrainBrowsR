# Processing Posts

Written by: Samuel Berton

## Goal

Once a particular post is parsed, it needs to be processed so that the data is helpful to the user. In this case, it removes the unnecessary buttons and scrolls to the active post and centres this post on the page.

## Details & Implementation

As was mentioned above, the goal is threefold:

1. Remove the unnecessary buttons,
2. Scroll to the active post.
3. Center the post

The implementation in JavaScript can be found in [this file](../../src/helpers/helper_script.js) as processPost. The function that implements each part will be given step by step.

The first part consists of finding the buttons and then removing them. Finding them is similar to [the parsing section](./parsing.md). To remove a particular element, you can hide it using [CSS](https://stackoverflow.com/questions/19400139/what-are-the-possible-ways-to-hide-an-element-via-css) or [HTML](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/hidden). The implementation finds the interactive elements and then passes them to the function formatInteractiveElements.

The second part can be implemented using a function such as [scroll into view](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView). This function is applied to an HTML element and takes the behaviour and alignment as arguments.

Finally, to centre the post. The element's style can be edited to be centred in the middle of the page, which is implemented in centerPost.

## Results

Scrolling to posts is currently working perfectly. Removing the clutter still contains some bugs that will be fixed in the next version.