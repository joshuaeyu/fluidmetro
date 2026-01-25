"use strict";

// Document elements
export const VehicleType = Object.freeze({
    Bus: Symbol("bus"),
    Metro: Symbol("metro"),
    Cableway: Symbol("cableway")
})
const canvas = document.getElementById("canvas");

// San Francisco border coordinates
const NORTH_BORDER = 37.833;
const SOUTH_BORDER = 37.700;
const EAST_BORDER = -122.359;
const WEST_BORDER = -122.517;
export const LONGITUDE_SPAN = NORTH_BORDER - SOUTH_BORDER;
export const LATITUDE_SPAN = EAST_BORDER - WEST_BORDER;
// export const milesPerDegreeLatitude = 54.69;
// export const milesPerDegreeLongitude = 69.00;

// Coordinate functions
export function calcX(longitude) {
    return (longitude - WEST_BORDER) / (EAST_BORDER - WEST_BORDER)
}
export function calcY(latitude) {
    return 1 - (latitude - SOUTH_BORDER) / (NORTH_BORDER - SOUTH_BORDER)
}
export function calcAdjustedX(longitude) {
    const x0 = calcX(longitude);
    if (canvas.width <= canvas.height) {
        return x0;
    } else {
        const offset = (canvas.width - canvas.height) / 2 / canvas.width;
        return x0 / (canvas.width / canvas.height) + offset;
    }
}
export function calcAdjustedY(latitude) {
    const y0 = calcY(latitude);
    if (canvas.height <= canvas.width) {
        return y0;
    } else {
        const offset = (canvas.height - canvas.width) / 2 / canvas.height;
        return y0 / (canvas.height / canvas.width) + offset;
    }
}

// Vehicle functions
export function getVehicleType(vehicle) {
    if (['CA', 'PH', 'PM'].indexOf(vehicle.route_id) !== -1) {
        return VehicleType.Cableway;
    } else if (isAlpha(vehicle.route_id[0])) {
        return VehicleType.Metro;
    } else {
        return VehicleType.Bus;
    }
}
function isAlpha(char) {
    return /^[A-Z]/.test(char);
}

// API calls
export async function fetchBatchIds() {
    // Fetch batch ids
    let batch_ids;
    try {
        const request = new Request("http://localhost:8000/history/all_batch_ids");
        const response = await fetch(request);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status} ${response.statusText}`);
        }
        batch_ids = await response.json();
    } catch (e) {
        throw e;
    }

    return batch_ids;
}

export async function fetchVehiclePositions(batch_id = null) {
    // Fetch vehicle positions
    let vehicles;
    try {
        let url = "http://localhost:8000";
        if (batch_id) {
            url += `/history/batch/${batch_id}`;
        } else {
            url += "/live";
        }
        const request = new Request(url);
        const response = await fetch(request);
        if (!response.ok) {
            throw new Error(`Response status: ${response.status} ${response.statusText}`);
        }
        vehicles = await response.json();
    } catch (e) {
        throw e;
    }

    return vehicles;
}