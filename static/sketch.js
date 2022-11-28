let inputFile;
let img;
let button;
let capture;
let printed = 0;
let canvas;

function setup() {
    canvas = createCanvas(600, 500);
    inputFile = createFileInput(handleFile);
    inputFile.position(50, (windowHeight/2));
    button = createButton('Capture Video');
    button.position(50,  (windowHeight/2) + 80);
    button.mousePressed(startCapture);

    capture = createCapture(VIDEO);
    capture.size(600, 500);
    capture.hide();
}

function draw() {
    if (img) {
        clear();
        image(img, 0, 0, 600, 500);
    }
}

function handleFile(file) {
    print(file);
    if (file.type === 'image') {
        sendCanvas(file.data);
    } else {
        img = null;
    }
}

function startCapture() {
    clear();
    resizeCanvas(600, 500);
    img = null;
    image(capture, 0, 0);
}

async function sendCanvas(image64) {
    const data = { image64 }
    const options = {
        method: 'POST',
        headers: {
           'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    };

    const response = await fetch('/', options);
    const json = await response.json();
    img = createImg(json.image64, '');
    img.hide();
}