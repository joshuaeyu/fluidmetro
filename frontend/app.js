"use strict";

// Document elements
const refreshBtn = document.getElementById("refresh-btn");
const vehiclesDiv = document.getElementById("vehicles");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
refreshBtn.addEventListener("click", fetchData);

// San Francisco border coordinates
const NORTH_BORDER = 37.833;
const SOUTH_BORDER = 37.708;
const EAST_BORDER = -122.359;
const WEST_BORDER = -122.517;

function calcX(longitude) {
    return (longitude - WEST_BORDER) / (EAST_BORDER - WEST_BORDER)
}
function calcY(latitude) {
    return 1 - (latitude - SOUTH_BORDER) / (NORTH_BORDER - SOUTH_BORDER)
}

async function fetchData() {
    // Fetch vehicle positions
    let vehicles;
    try {
        const request = new Request("http://localhost:8000/live");
        const response = await fetch(request);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status} ${response.statusText}`);
        }
        vehicles = await response.json();
    } catch (e) {
        alert(e);
    }
    // Draw on canvas
    if (canvas.getContext) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgb(128 0 0)";
        for (const [_, vehicle] of Object.entries(vehicles)) {
            let x = calcX(vehicle.longitude) * canvas.width;
            let y = calcY(vehicle.latitude) * canvas.height;
            ctx.fillRect(x, y, 2, 2);
        }
    } else {

    }

    // fetch("http://localhost:8000/live")
    //     .then((response) => {
    //         if (!response.ok) {
    //             throw new Error(`Could not open ${url}.`);
    //         }
    //         return response.text();
    //     })
    //     .then((text) => {
    //         const p = document.createElement("p");
    //         p.textContent = text;
    //         document.body.appendChild(p);
    //     })
    //     .catch((error) => {
    //         alert(error);
    //     });
}