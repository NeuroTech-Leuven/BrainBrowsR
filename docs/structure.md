# Structure

Written by: Samuel Berton

## Documentation guidelines

In the documentation we try to keep a similar structure, so that it is both easy to write as well as read.  
The goal of the documentation is the following:

1. Show the workings of the technology,
2. Explain the reasoning behind each of the implementations,
3. Give the opportunity to expand on the current project,
4. Be a scientific explanation of our project.

This means that the documentation has to reflect these basic principles and it should therefore be written in such a way that both non-experts, developers, scientists and others can understand it.

Each documentation file starts with a title. The title explains as short as possible what the file explains.  
Under the title we have the written by part. This is so that people can contact you if something is not clear. Using git, you can have a more detailed history of the file, but the author serves as the responsible of rhtis part of the documentation.

Underneath follow the sections:

1. Why/ goal: why is this part needed in the project, how is it relevant...
2. What/ details: explain it in detail, this is more of an abstract part where you focus on the mathematics/ science rather on how you made it in the project
3. How/ implementation: here you explain your implementation, try to reason with the author why you did certain actions or used certain packages/ technologies. Make sure to use links and citations.
4. Results: what is the result of your implementation. This could be a graph, video, picture. This is particularly important for data-team.
5. Sources: where can people find more info on the discussed topic.

## How to markdown

Since all the documentation will be written in markdown, I have added some information on how this works. As always, the internet is you greatest source, so if you don't know something you can always find it there.

According to wikipedia, [markdown](https://en.wikipedia.org/wiki/Markdown) is a lightweitght markup language for creating formatted text using a plain-text editor. This allows for it to be written on any computer, without special tools and programs. In github, which we will be using to host our documentation, markdown is formatted to look nice and easier to read.

To write markdown, you can use any editor. For a titles and headings, use `#` with the number indicating the level. Ordered lists can be created using `1.`. Lastly links can be added using `[text](link)`. More details can be found on the [markdown guide page](https://www.markdownguide.org/). As always there are extensions in VS Code to help you with development. For a preview, use [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced).

To include a diagram in markdown, I recommend using [mermaid](https://mermaid-js.github.io/mermaid/#/). With relatively easy syntax, diagrams can be created. It's also included in [github](https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/). To have your diagrams included in the preview, there is an [extension](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) in VS Code.
