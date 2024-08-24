var players = [];
var gameUpdates = [];

width = 600;
height = 600;

// adjust the data values to the size of the map
// overpass
//X -3959.9727 - -99.10431
//Y -3474.6633 - 1624.767

const xScale = d3.scaleLinear().domain([-3959.9727, -99.10431]).range([0, width]);
const yScale = d3.scaleLinear().domain([-3474.6633, 1624.767]).range([0, height]);

d3.json("round")
    .then(function (data) {
        const players = data.playerPositions[0]
        const gameUpdates = data.playerPositions
        const totalUpdates = data.playerPositions.length

        const svg = d3.select("#minimap");

        const progressBar = document.getElementById("progressBar");
        const isClicked = false;
        

        const playerEnters =  svg.selectAll(".player")
            .data(players, d => d.steamid)
            .enter().append("g")
            .attr("transform", d => {
                return "translate(" + xScale(d.X)+","+ yScale(d.Y) + ")" ;
            });

        const playerCircles = playerEnters.append("circle")
            .attr("class", "player")
            .attr("r", 5)
            .attr("fill", d => d.team_name=="CT" ? "blue" : "yellow");

        const playerNames = playerEnters.append("text")
            .attr("dx", -20)
            .attr("dy", -10)
            .text(d => d.name);


        function updatePlayerPositions(newData) {
            playerEnters.data(newData, d => d.steamid)
                .attr("transform", function(d) {
                    return "translate(" + xScale(d.X)+","+ yScale(d.Y) + ")";
                });
            console.log(newData[0].X)
            console.log(newData[0].Y)
        }

        let currentIndex = 0;
        function animateUpdates(index) {
            
            if (index < gameUpdates.length) {
                currentIndex = index
                updatePlayerPositions(gameUpdates[currentIndex]);
                if(!isClicked){
                    progressBar.value = Math.round((currentIndex/totalUpdates)*100)
                }
                
                currentIndex++;
                setTimeout(animateNextUpdate, 250);
            }
        }

        function animateNextUpdate(){
            animateUpdates(currentIndex)
        }

        animateUpdates(0);



        progressBar.addEventListener("mousedown", function(){

            //dont update the slider whiule  were clicking it
            isClicked = true;

        });
        progressBar.addEventListener("mouseup", function() {
            progress = this.value;
            currentFrame = Math.round((progress / 100) * totalUpdates);
            animateNextUpdate(currentFrame);
            isClicked = false;
        });

    });
