// import { fetchVehiclePositions } from "./app.js"
// import { initWebGPU } from "./webgpu.js"
// import { initSimulationPipelines } from "./fluids.js"
import { webGpuContext } from "./fluids/context.js";
import { SimulationApp } from "./fluids/simulation.js";
import { RenderApp } from "./fluids/render.js";

const canvas = document.getElementById("canvas");
await webGpuContext.init(canvas);

const simulationSettings = {
    M: 1000, // Doesn't include boundary
    N: 1000, // Doesn't include boundary
    dt: 0.001,
    diffusivity: 0.5,
    viscosity: 1,
};

const renderSettings = {
    M: 1000, // Doesn't include boundary
    N: 1000, // Doesn't include boundary
};

const simulator = await SimulationApp.build(simulationSettings);
const renderer = await RenderApp.build(renderSettings);

const data = new Float32Array((simulationSettings.M+2) * (simulationSettings.N+2));
for (let i = 0; i < simulationSettings.N+2; i++) {
    for (let j = 0; j < simulationSettings.M+2; j++) {
        const idx = i * (simulationSettings.M+2) + j;
        if (0.47*simulationSettings.M < i && i < 0.53*simulationSettings.M) {
            data[idx] = 5;
        } else {
            data[idx] = 0;
        }
    }
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

await simulator.addSource(simulator.resources.densityTextureArray, 0, data);
for (let i = 0; i < 1000; i++) {
    await simulator.densityStep();
    const tv = await simulator.getDensityOutputTextureView();
    renderer.render(tv);
    await delay(10);
}