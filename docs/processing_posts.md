# Processing Posts

Written by: Samuel Berton

## Goal

Once a particular post is parsed, it needs to be processed so that the data is useful to the user. In this case, it removes the unnecessary buttons and scrolls to the active post.

## Details & Implementation

As was mentioned above, the goal is twofold:

1. Remove the unnecessary buttons,
2. Scroll to the active post.

The first part consists of finding the buttons and then removing them. Finding them is similar as in [the parsing section](./parsing.md). To remove a certain element, you can hide it, using [CSS](https://stackoverflow.com/questions/19400139/what-are-the-possible-ways-to-hide-an-element-via-css) or [HTML](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/hidden).

The second part can be implemented using a function such as, [scroll into view](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollIntoView). This function is applied to a html element and takes as arguments the behaviour as well as the alignment.

## Results

Scrolling to posts is currently working perfect. Removing the clutter still contains some bugs, that will be squashed in a next version.
