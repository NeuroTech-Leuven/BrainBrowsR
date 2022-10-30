# Stimuli

Written by: Wout Van Droogenbroeck

## Goal

For SSVEP we need stimuli flickering at different frequencies inserted in the web page. We want the stimuli to be easy to adjust, that means changing the size, color, position, frequency etc. according to our needs.

## Details

Images on a website are defined as html elements as explained in [the parsing section](./parsing.md). So in order to display the stimuli using the extension, we have to insert them as html elements. The flickering effect can easily be added using CSS Animation that changes the opacity of the element at a certain rate.

## Implementation

In the [content script](../../src/content_script.js), we create an html image element that we append to the body of the web page, using the insertStimuli function in the [stimuli_helper](../../src/helpers/stimuli_helper.js). The element is given a class name, that can be used to define its style in the [CSS file](../../src/css/stimuli.css). It is possible to add multiple classes to elements, so they all share one class that defines the flickering animation (the simuli class below) but some variables are changed in their unique class.

<img src="./images/stimuli_class.png" width="400"/>

Each stimulus thus also has its own class, so their position, color and frequency can be different as shown here for the like class:

<img src="./images/like_class.png" width="250"/>


In the CSS file, we also define size, color, position etc. for each class, this way all the important properties can be altered in one place by changing just a few variables. The flickering animation is defined using a simple keyframe that sets the opacity to 1 at the start, 0 at the middle and back to 1 at the end. To choose a frequency, one can just set the duration of the animation.

## Results

We can succesfully insert our stimuli on the web page. The stimuli are easy to change by editing 1 CSS file.

<img src="./images/stimuli_result.png" width="500"/>
