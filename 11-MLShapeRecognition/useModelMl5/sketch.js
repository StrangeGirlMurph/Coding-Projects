let shapeClassifier;
let canvas;
let resultsDiv;
let inputImage;
let clearButton;

function setup() {
	canvas = createCanvas(400, 400);
	pixelDensity(1);
	background(255);

	inputImage = createGraphics(64, 64);
	resultsDiv = createDiv('loading model...');

	clearButton = createButton('clear');
	clearButton.mousePressed(function () {
		background(255);
	});

	let options = {
		inputs: [64, 64, 4],
		task: 'imageClassification'
	};

	shapeClassifier = ml5.neuralNetwork(options);

	const modelDetails = {
		model: '../model/model.json',
		metadata: '../model/model_meta.json',
		weights: '../model/model.weights.bin'
	};

	shapeClassifier.load(modelDetails, modelLoaded);
}

function draw() {
	if (mouseIsPressed) {
		strokeWeight(8);
		line(mouseX, mouseY, pmouseX, pmouseY);
	}
}

function modelLoaded() {
	console.log('model ready!');
	classifyImage();
}

function classifyImage() {
	inputImage.copy(canvas, 0, 0, 400, 400, 0, 0, 64, 64);

	//image(inputImage, 0, 0);
	shapeClassifier.classify({ image: inputImage }, gotResults);
}

function gotResults(err, results) {
	if (err) {
		console.error(err);
		return;
	}

	let label = results[0].label;
	let confidence = nf(Math.floor(100 * results[0].confidence), 2, 0);

	resultsDiv.html(`${label} ${confidence}%`);

	//console.log(results);
	classifyImage();
}

