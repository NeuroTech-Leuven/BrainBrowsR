# Software stack

## Goal

The software stack has to connect all the parts together and make sure that the detected SSVEP response has an outside effect.

## Implementation

In the following part a diagram is given to discuss the implementation of the software stack.

```mermaid
    flowchart TD;
        subgraph On start
        Start[Start the browser extension]-->pre[Preprocess html]
        pre-->init[set current_post = 0]
        init-->connect[start websocket connection]
        end
        subgraph Parse and wait
        connect-->parse[Parse the current_post]
        parse --> process[process the post]
        process-->wait
        wait[wait for message] --no message--> wait
        end
        subgraph websocket action
        wait--message received-->decision{Received message}
        decision--next-->next(increase current_post by 1)
        decision--previous-->previous(decrease current_post by 1)
        decision--like-->like(like the post)
        end
        next-->parse
        previous-->parse
        like -->wait

    style Start fill:#26bf24
    click connect href "./websockets.md"

```
