# Structure

Written by: Samuel Berton

## Documentation guidelines

In the documentation, we keep a similar structure so that it is both easy to write and read.  
The goal of the documentation is the following:

1. Show the workings of the technology,
2. Explain the reasoning behind each of the implementations,
3. Allow expanding on the current project,
4. Be a scientific explanation of our project.

Thus, the documentation has to reflect these basic principles, and it should therefore be written so that non-experts, developers, scientists and others can understand it.

Each documentation file starts with a title. The title explains as shortly as possible what the file explains.  
Under the title, we have the written-by part, where people can contact the author if something needs to be clarified. Git provides a more detailed history of the file, but the author serves as responsible for this part of the documentation.

Underneath follow the sections:

1. Why/ goal: why is this part needed in the project, and how is it relevant?
2. What/ details: explain the subject in detail, which is more of an abstract part where the focus is on mathematics/ science instead of how the project is done. 
3. How/ implementation: here, the implementation is explained—why specific actions or packages/technologies have been used, using links and citations.
4. Results: what is the result of the implementation? This result could be a graph, video, or picture, which is particularly important for data team.
5. Sources: where can people find more info on the discussed topic?

## How to markdown

Since all the documentation is written in markdown,

information is added on how markdown works. The internet is the greatest source of knowledge, so if you do not know something, you can always find it there.

According to Wikipedia, [markdown](https://en.wikipedia.org/wiki/Markdown) is a lightweight markup language for creating formatted text using a plain-text editor. This editor allows it to be written on any computer without special tools and programs. In GitHub, which we will use to host our documentation, markdown is formatted to look nice and easier to read.

To write markdowns, any editor can be used. For titles and headings, use `#` with the number indicating the level. Ordered lists can be created using `1.`. Lastly, links can be added using `[text](link)`. More details can be found on the [markdown guide page](https://www.markdownguide.org/). As always, there are extensions in VS Code to help with development. For a preview, use [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced).

To include a diagram in markdown, it is recommended to use [mermaid](https://mermaid-js.github.io/mermaid/#/). With relatively easy syntax, diagrams can be created. It is also included in [github](https://github.blog/2022-02-14-include-diagrams-markdown-files-mermaid/). To have your diagrams included in the preview, there is an [extension](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid) in VS Code.