# Project-22

This is the project code of NeuroTechLeuven's BrainBrowsR.

Soon, you can find a full description on our website [website](https://ntxl.org) of the project as well as our final product video.

## Repo structure

The [docs](./docs/) folder contains the entire explanation on how the project works. This documentation is written primarily with other developers and researchers in mind.

The icons folder, contains the PNG that are use for the stimuli in BrainBrowsR.

The src folder contains the extension code, this is organised in 5 folders:

1. css, containing the css files needed in the extension,
2. data_processing, which contains all methods used to perform the data_processing pipeline,
3. helpers, files that are used by the content_script.js to perform certain actions,
4. html, the html code needed by the extension
5. stimuli, some helper functions related to stimuli.

The server.py is the back-end code, that connects the headset and does the data-processing.

The manifest.json is the configuraton file for the extension. To learn more about this, you can read this [page](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json) by Mozilla.

## Installation & Usage

There are two components to the project, a data-processing part that connects with the EEG-headset, coded in Python, and the software part written in JavaScript.

To run the Python code, first go to the right directory command and install with pip: `pip install -r requirements.txt`. This will install all the necessary packages and their dependencies. Please check that your Python version is higher than 3.5. In the terminal, now run the local data-processing server using `python server.py`. This will first connect with the headset and then start a websocket server.

To set-up the headset and connect with it, read our [headset guide](docs/headset.md).

Once the server has initiated, you can start using the extension. At the moment, we are looking to make it possible to install the extension from Mozilla. Until then, you can use either web-ext or developer tools to run it.

The instructions to install web-ext are found on [this webpage](https://extensionworkshop.com/documentation/develop/getting-started-with-web-ext/) by Mozilla. To run, simply do `web-ext run`. Going to instagram and login in, will connect you to websocket server and allow the usage of the extension.

The other option is temporarily installing it, using [these instructions](https://extensionworkshop.com/documentation/develop/temporary-installation-in-firefox/) and proceeding similar as with web-ext.

## Further development

If you wish to use this repo as a basis for your project, we recommend you install web-ext, by Mozilla. This tool makes it a picnic to develop webextensions.
