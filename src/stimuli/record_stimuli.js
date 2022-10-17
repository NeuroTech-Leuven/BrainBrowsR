
// giveSignal(document.getElementsByClassName("like")[0])
startExperiment();
function giveSignal(element) { 
    element.style.backgroundColor = "red"; 
}
function stopSignal(element) {
    element.style.backgroundColor = "black"; 
}

async function startExperiment() {
    var wait_time = 4000;
    await sleep(wait_time);
    giveSignal(document.getElementsByClassName("like")[0]);
    await sleep(wait_time);
    stopSignal(document.getElementsByClassName("like")[0]);
    await sleep(wait_time);
    giveSignal(document.getElementsByClassName("comment")[0]);
    await sleep(wait_time);
    stopSignal(document.getElementsByClassName("comment")[0]);
    await sleep(wait_time);
    giveSignal(document.getElementsByClassName("up")[0]);
    await sleep(wait_time);
    stopSignal(document.getElementsByClassName("up")[0]);
    await sleep(wait_time);
    giveSignal(document.getElementsByClassName("down")[0]);
    await sleep(wait_time);
    stopSignal(document.getElementsByClassName("down")[0]);
}



function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}