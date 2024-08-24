const players = [
    {id: 1, x: 50, y: 50},
    {id: 2, x: 150, y: 120},
    {id: 3, x: 250, y: 180},
];

width = 300;
height = 300;

// adjust the data values to the size of the map
const xScale = d3.scaleLinear().domain([-4831, 300]) .range([0, width]);
const yScale = d3.scaleLinear().domain([0, 300]) .range([0, height]);

const svg = d3.select("#minimap");

const playerCircles = svg.selectAll(".player")
    .data(players)
    .enter().append("circle")
    .attr("class", "player")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5);

const gameUpdates = [
    [
        {id: 1, x: 60, y: 70},
        {id: 2, x: 170, y: 130},
        {id: 3, x: 230, y: 220},
    ],
    [
        {id: 1, x: 80, y: 90},
        {id: 2, x: 180, y: 140},
        {id: 3, x: 210, y: 240},
    ],
    [
        {id: 1, x: 100, y: 110},
        {id: 2, x: 190, y: 150},
        {id: 3, x: 190, y: 260},
    ],
    [
        {id: 1, x: 110, y: 100},
        {id: 2, x: 190, y: 145},
        {id: 3, x: 210, y: 270},
    ],

];

function updatePlayerPositions(newData) {
    playerCircles.data(newData)
        .transition()
        .duration(500)
        .attr("cx", d => xScale(d.x))
        .attr("cy", d => yScale(d.y));
}

let currentIndex = 0;
function animateUpdates() {
    if (currentIndex < gameUpdates.length) {
        updatePlayerPositions(gameUpdates[currentIndex]);
        currentIndex++;
        setTimeout(animateUpdates, 1000); 
    }
}

animateUpdates();