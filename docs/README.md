# Documentation

[Return to the mainpage](../README.md)

This is the developer documentation for the BrainBrowsR project by NeuroTech Leuven. The project consists of two main parts, a back-end and and a front-end. These are then connected through [websockets](websockets.md). The global structure that connects everything can be found in the following diagram.

```mermaid
    flowchart TD;
        subgraph BrainBrowsR
        subgraph Frontend
        subgraph On start
        Start[Start the browser extension]-->pre[Preprocess html and insert stimuli]
        pre-->init[set current_post to first post in DOM]
        init-->connect[start websocket connection]
        end
        subgraph Parse and wait
        connect--> process[process the current post]
        process-->wait
        wait[wait for message] --no message--> wait
        end
        subgraph websocket action
        wait--message received-->decision{Received message}
        decision--next-->next(parse the next post)
        decision--previous-->previous(parse the previous post)
        decision--like-->like(like the post)
        end
        next-->process
        previous-->process
        like -->wait
        end
        subgraph Backend
        subgraph On Start
        BrainServR[Create an instance of BrainServR]
        BrainServR-->Headset[Connect with the headset]
        Headset-->Websockets[Starts the WebSockets server]
        Websockets--waiting for connect-->Websockets
        Websockets--extension connects-->XTConnect

        connect-->XTConnect[Extension Connects]

        end
        subgraph Data-processing
        XTConnect-->SDP[Start data-processing]
        SDP-->Gather[Get data from the headset]
        Gather-->prep[Preprocess the data]
        prep-->classify[Classify the data]
        classify-->thresh{Certainty higher than threshold?}
        thresh --yes--> send[Send message through websockets]
        send--label/action-->wait
        send--start over-->prep
        thresh--no--> prep

        end
        end
        end

    style Start fill:#26bf24
```

## Back-end

The back-end of BrainBrowR consists of two parts, the websockets server and the data-processing pipeline. The backend is written in Python is invisible to the user of the application. It collects the data from the headset, applies data-processing to it and sends the result to the extension through websockets. To learn more about websockets, go to the documentation in [this document](websockets.md). To learn more about the data-processing pipeline, go to the documentation [here](data_processing.md).

## Front-end

The front-end is the extension. The front-end is written in JavaScript and with Firefox in mind as the browser. Firefox has created some useful tools to make development of the extension easier. However it should be easy to extend the extension to Chromium base browsers. To learn more about the extension, see [here](extension.md)

The extension does three main things, first it inserts the stimuli in the webpage, the methodology for this is written [here](extension/stimuli.md). These stimuli will excite the brain so that the dataprocessing pipeline will detect that the user is looking at a certain stimulus. The extension will then respond appropriately by parsing the right post, described [here](extension/parsing.md) and then [processing this](extension/processing_posts.md).

[Return to the mainpage](../README.md)
