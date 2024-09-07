//https://stackoverflow.com/a/40030387
var canvas = new fabric.Canvas('map-canvas', { preserveObjectStacking:true });
const mapSelector = document.getElementById('map-selector');
const saveButton = document.getElementById('saveButton');

var currentMapImg;

function loadMap(mapName) {

    fabric.Image.fromURL(`/static/maps/${mapName}.png`, function(oImg) {
        if(currentMapImg){
            canvas.remove(currentMapImg);
        }
        oImg.set('selectable',false).set('erasable', false);
        oImg.scaleToHeight(800);
        oImg.scaleToWidth(800);
        canvas.add(oImg);
        oImg.sendToBack();
        currentMapImg = oImg;
    });
}

loadMap(mapSelector.value);
mapSelector.addEventListener('change', function() {
    loadMap(this.value);
});

saveButton.addEventListener('click', function(){
    // POST the strategy details to the server
})

const tools = document.querySelectorAll('.tool-icon');
canvas.freeDrawingBrush.width = 10;

tools.forEach(tool => {
    tool.addEventListener('click', function() {
        tools.forEach(t => t.classList.remove('active'));
        this.classList.add('active');

        switch(this.id){
            case "draw":
                canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
                canvas.freeDrawingBrush.width = 10;
                canvas.isDrawingMode = true;
                break;
            case "erase":
                canvas.freeDrawingBrush = new fabric.EraserBrush(canvas);
                canvas.freeDrawingBrush.width = 50;
                canvas.isDrawingMode = true;
                break;
            case "undo":
                canvas.freeDrawingBrush = new fabric.EraserBrush(canvas);
                canvas.freeDrawingBrush.width = 50;
                canvas.freeDrawingBrush.inverted = true;
                canvas.isDrawingMode = true;
                break;


            case "select":
                canvas.isDrawingMode = false;
                break;

        }
    });
});

var rect = new fabric.Rect({
    left: 100,
    top: 100,
    fill: 'red',
    width: 20,
    height: 20,
    erasable: false
})

canvas.add(rect)
rect.bringToFront();

