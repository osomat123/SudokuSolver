const submitButton = document.querySelector("#submit");
const imageInput = document.querySelector("#image_input");
const imageDiv = document.querySelector(".image");
const solutionDiv = document.querySelector(".solution");
var response_data;

function bigSad() {
    if(solutionDiv.firstChild !== null)
        solutionDiv.removeChild(solutionDiv.firstChild);

    let sad_image = document.createElement("img");
    sad_image.src = sad_url;
    sad_image.style.height = "80%";
    sad_image.style.width = "80%";
    solutionDiv.append(sad_image)
}

function showImage() {
    let fr = new FileReader();
    fr.readAsDataURL(imageInput.files[0]);

    if(imageDiv.firstChild !== null)
        imageDiv.removeChild(imageDiv.firstChild);
    
    let img = document.createElement("img");
    fr.onload = function(e) { img.src = this.result; }
    img.class = "original";
    img.style.height = "80%";
    img.style.width = "80%";
    imageDiv.append(img)

    if(solutionDiv.firstChild !== null)
        solutionDiv.removeChild(solutionDiv.firstChild);

    let gif = document.createElement("img");
    gif.src = gif_url;
    solutionDiv.append(gif)

    document.querySelector(".input").style.marginTop = '30px';
}

function drawGrid(length){
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');

    ctx.lineWidth = 6;
    ctx.strokeRect(0, 0, length, length);
    let stepSize = length / 9;
  
    let i;
  
    for(i = 1; i<9; i++){
      
      if(i % 3 == 0){
        ctx.lineWidth = 3;
      }
      else {
        ctx.lineWidth = 1;
      }
  
      ctx.beginPath();
      ctx.moveTo((stepSize*i), 0);
      ctx.lineTo((stepSize*i), length);
      ctx.stroke();
    }
  
    for(i = 1; i<9; i++){
      if(i % 3 == 0){
        ctx.lineWidth = 3;
      }
      else {
        ctx.lineWidth = 1;
      }
  
      ctx.beginPath();
      ctx.moveTo(0, (stepSize*i));
      ctx.lineTo(length, (stepSize*i));
      ctx.stroke();
    }
  }
  
  function fillNumbers(solvedGrid, originalGrid, length) {
    let i, j, num;
    let boxSize = length / 9;
    let offsetX = boxSize / 2.7;
    let offsetY = boxSize / 1.5;

    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');
    
    for(i=0; i<solvedGrid.length; i++){
      num = solvedGrid[i];
      stepX = i % 9;
      stepY = parseInt(i / 9);
      startX = boxSize * stepX + offsetX;
      startY = boxSize * stepY + offsetY;
      
      if(originalGrid[i] != 0){
          ctx.fillStyle = "#0072e3";
          ctx.font = `${boxSize / 1.8}px Courier New bold`;
      }
      else {
        ctx.fillStyle = "black";
        ctx.font = `${boxSize / 1.8}px Courier New`;
      }

      //ctx.font = `${boxSize / 1.8}px Courier New`;
      ctx.fillText(num, startX, startY);
    }
  }

function showSolution(data) {
    let originalGrid = data.original.split("");
    let solvedGrid = data.solved.split("");


    if(solutionDiv.firstChild !== null)
        solutionDiv.removeChild(solutionDiv.firstChild);

    let canvas = document.createElement("canvas")
    canvas.id = "canvas";
    canvas.width = 400;
    canvas.height = 400;
    solutionDiv.append(canvas);
    drawGrid(canvas.width);
    fillNumbers(solvedGrid, originalGrid, canvas.width);
}

function submitImage() {
    let files = imageInput.files;
    let formData = new FormData();

    if(files.length == 0){
        alert("No File Selected");
        return null;
    }

    var ext = files[0].name.split('.').pop()
    formData.append('sudoku_image',files[0]);
    formData.append('ext',ext);

    let url = "/";
    fetch(url, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Recived Data!!");
        response_data = data;
        if(data.success == 0){
            bigSad();
        }
        else {
            showSolution(data);
        }
    })
    .catch(error => {
        console.log(error);
        bigSad();
    }); 
}


function doStuff(){
    showImage();
    submitImage();
}

submitButton.addEventListener('click', doStuff);