"use strict";

// Data refresh button
const refreshBtn = document.getElementById("refresh-btn");
const vehiclesDiv = document.getElementById("vehicles");
refreshBtn.addEventListener("click", fetchData);
async function fetchData() {
    try {
        // Get vehicle positions as pbuf
        const request = new Request("http://localhost:8000/live");
        const response = await fetch(request);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status} ${response.statusText}`);
        }
        vehiclesDiv.textContent = await response.text();
    } catch (e) {
        alert(e);
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