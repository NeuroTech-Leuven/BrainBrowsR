# Parsing

Written by: Samuel Berton

## Goal

With parsing, we extract aspects of the HTML code that each website is built on. Other blocks then use the extracted data to create the desired effect of the extension.

## Details

Each website consists of three fundamental technologies:

1. [HTML][1], hypertext markup language
2. [CSS][2] cascading style sheets
3. [Javascript][3]

HTML provides the document's structure into titles, sections, images, and links. To view the HTML code of any website, the 'Inspect Element' button in your browser can be used by right-clicking it.
Though plain HTML can already be used for many things, it needs to be supplemented with CSS and Javascript to have nice-looking, dynamic websites. CSS provides the style, and javascript makes the websites dynamic. These three technologies play an essential part in every website. However, as a side note, people use technologies like React to make modern websites.

Our extension runs in what is called a content script. This script is a piece of Javascript code inserted in the webpage and can then find and change certain aspects of the website using HTML and CSS. In the case of parsing, this uses functions such as [document.getElementById][4].

## Implementation

The actual implementation of the parser consists of two parts:

1. Finding the posts in the HTML,
2. Collect them with a query function.

To find the posts in the HTML code, it is recommended to use developer tools in the browser. It depends on which browser is used, but we recommend using either [firefox][6] or [chrome][5]. The panel used here is called the elements panel. ![Elements panel](images/elements_panel.png) In this panel, you find the source HTML code of the website. For most modern websites, such as Facebook and Instagram, this is very complex and consists of many layers. To make it easier to find the post, there is a handy tool in the right corner of the developer tools. ![Selection Tool](./images/selection_tool.png). Hovering with your mouse on certain elements will highlight them and show them in HTML. You may need to look at children or parents, but this tool will get you as close as possible.

Next, a query function is used to collect them. For this, we need to know what makes a post unique from other elements. For Instagram, either the class or the article tag can be used. The selection function is then either getElementByClassName or getElementByTagName. Both function roughly the same as [get element by id][4]. The result of this function is an HTML collection, which can be converted to an array or used as is.

The implementation can be found in [here](../../src/helpers/helper_script.js) as the getPosts. On Instagram, you can select the posts using the article tag. A minor issue is that the [Document-Object-Model](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction) only loads a limited amount of posts at once. There is some extra logic needed to navigate between posts instead of using an index. This logic is implemented in nextFromCurrent and previousFromCurrent. It works as follows: first, all the posts currently in the dom are parsed, then the index of the current post is found in this array, and this new index is then used to find either the next or previous.

## Results

We can successfully find all the posts on Instagram. The parsed posts can then be used inside the other functions to implement functionality on the posts, which can be extended to other websites, such as Reddit and Twitter. The above methodology is straightforward to extend to websites, structured similarly to Instagram (a feed).

[1]: https://en.wikipedia.org/wiki/HTML "HTML"
[2]: https://en.wikipedia.org/wiki/CSS "CSS"
[3]: https://en.wikipedia.org/wiki/JavaScript "Javascript"
[4]: https://developer.mozilla.org/en-US/docs/Web/API/Document/getElementById "Get element by id"
[5]: https://developer.chrome.com/docs/devtools/ "Chrome devtools"
[6]: https://developer.mozilla.org/en-US/docs/Tools "Mozilla devtools"
