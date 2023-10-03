let x = [];
let y = [];

let size_data = 20;

let index = 0;
let url = "/getData?profile="+index;

// Handle functions (for the select fields)
// Profile
function handleProfileChange(selectElement) {
    // Getting new value
    var selected_profile = selectElement.value;
    index = selected_profile;

    // Updating URL
    url = "/getData?profile="+index;

    // Get the data of the selected profile
    getData();
}
// Size
function handleSizeChange(selectElement) {
    // Getting new value
    var selected_size = selectElement.value;
    size_data = selected_size;

    // Get the data of the selected profile
    plotGraph();
}

// Function to plot the graph
function plotGraph(){

    var data = {
        x: x.slice(-size_data),
        y: y.slice(-size_data),
        mode: 'lines',
        name: 'Test'
    };

    var data_graph = [data];

    var layout_graph = {
        title: `Profile `+index,
    };

    Plotly.newPlot('Plot', data_graph, layout_graph);
}

// Function to request the data to the api (flask endpoint)
function getData(){
    $.ajax({
        type: "GET",
        url: url,
        contentType: "application/json",
        dataType: 'json' ,
    }).done( function(data) {
        x = data.x;
        y = data.y;

        plotGraph();
    });
}

window.setInterval(getData, 5000);