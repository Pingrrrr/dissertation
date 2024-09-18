var players = [];
var gameUpdates = [];

width = 800;
height = 800;

// adjust the data values to the size of the map
// overpass - values from awpy https://github.com/pnxenopoulos/awpy/blob/main/awpy/data/map_data.py
//"pos_x": -4831,
//"pos_y": 1781,
//"scale": 5.2,

//scale is used to put player co-ordinates on 1024X1024 images in awpy
// so we can just use the scale * 1024 to find out width and length of the maps
let maps={
    "de_overpass" : {
        "pos_x": -4831,
        "pos_y": 1781,
        "scale": 5.2,
    },
    "de_nuke": {
        "pos_x": -3453,
        "pos_y": 2887,
        "scale": 7,
    },

    "de_vertigo": {
        "pos_x": -3168,
        "pos_y": 1762,
        "scale": 4,
    },

    "de_ancient": {
        "pos_x": -2953,
        "pos_y": 2164,
        "scale": 5,
    },
    "de_anubis": {
        "pos_x": -2796,
        "pos_y": 3328,
        "scale": 5.22,
    },
    "de_dust": {
        "pos_x": -2850,
        "pos_y": 4073,
        "scale": 6,
    },
    "de_dust2": {
        "pos_x": -2476,
        "pos_y": 3239,
        "scale": 4.4,
    },
    "de_inferno": {
        "pos_x": -2087,
        "pos_y": 3870,
        "scale": 4.9,
    },
    "de_inferno_s2": {
        "pos_x": -2087,
        "pos_y": 3870,
        "scale": 4.9,
    },
    "de_mirage": {
        "pos_x": -3230,
        "pos_y": 1713,
        "scale": 5,
    }
    
}


const mapWidth = 1024 * maps[map].scale;
const xScale = d3.scaleLinear().domain([maps[map].pos_x, (maps[map].pos_x + mapWidth)]).range([0, width]);
const yScale = d3.scaleLinear().domain([maps[map].pos_y, (maps[map].pos_y - mapWidth)]).range([0, height]);

const kills = d3.json("../kills/" + round_id);


//['smoke', 'flashbang', 'molotov', 'he_grenade', 'incendiary_grenade']
let grenadeColours = new Map();
grenadeColours.set('smoke','gray');
grenadeColours.set('flashbang','white');
grenadeColours.set('molotov','orange');
grenadeColours.set('he_grenade','red');
grenadeColours.set('incendiary_grenade','orange');




console.log('Round ID ' + round_id);



function loadStrategy(canvas, url){
    fetch(url, {
        method: 'GET'
    })
        .then(response => {
            return response.json();
        })
        .then(json => {
            console.log(json)
            canvas.loadFromJSON(json);
            canvas.setBackgroundImage(null);
            canvas.setBackgroundColor('');
            ctx = canvas.getContext("2d");
            ctx.clearRect(0, 0, 800, 800);

            canvas.renderAll();
        });
};


stratButtons = document.querySelectorAll('.strategy-btn');
var canvas = new fabric.Canvas('map-canvas', { preserveObjectStacking: true });
stratButtons.forEach(button => {
    button.addEventListener('click', function (event) {

        var url = '/strategy/'+this.value+'/canvas'
        loadStrategy(canvas, url);



    });
});

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
loadMap(canvas, 'maps/'+map)


d3.json("../ticks/" + round_id)
    .then(function (data) {
        console.log(data.playerPositions.length-1)
        const firstTick = data.playerPositions[0][0].tick
        const lastTick = data.playerPositions[data.playerPositions.length-1][0].tick
        const players = data.playerPositions[0]
        const grenades = data.grenades
        const weaponFires = data.weaponFires
        const gameUpdates = data.playerPositions
        const totalUpdates = data.playerPositions.length

        const svg = d3.select("#minimap");


        const progressBar = document.getElementById("progressBar");
        
        let isClicked = false;
        let playing = false;


        const playerEnters = svg.selectAll(".player")
            .data(players, d => d.steamid)
            .enter().append("g")
            .attr("transform", d => {
                return "translate(" + xScale(d.X) + "," + yScale(d.Y) + ")";
            });

        //https://d3-graph-gallery.com/graph/shape.html
        const playerCircles = playerEnters.append("circle")
            .attr("class", "player")
            .attr("r", 7)
            .attr("fill", d => d.health < 1 ? "red" : d.team_name == "CT" ? "blue" : "yellow");

        const playerNames = playerEnters.append("text")
            .attr("dx", -20)
            .attr("dy", -10)
            .text(d => d.name);

        const healthBarOutline = playerEnters.append("rect")
            .attr("x", -15)
            .attr("y", 6)
            .attr('width', 30)
            .attr('height', 5)
            .attr('stroke', 'black');

        const healthBarFill = playerEnters.append("rect")
            .attr("x", -15)
            .attr("y", 6)
            .attr('width', 30)
            .attr('height', 5)
            .attr('fill', 'green');

        const playerAim = playerEnters.append("path")
            .attr("d", d3.arc()
                .innerRadius(0)
                .outerRadius(7)
                .startAngle(-0.5)
                .endAngle(0.5)
            )
            .attr('stroke', 'black')
            .attr('fill', 'white');


        function updatePlayerPositions(newData) {
            playerEnters.data(newData, d => d.steamid)
                .attr("transform", function (d) {
                    return "translate(" + xScale(d.X) + "," + yScale(d.Y) + ")";
                });

        }

        function animatePlayerPositions(newData) {

            //https://www.codecademy.com/resources/docs/d3/interactivity/ease
            playerEnters.data(newData, d => d.steamid).transition()
                .duration(250)
                .ease(d3.easeLinear)
                .attr("transform", function (d) {
                    return "translate(" + xScale(d.X) + "," + yScale(d.Y) + ")";
                });

            playerCircles.data(newData, d => d.steamid)
                .attr("fill", d => d.health < 1 ? "gray" : d.team_name == "CT" ? "blue" : "yellow");

            healthBarFill.data(newData, d => d.steamid)
                .attr('width', d => ((d.health / 100) * 30))

            playerAim.data(newData, d => d.steamid).transition()
                .duration(250)
                .ease(d3.easeLinear)
                .attr('transform', d => "rotate(" + -d.yaw + ")");

        }

        function animateGrenades(newData) {

            grenadeSvgs = svg.selectAll(".grenade")
                .data(newData, g => g.entity_id);

            grenadeSvgs.exit().remove();

            grenadeSvgs.enter()
                .append("circle")
                .attr("class", "grenade")
                .attr("r", 5)
                .attr("fill", g => grenadeColours.get(g.grenade_type))
                .attr("transform", g => {
                    return "translate(" + xScale(g.X) + "," + yScale(g.Y) + ")";
                });

            grenadeSvgs.transition()
                .duration(250)
                .ease(d3.easeLinear)
                .attr("transform", function (g) {
                    return "translate(" + xScale(g.X) + "," + yScale(g.Y) + ")";
                });

        }

        function animateWeaponFires(newData){

            newData.forEach(function (wf, index) {

                weaponFlashCircles = playerEnters.filter(d => d.steamid === wf.player_steamid)
                .append("circle")
                .attr("r", 10) 
                .attr("fill", "white")
                .attr("opacity",1);

                weaponFlashCircles.transition()
                .duration(500) 
                .ease(d3.easeLinear)
                .attr("opacity", 0) 
                .on("end", function() {
                    d3.select(this).remove();
                });
                
              });

        }


        let currentIndex = 0;
        function animateUpdates(index) {

            if (index < gameUpdates.length) {
                currentIndex = index
                currentTick = gameUpdates[currentIndex][0].tick;
                animatePlayerPositions(gameUpdates[currentIndex]);
                animateGrenades(grenades[currentIndex])
                animateWeaponFires(weaponFires[currentIndex])
                progressBar.value = Math.round((currentIndex / totalUpdates) * 100)
                currentIndex++;
                nextAnimation = setTimeout(animateNextUpdate, 250);
            }
        }

        function animateNextUpdate() {
            if (!isClicked && playing) {
                animateUpdates(currentIndex)
            }
        }

        playing=true
        animateUpdates(0);

        progressBar.addEventListener("mousedown", function () {
            //dont update the slider whiule  were clicking it
            isClicked = true;

        });
        progressBar.addEventListener("mouseup", function () {
            isClicked = false;
            progress = this.value;
            currentFrame = Math.round((progress / 100) * totalUpdates);
            clearTimeout(nextAnimation)
            updatePlayerPositions(currentFrame)
            setTimeout(animateUpdates(currentFrame), 250)

        });

        const playButton = document.getElementById('playButton');

        function pauseReplay(){
            playing=false;
            clearTimeout(nextAnimation)
        }

        function playReplay(){
            playing=true;
            animateNextUpdate();
        }

        // Toggle Play/Pause
        playButton.addEventListener('click', function() {
            if (!playing) {
                playReplay();
                playButton.textContent = 'Pause';
            } else {
                pauseReplay()
                playButton.textContent = 'Play ';
            }
        });

        const timestampComments = document.getElementsByClassName("timestampComment")
        console.log(timestampComments)

        for(comment of timestampComments){
            comment.addEventListener("click", function () {
                console.log("clicked! Value is "+this.id)
                tick = this.id;
                currentFrame = Math.round(((tick-firstTick)/(lastTick-firstTick)) * totalUpdates);
                console.log("moving to frame: "+currentFrame)
                clearTimeout(nextAnimation)
                updatePlayerPositions(currentFrame)
                setTimeout(animateUpdates(currentFrame), 250)
    
            });

        }

    });



