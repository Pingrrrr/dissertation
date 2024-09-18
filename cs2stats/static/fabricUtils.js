
var currentMap = "de_dust2"
var currentMapImg;

function setMap(canvas, oImg) {
    if (currentMapImg) {
        canvas.remove(currentMapImg);
    }
    oImg.set('selectable', false).set('erasable', false);
    oImg.scaleToHeight(800);
    oImg.scaleToWidth(800);
    canvas.setBackgroundImage(oImg, canvas.renderAll.bind(canvas));
    currentMapImg = oImg;
}

function loadMap(canvas, mapName) {

    fabric.Image.fromURL(`/static/maps/${mapName}.png`, function (oImg) {
        setMap(canvas, oImg)
    });
    currentMap = mapName;
}

function loadStrategy(canvas, url, callback){
    fetch(url, {
        method: 'GET'
    })
        .then(response => {
            return response.json();
        })
        .then(json => {
            console.log(json)
            canvas.loadFromJSON(json, callback)

        });
};