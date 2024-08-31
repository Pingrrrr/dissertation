var players = [];
var gameUpdates = [];

width = 600;
height = 600;

// adjust the data values to the size of the map
// overpass - values from awpy https://github.com/pnxenopoulos/awpy/blob/main/awpy/data/map_data.py
//"pos_x": -4831,
//"pos_y": 1781,
//"scale": 5.2,

//scale is used to put player co-ordinates on 1024X1024 images in awpy
// so we can just use the scale * 1024 to find out width and length of the maps

const mapWidth = 1024 * 5.2
const xScale = d3.scaleLinear().domain([-4831, (-4831 + mapWidth)]).range([0, width]);
const yScale = d3.scaleLinear().domain([1781, (1781 - mapWidth)]).range([0, height]);

console.log('Round ID '+ round_id );

d3.json("../ticks/"+round_id)
    .then(function (data) {
        const players = data.playerPositions[0]
        const gameUpdates = data.playerPositions
        const totalUpdates = data.playerPositions.length

        const svg = d3.select("#minimap");

        const progressBar = document.getElementById("progressBar");
        let isClicked = false;
        

        const playerEnters =  svg.selectAll(".player")
            .data(players, d => d.steamid)
            .enter().append("g")
            .attr("transform", d => {
                return "translate(" + xScale(d.X)+","+ yScale(d.Y) + ")" ;
            });

        //https://d3-graph-gallery.com/graph/shape.html
        const playerCircles = playerEnters.append("circle")
            .attr("class", "player")
            .attr("r", 5)
            .attr("fill", d => d.health <1 ? "red" :d.team_name=="CT" ? "blue" : "yellow");

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
              .outerRadius(5)
              .startAngle(-0.5)
              .endAngle(0.5)
              )
            .attr('stroke', 'black')
            .attr('fill', 'white');
            

        function updatePlayerPositions(newData){
            playerEnters.data(newData, d => d.steamid)
            .attr("transform", function(d) {
                return "translate(" + xScale(d.X)+","+ yScale(d.Y) + ")";
            });

        }


        function animatePlayerPositions(newData) {

            //https://www.codecademy.com/resources/docs/d3/interactivity/ease
            playerEnters.data(newData, d => d.steamid).transition()
                .duration(250)
                .ease(d3.easeLinear)
                .attr("transform", function(d) {
                    return "translate(" + xScale(d.X)+","+ yScale(d.Y) + ")";
                });
            
            playerCircles.data(newData, d => d.steamid)
                .attr("fill", d => d.health <1 ? "gray" :d.team_name=="CT" ? "blue" : "yellow");
            
            healthBarFill.data(newData, d => d.steamid)
                .attr('width', d => ((d.health/100)*30))

            playerAim.data(newData, d => d.steamid).transition()
            .duration(250)
            .ease(d3.easeLinear)
                .attr('transform', d => "rotate("+-d.yaw+")");

        }

        let currentIndex = 0;
        function animateUpdates(index) {
            
            if (index < gameUpdates.length) {
                currentIndex = index
                animatePlayerPositions(gameUpdates[currentIndex]);
                    progressBar.value = Math.round((currentIndex/totalUpdates)*100)
                currentIndex++;
                nextAnimation = setTimeout(animateNextUpdate, 250);
            }
        }

        function animateNextUpdate(){
            if(!isClicked){
                animateUpdates(currentIndex)
            }
        }

        animateUpdates(0);

        progressBar.addEventListener("mousedown", function(){
            //dont update the slider whiule  were clicking it
            isClicked = true;

        });
        progressBar.addEventListener("mouseup", function() {
            isClicked = false;
            progress = this.value;
            currentFrame = Math.round((progress / 100) * totalUpdates);
            clearTimeout(nextAnimation)
            updatePlayerPositions(currentFrame)
            setTimeout(animateUpdates(currentFrame), 250)
            
        });

    });
