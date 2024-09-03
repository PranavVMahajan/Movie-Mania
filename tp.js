var s = ""; // Not used in the provided code, seems unused.

var myarray = []; // Declares an empty array named myarray to store IDs of clicked buttons.

// Declares a function named toggleSeat, which takes an ID parameter.
function toggleSeat(id) {
    // Retrieves the button element by its ID.
    var button = document.getElementById(id);
    
    // Gets the computed style of the button.
    var computedStyle = window.getComputedStyle(button);
    
    // Extracts the background color from the computed style.
    var backgroundColor = computedStyle.backgroundColor;

    // Checks if the background color of the button is white.
    if (backgroundColor === "rgb(255, 255, 255)") {
        // Changes the background color of the button to a shade of gray.
        button.style.backgroundColor = "#708090";
        // Changes the text color of the button to white.
        button.style.color = "#fff";
        // Pushes the ID of the button into the myarray array.
        myarray.push(id);
        // Logs the updated myarray to the console.
        console.log(myarray);
    } 
    // Checks if the background color of the button is gray.
    else if (backgroundColor === "rgb(112, 128, 144)") {
        // Changes the background color of the button back to white.
        button.style.backgroundColor = "#fff";
        // Changes the text color of the button to red.
        button.style.color = "#ff2c1f";
        // Finds the index of the button ID in the myarray array.
        var indexToRemove = myarray.indexOf(id);
        // Checks if the button ID exists in the myarray array.
        if (indexToRemove !== -1) {
            // Removes the button ID from the myarray array.
            myarray.splice(indexToRemove, 1);
        }
        // Logs the updated myarray to the console.
        console.log(myarray);
    }
}
