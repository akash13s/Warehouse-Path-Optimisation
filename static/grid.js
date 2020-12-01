var form = document.getElementById('selectionForm');

form.addEventListener('submit', getFun);

var submitBtn = document.getElementById('submitBtn');

submitBtn.addEventListener('submit', getPath);

var input = document.getElementById('warehouseID');

// var wID = input.value;


var mySet = new Set();
var inputSet = new Set();
var inputSetSource = new Set();
var outputSet = new Set();
var myPath = new Set();
var inputX, inputY;

function getFun(e) {
    e.preventDefault();
    getRequest(input.value);
    document.getElementById('renderBtn').disabled = true;
    document.getElementById('finalBtn').hidden = false;
}

function getPath(e) {
    e.preventDefault();
    // console.log(e.target);
    makePostRequest(inputSet, inputSetSource);
    document.getElementById('finalBtn').disabled = true;
}

var HEIGHT = 35,
WIDTH = 35,
PADDING = 3;

var BLOCKED_CELL_COLOR = "lime",
  VALID_CELL_COLOR = "#101010",
  SOURCE_COLOR = "red",
  INTERMEDIATE_CELL_COLOR = "#CD853F",
  ITEM_COLOR = "blue";

function gridData(dimensionX, dimensionY, mySet) {
    // console.log(dimensionX, dimensionY);
    inputX = dimensionX;
    inputY = dimensionY;
    var my_Set = new Set(mySet);
    var data = new Array();
    var xpos = 1;
    var ypos = 1;
    var width = WIDTH;
    var height = HEIGHT;
    // if (input.value == 'large-warehouse') {
    //     width = 40;
    //     height = 40;
    // }
    var click = 0;
    var xx = 0;
    var yy = 0;
    var valid = 0;
    // console.log(my_Set);
    for (var row = 0; row < dimensionX; row++) {
        data.push(new Array());

        for (var column = 0; column < dimensionY; column++) {
            if (my_Set.has(`${row}_${column}`)) {
                data[row].push({
                    x: xpos,
                    y: ypos,
                    xCor: xx,
                    yCor: yy,
                    width: width,
                    height: height,
                    click: click,
                    valid: 1
                })
            } else {
                data[row].push({
                    x: xpos,
                    y: ypos,
                    xCor: xx,
                    yCor: yy,
                    width: width,
                    height: height,
                    click: click,
                    valid: 0
                })
            }
            xpos += width;
            yy++;
        }
        xpos = 1;
        ypos += height;
        yy = 0;
        xx++;
    }
    return data;
}

function printGrid(dimensionX, dimensionY, mySet) {

    // console.log(dimensionX, dimensionY);
    var gData = gridData(dimensionX, dimensionY, mySet);
    // console.log(gData);
    var grid = d3.select('#grid')
        .append("svg")
        .attr("width", dimensionY * WIDTH + 50 + "px")
        .attr("height", dimensionX * HEIGHT + 50 + "px")

    var row = grid.selectAll(".row")
        .data(gData)
        .enter()
        .append("g")
        .attr("class", "row");

    var column = row.selectAll(".square")
        .data(function(d) { return d; })
        .enter()
        .append("rect")
        .attr("class", "square")
        .attr("rx", 6)
        .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y; })
        .attr("width", function(d) { return d.width - PADDING; })
        .attr("height", function(d) { return d.height - PADDING; })
        .attr("class", function(d) {
            if (d.valid == 0)
                return "shelving-cell";
            else
                return "navigable-cell";
        })
        .style("stroke", "#222")
        .on('click', function(d) {
            if (d.valid == true) {
                d.click++;
                if ((d.click) % 3 == 0) {
                    d3.select(this).style("fill", VALID_CELL_COLOR);
                    if (inputSet.has(`${d.xCor}_${d.yCor}`)) {
                        inputSet.delete(`${d.xCor}_${d.yCor}`);
                    }
                    if (inputSetSource.has(`${d.xCor}_${d.yCor}`)) {
                        inputSetSource.delete(`${d.xCor}_${d.yCor}`);
                    }
                }
                if ((d.click) % 3 == 1) {
                    d3.select(this).style("fill", ITEM_COLOR);
                    inputSet.add(`${d.xCor}_${d.yCor}`);
                    if (inputSetSource.has(`${d.xCor}_${d.yCor}`)) {
                        inputSetSource.delete(`${d.xCor}_${d.yCor}`);
                    }
                }
                if ((d.click) % 3 == 2) {
                    if (inputSetSource.size == 0) {
                        d3.select(this).style("fill", SOURCE_COLOR);
                        inputSetSource.add(`${d.xCor}_${d.yCor}`);
                    } else {
                        d3.select(this).style("fill", VALID_CELL_COLOR);
                    }
                    if (inputSet.has(`${d.xCor}_${d.yCor}`)) {
                        inputSet.delete(`${d.xCor}_${d.yCor}`);
                    }
                }
            }
            // console.log(inputSet);
            // console.log(inputSetSource);
        });
}

function gridDataFinal(inputX, inputY, mySet, myPath, set1, set2) {

    console.log(myPath);
    console.log(mySet);
    var data1 = new Array();
    var xpos1 = 1;
    var ypos1 = 1;
    var width1 = WIDTH;
    var height1 = HEIGHT;
    // if (input.value == 'large-warehouse') {
    //     console.log(input.value);
    //     width1 = 40;
    //     height1 = 40;
    // }
    var click1 = 0;
    var xx1 = 0;
    var yy1 = 0;
    var cellType;
    for (var row = 0; row < inputX; row++) {
        data1.push(new Array());
        for (var column = 0; column < inputY; column++) {
            if (set2.has(`${row}_${column}`)) {
                data1[row].push({
                    x: xpos1,
                    y: ypos1,
                    xCor: xx1,
                    yCor: yy1,
                    width: width1,
                    height: height1,
                    cellType: 0 // SOURCE CELL
                })
            } else if (set1.has(`${row}_${column}`)) {
                data1[row].push({
                    x: xpos1,
                    y: ypos1,
                    xCor: xx1,
                    yCor: yy1,
                    width: width1,
                    height: height1,
                    cellType: 1 // ITEM TO PICK UP CELL
                })
            } else if (myPath.has(`${row}_${column}`) == true && set1.has(`${row}_${column}`) == false && set2.has(`${row}_${column}`) == false) {
                data1[row].push({
                    x: xpos1,
                    y: ypos1,
                    xCor: xx1,
                    yCor: yy1,
                    width: width1,
                    height: height1,
                    cellType: 2 // PATH CELL
                })
            } else if (mySet.has(`${row}_${column}`) == true && myPath.has(`${row}_${column}`) == false && set1.has(`${row}_${column}`) == false && set2.has(`${row}_${column}`) == false) {
                data1[row].push({
                    x: xpos1,
                    y: ypos1,
                    xCor: xx1,
                    yCor: yy1,
                    width: width1,
                    height: height1,
                    cellType: 3 // NAVIGABLE CELL
                })
            } else {
                data1[row].push({
                    x: xpos1,
                    y: ypos1,
                    xCor: xx1,
                    yCor: yy1,
                    width: width1,
                    height: height1,
                    cellType: 4 // SHELVING CELL
                })
            }
            xpos1 += width1;
            yy1++;
        }
        xpos1 = 1;
        ypos1 += height1;
        yy1 = 0;
        xx1++;
    }
    return data1;
}

function printGridFinal(myPath, set1, set2) {
    var gDataFinal = gridDataFinal(inputX, inputY, mySet, myPath, set1, set2);
    // console.log(gDataFinal);
    // console.log(inputX, inputY);
    var grid1 = d3.select('#finalGrid')
        .append("svg")
        .attr("width", inputY * WIDTH + 50 + "px")
        .attr("height", inputX * HEIGHT + 50 + "px")

    var row1 = grid1.selectAll(".row")
        .data(gDataFinal)
        .enter()
        .append("g")
        .attr("class", "row");

    var column1 = row1.selectAll(".square")
        .data(function(d) { return d; })
        .enter()
        .append("rect")
        .attr("class", "square")
        .attr("rx", 6)
        .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y; })
        .attr("width", function(d) { return d.width - PADDING; })
        .attr("height", function(d) { return d.height - PADDING; })
        .attr("class", function(d) {
            if (d.cellType == 0)
                return "source-cell";
            else if (d.cellType == 1)
                return "item-to-pick-up-cell";
            else if (d.cellType == 2)
                return "path-cell";
            else if (d.cellType == 3)
                return "navigable-cell";
            else
                return "shelving-cell";
        })
        .style("stroke", "#222")
}

function getRequest(x) {

    const proxyurl = "https://cors-anywhere.herokuapp.com/";
    var reqUrl = 'https://warehouse-path-optimisation.herokuapp.com/warehouse/' + x;
   
    fetch(reqUrl)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            for (var i = 0; i < data.valid_nodes.length; i++) {
                var currX = data.valid_nodes[i][0];
                var currY = data.valid_nodes[i][1];
                mySet.add(`${currX}_${currY}`);
            }
            console.log(mySet);
            printGrid(data.dimensions[0], data.dimensions[1], mySet);
        })
        .catch(e =>
            alert(e)
        );
}

function makePostRequest(set1, set2) {

    var tempArr1 = [...set1];
    console.log(tempArr1);
    var arr1 = new Array();
    for (var i = 0; i < tempArr1.length; i++) {
        var a = tempArr1[i].split("_");
        arr1.push({ x: Number(a[0]), y: Number(a[1]) });
    }
    var tempArr2 = [...set2];
    var a = tempArr2[0].split("_");
    var arr2 = { x: Number(a[0]), y: Number(a[1]) };
    var postData = {
        source: arr2,
        items: arr1
    }
    console.log(postData);
    console.log(input.value);
    const proxyurl = "https://cors-anywhere.herokuapp.com/";
    var postUrl = 'https://warehouse-path-optimisation.herokuapp.com/' + input.value + '/find-pick-path';
  
    fetch(postUrl, {
            method: 'post',
            headers: {
                "Accept": "application/json, text/plain, */*",
                "Content-type": "application/json"
            },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            for (var i = 1; i < data.path.length - 1; i++) {
                var currX = data.path[i][0];
                var currY = data.path[i][1];
                myPath.add(`${currX}_${currY}`);
            };
            
            printGridFinal(myPath, set1, set2);
        })
        .catch(e => {
            alert(e);
            console.log(e);
        });

}