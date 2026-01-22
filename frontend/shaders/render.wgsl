// Vertex shader
struct VertexOut {
    @location(0) uv : vec2f,
    @builtin(position) position : vec4f
}

@vertex
fn vertex_main (
    @location(0) position: vec4f,
    @location(1) uv: vec2f
) -> VertexOut {
    return VertexOut(vec2f(uv.x, 1.0-uv.y), position);
}

// Fragment shader
@group(0) @binding(0) var output_sampler: sampler;
@group(0) @binding(1) var output_map: texture_2d<f32>;

@fragment
fn fragment_main(
    fragIn: VertexOut
) -> @location(0) vec4f {
    let sample = textureSample(output_map, output_sampler, fragIn.uv);
    let value = min(sample.r, 100);
    
    // Display color gradient with multiple stops
    var mix_value = value;
    var disp_value = vec4f(0,0,0,1);
    let width0 = 5.0;
    let width1 = 10.0;
    let width2 = 85.0;
    // interval0: black to cyan
    disp_value = mix(disp_value, vec4f(0,0.5,0.5,1), clamp(mix_value, 0, width0) / width0);
    mix_value -= width0;
    // interval1: cyan to magenta
    disp_value = mix(disp_value, vec4f(0.75,0,0.75,1), clamp(mix_value, 0, width1) / width1);
    mix_value -= width1;
    // interval2: magenta to white
    disp_value = mix(disp_value, vec4f(1,1,1,1), clamp(mix_value, 0, width2) / width2);
    
    return disp_value;
}