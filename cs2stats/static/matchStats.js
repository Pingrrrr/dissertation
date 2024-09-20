const bombplantData = {
    "name": "bomb plants",
    "children":[{
    "name": "NAVI",
    "children": [
    {
        "name": "A site",
        "children": [
            { "name": "Detonated", "size": 2 },
            { "name": "Defused", "size": 1 }
        ]
    },
    {
        "name": "B site",
        "children": [
            { "name": "Detonated", "size": 2 },
            { "name": "Defused", "size": 0 }
        ]
    }
]
},{
    "name": "EF",
    "children": [
    {
        "name": "A site",
        "children": [
            { "name": "Detonated", "size": 2 },
            { "name": "Defused", "size": 2 }
        ]
    },
    {
        "name": "B site",
        "children": [
            { "name": "Detonated", "size": 1 },
            { "name": "Defused", "size": 1 }
        ]
    }
]
}
]

};



const roundData = {
    "name":"Rounds Won",
    "children":[{
        "name": "NAVI",
        "children":[
            {"name":"T","size":12},
            {"name":"CT","size":10}
        ]
    },{
        "name": "EF",
        "children":[
            {"name":"T","size":10},
            {"name":"CT","size":10}
        ]
    }
]
}

const killsData = {
    "name":"Kills",
    "children":[{
        "name": "NAVI",
        "children":[
            {"name":"T","size":28},
            {"name":"CT","size":38}
        ]
    },{
        "name": "EF",
        "children":[
            {"name":"T","size":23},
            {"name":"CT","size":11}
        ]
    }
]

}

bombsChart = chart = Sunburst(bombplantData, {
    value: d => d.size,
    label: (d,n) => d.name + " ("+n.sum(d => d.size).value+")", 
    width: 400,
    height: 400,
    color: ["blue","red"]
  });
  
  document.getElementById("bombplants").appendChild(bombsChart);

roundsChart = chart = Sunburst(roundData, {
    value: d => d.size,
    label: (d,n) => d.name + " ("+n.sum(d => d.size).value+")", 
    width: 400,
    height: 400,
    color: ["green","red"]
  });
  
  document.getElementById("rounds").appendChild(roundsChart);

killsChart = chart = Sunburst(killsData, {
    value: d => d.size,
    label: (d,n) => d.name + " ("+n.sum(d => d.size).value+")", 
    width: 400,
    height: 400,
    color: ["red","yellow"]
  });

  d3.json("./kills")
    .then(function (data) {

        killsChart = chart = Sunburst(data, {
            value: d => d.size,
            label: (d,n) => d.name + " ("+n.sum(d => d.size).value+")", 
            width: 400,
            height: 400,
            color: ["red","yellow"]
          });

          document.getElementById("kills").appendChild(killsChart);


    });
  
  