import moderngl
from array import array
import pygame
import random

from config import *

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

# ========================== FULL EFFECT FRAG START =======================
frag_shader = """
#version 330 core

uniform vec2 resolution;
uniform sampler2D screen;  // Main Screen
uniform sampler2D tex1;    // First texture
uniform sampler2D tex2;    // Second texture
uniform sampler2D tex3;    // Third texture
uniform vec4 burst_color; // Color of the blood burst (e.g., vec4(1.0, 0.0, 0.0, 1.0) for red)


uniform float time;
uniform int effect_count;      // Number of active effects
uniform float vignette_strength; // Vignette intensity
uniform float fog_intensity;
uniform float ripple;            // Enable ripple effect
uniform float side_warble;      // Enable side warble effect
uniform float shadow_speed;    // Enable central pulse effect
uniform float perlin_toggle;     // Enable Perlin fog effect
uniform float blood_burst;      // Enable blood burst effect
uniform vec2 origin;           // Origin point of the burst in UV coordinates

in vec2 uvs;
out vec4 f_color;

// Float to generate random numbers with a pseudo-random number generator (PRNG)
float random(vec2 p) {
    return fract(sin(dot(p.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

// Function to generate Perlin noise
float perlin(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    // Smoothstep interpolation
    f = f * f * (3.0 - 2.0 * f);

    // Random hash function
    float a = dot(i, vec2(12.9898, 78.233));
    float b = dot(i + vec2(1.0, 0.0), vec2(12.9898, 78.233));
    float c = dot(i + vec2(0.0, 1.0), vec2(12.9898, 78.233));
    float d = dot(i + vec2(1.0, 1.0), vec2(12.9898, 78.233));

    // Interpolate the values
    float res = mix(mix(sin(a) * 43758.5453, sin(b) * 43758.5453, f.x),
                    mix(sin(c) * 43758.5453, sin(d) * 43758.5453, f.x), f.y);
    return fract(res);
}

void main() {
    vec4 base_color = texture(screen, uvs);


    // If ripple is enabled, apply ripple effect
    if (ripple > 0.0) {
        // Adjust the UVs for ripple effect
        vec2 centered_uvs = uvs - vec2(0.5, 0.5) * ripple; // Center the UV coordinates
        float ripple_dist = length(centered_uvs);
        float ripple_strength = sin(ripple_dist * 10.0 - time * 5.0) * 0.02; // Adjust the ripple intensity
        vec2 ripple_uvs = uvs + centered_uvs * ripple_strength;
        base_color = texture(screen, ripple_uvs); // Apply the ripple-distorted texture
    }

    if (side_warble > 0.0) {
        // Create a side shake effect
        base_color = mix(texture(tex3, vec2(uvs.x + cos(uvs.y * 10.0 + time * 0.05) * 0.02 * side_warble, uvs.y)), base_color, 0.5);
    }

    if (shadow_speed > 0.0) {
        // Create a central pulse shake effect
        base_color = mix(texture(tex2, uvs) * sin(time * shadow_speed * 0.01 + uvs.x * 5.0), base_color, 0.5);    
    }
    
    if (perlin_toggle > 0) {
        // Scale coordinates for Perlin noise
        vec2 uv = uvs * 5.0; // Adjust scale for desired fog detail

        // Add time for animation
        uv.x += time * 0.05;
        uv.y += time * 0.03;

        // Generate noise
        float noise = perlin(uv);

        // Use noise as fog alpha
        float fog = clamp(noise * perlin_toggle, 0.0, 100.0);

        // Mix fog color with base color
        vec4 fog_color = vec4(0.8, 0.8, 0.8, 1.0); // Light gray fog
        base_color *= mix(base_color, fog_color, fog);
    }
    
    if (blood_burst > 0.0) {
        vec2 centered_uvs = uvs - origin; // Center UVs on the burst origin
        float dist = length(centered_uvs); // Distance from the origin
    
        // Radial pulse effect
        float pulse = sin((dist - time * 0.25) * 15.0) * exp(-dist * 5.0);
        vec2 distorted_uvs = uvs + centered_uvs * pulse * 0.04;
    
        // Chromatic aberration: offset red, green, and blue channels slightly
        float chroma_offset = sin(time * 3.0) * 0.005;
        vec4 burst_color = vec4(
            texture(tex1, distorted_uvs + vec2(chroma_offset, 0.0)).r,
            texture(tex1, distorted_uvs + vec2(-chroma_offset, chroma_offset)).g,
            texture(tex1, distorted_uvs + vec2(0.0, -chroma_offset)).b,
            1.0
        );

        // Enhanced burst glow with radial gradient
        float radial_gradient = smoothstep(0.0, 1.0, exp(-dist * 5.0) * sin(time * 2.0 + dist * 10.0));
        vec4 glow_color = vec4(1.0, 0.0, 0.0, 1.0) * radial_gradient;
    
        // Directional streaks
        float angle = atan(centered_uvs.y, centered_uvs.x);
        float streaks = sin(angle * 12.0 + time * 10.0) * exp(-dist * 15.0);
        vec4 streak_color = vec4(streaks, streaks * 0.3, streaks * 0.1, 1.0);
    
    
        // Particle Effect Enhancements
        float particle_density = 200.0;  // Increase the density of particles
        float particle_speed = 10.0;     // Speed of particle drift
        float particle_size = 0.02;      // Larger particle size
        float particle_intensity = 1.5; // Boost the particle brightness
        
        vec2 particle_coords = mod(centered_uvs * particle_density + time * particle_speed, particle_size) - 0.5 * particle_size;
        float particle_dist = length(particle_coords);
        
        // Create multiple layers of particles for depth
        float particles_layer1 = exp(-particle_dist * 50.0) * random(uvs + time * 0.5) * exp(-dist * 8.0);
        float particles_layer2 = exp(-particle_dist * 30.0) * random(uvs * 1.5 + time * 0.8) * exp(-dist * 6.0);
        float particles_layer3 = exp(-particle_dist * 70.0) * random(uvs * 2.0 + time * 1.2) * exp(-dist * 10.0);
        
        // Combine layers for exaggerated effect
        float total_particles = particles_layer1 + particles_layer2 * 0.8 + particles_layer3 * 0.6;
        vec4 particle_color = vec4(total_particles * particle_intensity, 0.0, 0.0, 1.0);

    
        // Combine all effects
        vec4 combined_effects = burst_color + glow_color + streak_color + particle_color;
    
        // Smooth blending based on distance
        float intensity = smoothstep(0.5, 0.0, dist); // Smooth fading outward
        base_color = mix(base_color, combined_effects, intensity);
    

    
    
        // Burst glow
        float glow = exp(-dist * 10.0) * sin(time * 5.0 + dist * 20.0) * 0.5 + 0.5;
        glow_color = vec4(1, 0, 0, 1) * glow;
    
        // Particle-like noise
        float noise = random(uvs + time) * 0.2 * exp(-dist * 10.0);
        vec4 noise_color = vec4(noise, 0.0, 0.0, 1.0); // Red-tinted noise
    
        // Blend all effects
        intensity = smoothstep(0.5, 0.0, dist); // Smooth fading of the effect outward
        vec4 final_color = mix(base_color, vec4(1, 0, 0, 1) + glow_color + noise_color, intensity);
    
        base_color = final_color;
    }
    
    if (fog_intensity > 0) {
    vec4 base_color = texture(tex1, uvs);

    // Scale coordinates for Perlin noise
    vec2 uv = uvs * 2.0; // Adjust scale for smoother fog

    // Add time for animation (movement of the fog)
    uv.x += time * 0.03;
    uv.y += time * 0.02;

    // Generate smooth fog noise
    float noise = perlin(uv);

    // Apply noise as fog intensity (smooth effect)
    float fog = smoothstep(0.2, 0.8, noise * fog_intensity); // Smooth fog intensity

    // Mix fog color with base color (smooth effect)
    vec4 fog_color = vec4(0.9, 0.9, 0.9, 1.0);  // Light gray fog
    base_color *= mix(base_color, fog_color, fog);  // Add fog effect
    }
    
        // If no effects are active, render the base screen
        if (effect_count == 0 && vignette_strength <= 0.0) {
            f_color = base_color;
            return;
    }

    // Effects for tex1, tex2, tex3
    vec4 color1 = texture(tex1, vec2(uvs.x + sin(uvs.y * 10.0 + time * 0.05) * 0.02, uvs.y));

    // Combine effects based on effect_count
    vec4 final_color = base_color;



    // Apply vignette effect if intensity is greater than 0
    if (vignette_strength > 0.0) {
        vec2 screen_center = vec2(0.5, 0.5);
        float distance = length(uvs - screen_center);
        float vignette = smoothstep(0, 1.0, distance); // Adjust the range as needed
        final_color.rgb *= mix(1.0, 1.0 - vignette_strength, vignette);
    }

    f_color = final_color; // Output the final color with all effects applied
}
"""
# ========================== FULL EFFECT FRAG START =======================

# ========================== VERTICAL WAVE FRAG START =======================
vertical_wave_frag_shader = '''
#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 sample_pos = vec2(uvs.x + sin(uvs.y * 10 + time * 0.01) * 0.1, uvs.y);
    f_color = vec4(texture(tex, sample_pos).rg, texture(tex, sample_pos).b * 1.5, 1.0);
}
'''
# ========================== VERTICAL WAVE FRAG END =========================

point_glow_shader = '''
#version 330 core

uniform sampler2D tex1;
uniform vec2 positions[50];  // Precomputed positions passed from outside
uniform vec2 resolution;     // Screen resolution for scaling
uniform float point_size;    // Size of the glowing points
uniform float time;
uniform vec3 color;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec4 _ = texture(tex1, uvs);
    float time = time;
    vec3 col = vec3(0.0);

    // Iterate over the precomputed positions
    for (int i = 0; i < 50; i++) {
        vec2 pos = positions[i] / resolution; // Normalize positions to match texture coordinates
        float dist = length(uvs - pos);

        // Add glow effect based on distance to the point
        col += point_size / (dist + 0.001); // Adjust point_size for desired intensity
        col *= color;
    }

    // Set the final color with the glow effect
    // f_color = mix(texture(tex1, uvs), vec4(col, 1.0), 0.3);
    f_color = vec4(col, 1.0) + texture(tex1, uvs);
    

}
'''
def particle_drifter(shader, screen, positions, camera, size=0.001, color=(1, 1, 1)):
    """
    Render and update particles as part of the background, independent of the camera panning.

    :param shader: The shader program for rendering particles.
    :param screen: The pygame screen.
    :param positions: A numpy array of particle positions (screen-space coordinates).
    :param camera: The Camera instance.
    :param size: Particle size.
    :param color: Particle color (RGB tuple).
    """
    shader.program['color'] = color
    shader.program['point_size'] = size
    shader.program['resolution'] = screen.get_size()

    # Update particle positions
    for position in positions:
        # Apply random drift to particles
        position[0] += random.randint(-1, 1) / 10  # Horizontal drift
        position[1] += random.randint(2, 4)   # Downward drift

        # Wrap particles around the screen bounds
        position[0] %= camera.world_width
        position[1] %= camera.world_height

    # Transform particle positions into relative screen coordinates
    screen_positions = positions.copy()
    screen_positions[:, 0] -= camera.camera.x
    screen_positions[:, 1] -= camera.camera.y

    # Pass transformed positions to the shader
    shader.program['positions'] = screen_positions

# ========================== DIAGONAL RIPPLE FRAG START =======================
diagonal_ripple_frag_shader = '''
#version 330 core

uniform sampler2D tex1;
uniform float time;
uniform vec2 mouse_pos;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 centered_uvs = uvs - mouse_pos; // Shift UVs to center on the mouse
    float dist = length(centered_uvs);  // Distance from the mouse position
    float ripple = sin((dist * 10.0 - time * 0.1)) * 0.05; // Ripple effect
    vec2 ripple_uvs = uvs + centered_uvs * ripple; // Apply ripple distortion
    f_color = texture(tex1, ripple_uvs);
}
'''
# ========================== DIAGONAL RIPPLE FRAG END =========================

# ========================== BLOOD BURST FRAG START =======================
full_screen_blood_burst_frag_shader = '''
#version 330 core

uniform sampler2D tex1;
uniform float time; // Time variable for animation
uniform vec2 origin; // Origin point of the burst in UV coordinates
uniform vec4 burst_color; // Color of the blood burst (e.g., vec4(1.0, 0.0, 0.0, 1.0) for red)

in vec2 uvs;
out vec4 f_color;

float random(vec2 p) {
    return fract(sin(dot(p.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec2 centered_uvs = uvs - origin; // Center UVs on the burst origin
    float dist = length(centered_uvs); // Distance from the origin

    // Radial pulse effect
    float pulse = sin((dist - time * 0.25) * 15.0) * exp(-dist * 5.0);
    vec2 distorted_uvs = uvs + centered_uvs * pulse * 0.04;

    // Chromatic aberration: offset red, green, and blue channels slightly
    float chroma_offset = sin(time * 3.0) * 0.005;
    vec4 base_color = vec4(
        texture(tex1, distorted_uvs + vec2(chroma_offset, 0.0)).r,
        texture(tex1, distorted_uvs + vec2(-chroma_offset, chroma_offset)).g,
        texture(tex1, distorted_uvs + vec2(0.0, -chroma_offset)).b,
        1.0
    );

    // Burst glow
    float glow = exp(-dist * 10.0) * sin(time * 5.0 + dist * 20.0) * 0.5 + 0.5;
    vec4 glow_color = burst_color * glow;

    // Particle-like noise
    float noise = random(uvs + time) * 0.2 * exp(-dist * 10.0);
    vec4 noise_color = vec4(noise, 0.0, 0.0, 1.0); // Red-tinted noise

    // Blend all effects
    float intensity = smoothstep(0.5, 0.0, dist); // Smooth fading of the effect outward
    vec4 final_color = mix(base_color, burst_color + glow_color + noise_color, intensity);

    f_color = final_color;
}
'''
local_blood_burst_frag_shader = """    
#version 330 core

        main () {
        vec2 centered_uvs = uvs - origin; // Center UVs on the burst origin
        float dist = length(centered_uvs); // Distance from the origin
    
        // Radial pulse effect
        float pulse = sin((dist - time * 0.25) * 15.0) * exp(-dist * 5.0);
        vec2 distorted_uvs = uvs + centered_uvs * pulse * 0.04;
    
        // Chromatic aberration: offset red, green, and blue channels slightly
        float chroma_offset = sin(time * 3.0) * 0.005;
        vec4 burst_color = vec4(
            texture(tex1, distorted_uvs + vec2(chroma_offset, 0.0)).r,
            texture(tex1, distorted_uvs + vec2(-chroma_offset, chroma_offset)).g,
            texture(tex1, distorted_uvs + vec2(0.0, -chroma_offset)).b,
            1.0
        );

        // Enhanced burst glow with radial gradient
        float radial_gradient = smoothstep(0.0, 1.0, exp(-dist * 5.0) * sin(time * 2.0 + dist * 10.0));
        vec4 glow_color = vec4(1.0, 0.0, 0.0, 1.0) * radial_gradient;
    
        // Directional streaks
        float angle = atan(centered_uvs.y, centered_uvs.x);
        float streaks = sin(angle * 12.0 + time * 10.0) * exp(-dist * 15.0);
        vec4 streak_color = vec4(streaks, streaks * 0.3, streaks * 0.1, 1.0);
    
        // Particle-like noise
        float particle_size = 0.01;
        vec2 particle_coords = mod(centered_uvs * 100.0 + time * 5.0, particle_size) - 0.5 * particle_size;
        float particle_dist = length(particle_coords);
        float particles = exp(-particle_dist * 50.0) * random(uvs + time) * exp(-dist * 10.0);
        vec4 particle_color = vec4(particles, 0.0, 0.0, 1.0);
    
        // Combine all effects
        vec4 combined_effects = burst_color + glow_color + streak_color + particle_color;
    
        // Smooth blending based on distance
        float intensity = smoothstep(0.5, 0.0, dist); // Smooth fading outward
        base_color = mix(base_color, combined_effects, intensity);
    

    
    
        // Burst glow
        float glow = exp(-dist * 10.0) * sin(time * 5.0 + dist * 20.0) * 0.5 + 0.5;
        glow_color = vec4(1, 0, 0, 1) * glow;
    
        // Particle-like noise
        float noise = random(uvs + time) * 0.2 * exp(-dist * 10.0);
        vec4 noise_color = vec4(noise, 0.0, 0.0, 1.0); // Red-tinted noise
    
        // Blend all effects
        intensity = smoothstep(0.5, 0.0, dist); // Smooth fading of the effect outward
        vec4 final_color = mix(base_color, vec4(1, 0, 0, 1) + glow_color + noise_color, intensity);
    
        base_color = final_color;
    }
    
        // If no effects are active, render the base screen
        if (effect_count == 0 && vignette_strength <= 0.0) {
            f_color = base_color;
            return;
    }

    // Effects for tex1, tex2, tex3
    vec4 color1 = texture(tex1, vec2(uvs.x + sin(uvs.y * 10.0 + time * 0.05) * 0.02, uvs.y));

    // Combine effects based on effect_count
    vec4 final_color = base_color;
}
"""
# ========================== BLOOD BURST FRAG END =======================

enhanced_blood_burst = """
#version 330 core

uniform sampler2D tex1;
uniform vec2 u_resolution; // Screen resolution
uniform float time;      // Elapsed time
uniform vec2 u_center;     // Center of the blood burst
uniform vec4 u_base_color; // Base blood color
uniform vec4 u_glow_color; // Glow color
uniform float u_intensity; // Intensity of the effect

in vec2 uvs;
out vec4 fragColor;

void main() {
    vec4 _ = texture(tex1, uvs);
    // Normalized coordinates
    vec2 uv = gl_FragCoord.xy / u_resolution;
    vec2 center_uv = u_center / u_resolution;

    // Distance from the center of the blood burst
    float dist = distance(uv, center_uv);

    // Radial gradient for the base burst
    float burst = smoothstep(0.4, 0.0, dist);

    // Pulsating effect
    float pulse = 0.5 + 0.5 * sin(time * 5.0);
    float pulse_effect = smoothstep(0.4 + 0.05 * pulse, 0.0, dist);

    // Radial ripples
    float ripple = 0.05 * sin((dist - time) * 20.0) * burst;

    // Combined effect
    float final_burst = clamp(burst + pulse_effect + ripple, 0.0, 1.0);

    // Glow effect around the edges
    float glow = smoothstep(0.5, 0.4, dist) * pulse;

    // Final color
    vec4 color = mix(u_base_color, u_glow_color, glow);
    fragColor = color * final_burst;
}
"""

# ========================== VIGNETTE FRAG START =======================
vignette_frag_shader = """
#version 330 core

uniform sampler2D tex1;    // First texture
uniform float vignette_strength; // Vignette intensity
uniform float time; // Time value


in vec2 uvs;
out vec4 f_color;

void main() {
    vec4 base_color = texture(tex1, uvs);

    float time = time;
    vec2 screen_center = vec2(0.5, 0.5);
    float distance = length(uvs - screen_center);
    float vignette = smoothstep(0, 1.0, distance); // Adjust the range as needed
    base_color.rgb *= mix(1.0, 1.0 - vignette_strength, vignette);


    f_color = base_color; // Output the final color with all effects applied
}
"""
# ========================== VIGNETTE FRAG END =========================

soft_fog = """
#version 330 core

uniform sampler2D tex1;      // First texture (scene texture)
uniform float fog_intensity; // Intensity of the fog effect
uniform float time;          // Time value for animation

in vec2 uvs;  // Texture coordinates
out vec4 f_color;  // Output color

// Function to generate Perlin noise
float perlin(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    f = f * f * (3.0 - 2.0 * f);

    float a = dot(i, vec2(12.9898, 78.233));
    float b = dot(i + vec2(1.0, 0.0), vec2(12.9898, 78.233));
    float c = dot(i + vec2(0.0, 1.0), vec2(12.9898, 78.233));
    float d = dot(i + vec2(1.0, 1.0), vec2(12.9898, 78.233));

    float res = mix(mix(sin(a) * 43758.5453, sin(b) * 43758.5453, f.x),
                    mix(sin(c) * 43758.5453, sin(d) * 43758.5453, f.x), f.y);
    return fract(res);
}

void main() {
    vec4 base_color = texture(tex1, uvs);

    // Scale coordinates for Perlin noise
    vec2 uv = uvs * 2.0; // Adjust scale for smoother fog

    // Add time for animation (movement of the fog)
    uv.x += time * 0.03;
    uv.y += time * 0.02;

    // Generate smooth fog noise
    float noise = perlin(uv);

    // Apply noise as fog intensity (smooth effect)
    float fog = smoothstep(0.2, 0.8, noise * fog_intensity); // Smooth fog intensity

    // Mix fog color with base color (smooth effect)
    vec4 fog_color = vec4(0.9, 0.9, 0.9, 1.0);  // Light gray fog
    base_color *= mix(base_color, fog_color, fog);  // Add fog effect

    f_color = base_color; // Output final color
}
"""

rapid_glow_particles = """
#version 330 core

uniform vec2 resolution;
uniform float time;
uniform sampler2D tex1;
uniform vec2 center; // The center of the glow area (can be the screen center or a fixed point)
uniform float particle_size; // Particle size for glow effect
uniform float pulse_speed;   // Speed at which the glow pulses
uniform float movement_speed; // Speed at which particles move

in vec2 uvs;
out vec4 f_color;

// Pseudo-random number generator to give particles dynamic randomness
float random(vec2 p) {
    return fract(sin(dot(p.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

// Function to create a mystical glow effect with particles
void main() {
    vec2 particle_uvs = uvs - center; // Offset to the center of the glow
    vec4 _ = texture(tex1, uvs); // Sample the texture
    float distance = length(particle_uvs); // Calculate distance from the center
    
    // Particle movement over time
    vec2 movement = vec2(sin(time * movement_speed), cos(time * movement_speed)) * 0.05;
    particle_uvs += movement;
    
    // Adjust particle size based on distance from center for a more natural effect
    float particle_distance = distance * particle_size;

    // Create a dynamic glow effect (pulsing)
    float glow_intensity = sin(time * pulse_speed) * 0.5 + 0.5; // Pulsing over time

    // Noise for adding randomness to the glow effect
    float noise = random(uvs + time * 0.2) * 0.3;

    // Determine the particle's brightness based on its distance from the center
    float brightness = exp(-distance * 6.0) * glow_intensity + noise;

    // Choose a warm color palette (mystical light colors like soft yellows and golds)
    vec4 glow_color = vec4(1.0, 0.8, 0.4, 1.0) * brightness; // Warm yellow-orange glow
    
    // Apply a soft fade for particles far from the center to make them appear more mystical
    if (distance > 0.5) {
        glow_color.a = 0.0; // Fade out particles farther from the center
    }

    // Output the final color with the glow effect
    f_color = glow_color;
}
"""

enchanted_pollen = """
#version 330 core

uniform vec2 resolution;
uniform float time;
uniform sampler2D tex1;
uniform vec2 center;  // The center of the glow effect (or the "canopy")
uniform float particle_size;  // Size of the particles
uniform float fall_speed;  // Speed at which the particles fall
uniform float pulse_speed;  // Speed at which particles pulse
uniform vec4 particle_color;  // The color of the particle glow (light yellow, green, or pale)

in vec2 uvs;
out vec4 f_color;

// Pseudo-random number generator
float random(vec2 p) {
    return fract(sin(dot(p.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

// Function to create a falling particle effect
void main() {
    vec2 particle_uvs = uvs - center; // Offset to center the particles around the center of the screen
    vec4 _ = texture(tex1, uvs); // Sample the texture
    float distance = length(particle_uvs); // Distance from the center (for size adjustments)

    // Slow falling movement (simulate the particles drifting down)
    float fall = mod(time * fall_speed + random(uvs), 1.0); // Fall over time, randomize the start of each particle
    
    // Particle size and distance-based fading
    float particle_opacity = smoothstep(0.1, 0.3, distance); // Fade based on distance from center
    float size = particle_size * (1.0 - fall);  // Decrease size as particles fall

    // Create a gentle pulse for each particle
    float pulse_intensity = sin(time * pulse_speed + distance * 10.0) * 0.2 + 0.3; // Pulse effect based on distance

    // Light glow effect (using soft pastel colors)
    vec4 glow_color = particle_color * (pulse_intensity * particle_opacity); // Multiply intensity and opacity

    // Apply particle size to UVs and offset them based on fall
    vec2 final_uvs = uvs + vec2(sin(uvs.x * 10.0) * 0.05, -fall * 0.5); // Gentle downward fall effect

    // Add randomness for each particle to create a more organic and natural look
    float noise = random(final_uvs + time * 0.1) * 0.1; // Gentle random flickering

    // Apply the glow and random noise to the particle color
    f_color = glow_color + vec4(noise, noise, noise, 0.0); // Adding slight noise to the color

    // Fading out particles further from the center
    if (distance > 0.5) {
        f_color.a *= 0.5;  // Fading effect based on distance from center
    }

    // Final opacity based on distance and time
    f_color.a = smoothstep(0.0, 0.3, fall) * f_color.a;  // Make particles fade as they fall further
}
"""

# ========================== PERLIN NOISE FRAG END =========================
perlin_noise_shader = """
#version 330 core

uniform sampler2D tex1;    // First texture
uniform float perlin_toggle; // Perlin Noise intensity
uniform float time; // Time value


in vec2 uvs;
out vec4 f_color;


// Function to generate Perlin noise
float perlin(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    // Smoothstep interpolation
    f = f * f * (3.0 - 2.0 * f);

    // Random hash function
    float a = dot(i, vec2(12.9898, 78.233));
    float b = dot(i + vec2(1.0, 0.0), vec2(12.9898, 78.233));
    float c = dot(i + vec2(0.0, 1.0), vec2(12.9898, 78.233));
    float d = dot(i + vec2(1.0, 1.0), vec2(12.9898, 78.233));

    // Interpolate the values
    float res = mix(mix(sin(a) * 43758.5453, sin(b) * 43758.5453, f.x),
                    mix(sin(c) * 43758.5453, sin(d) * 43758.5453, f.x), f.y);
    return fract(res);
}

void main() {
    vec4 base_color = texture(tex1, uvs);


    // Scale coordinates for Perlin noise
    vec2 uv = uvs * 5.0; // Adjust scale for desired fog detail

    // Add time for animation
    uv.x += time * 0.05;
    uv.y += time * 0.03;

    // Generate noise
    float noise = perlin(uv);

    // Use noise as fog alpha
    float fog = clamp(noise * perlin_toggle, 0.0, 100.0);

    // Mix fog color with base color
    vec4 fog_color = vec4(0.8, 0.8, 0.8, 1.0); // Light gray fog
    base_color *= mix(base_color, fog_color, fog);

    f_color = base_color; // Output the final color with all effects applied
}
"""
# ========================== PERLIN NOISE FRAG END =========================

# ========================== GLOW EFFECT FRAG START =========================
glow_effect_shader = """
uniform sampler2D texture1; // Base texture
uniform vec3 glowColor; // Color of the glow
uniform float glowIntensity; // Intensity of the glow
uniform float time; // For dynamic pulsing effect

void main()
{
    // Sample the base texture
    vec4 baseColor = texture(texture1, TexCoord);

    // Create the glow effect
    float glow = sin(time * 2.0) * 0.5 + 0.5; // Pulsing effect
    vec4 glowEffect = vec4(glowColor, 1.0) * glow * glowIntensity;

    // Combine base color and glow
    FragColor = baseColor + glowEffect;
}"""
# ========================== GLOW EFFECT FRAG END =========================

# ========================== TECHNO SHIELD FRAG START =========================
wild_vert_shader = """

#version 330 core

in vec2 vert;  // Input vertex position
out vec2 uv;   // Pass through UV coordinates (optional, only if needed for something else)

void main() {
    uv = vert * 0.5 + 0.5; // Convert [-1, 1] range to [0, 1], optional
    gl_Position = vec4(vert, 0.0, 1.0);
}
"""
wild_frag_shader = """
#version 330 core

uniform sampler2D tex1;    // Texture, not used in this effect but included for completeness
uniform float time;        // Time value
uniform float hard_radius;      // Effect hard cut-off radius
uniform float soft_radius;      // Effect fade out radius
uniform vec2 resolution;   // Screen resolution
uniform vec2 mouse;        // Mouse Position
in vec2 uvs;               // Input UV coordinates
out vec4 f_color;          // Final fragment color

// Palette function for generating colors
vec3 palette(float t) {
    vec3 a = vec3(0.5, 0.5, 0.5);
    vec3 b = vec3(0.5, 0.5, 0.5);
    vec3 c = vec3(1.0, 1.0, 1.0);
    vec3 d = vec3(0.263, 0.416, 0.557);

    return a + b * cos(6.28318 * (c * t + d));
}

void main() {
    // Transform UV coordinates to center the effect
    vec4 _ = texture(tex1, uvs);
    vec2 uv = (gl_FragCoord.xy * 2.0 - resolution.xy) / resolution.y;
    uv -= (mouse * 2.0 - 1);
    vec2 uv0 = uv;
    vec3 finalColor = vec3(0.0);

    // Iterative loop to create the layered effect
    for (float i = 0.0; i < 4.0; i++) {
        uv = fract(uv * 1.5) - 0.5;

        // Calculate distance and color contributions
        float d = length(uv) * exp(-length(uv0));
        vec3 col = palette(length(uv0) + i * 0.4 + time * 0.4);

        d = sin(d * 8.0 + time) / 8.0;
        d = abs(d);
        d = pow(0.01 / d, 1.2);

        finalColor += col * d;
    }

    if (hard_radius > 0) {
    float dist = length(uv0);
    if (dist > hard_radius) {
        discard;  // Skip rendering for pixels outside the radius
     }
    }

    if (soft_radius > 0) {
    float dist = length(uv0);
    float intensity = smoothstep(soft_radius, soft_radius * 0.8, dist);  // Smooth falloff
    finalColor *= 1.0 - intensity;  // Fade the effect
    }



    // Output the final color
    f_color = vec4(finalColor, 1.0);



}
"""
wild_frag_shader_2 = """
#version 330 core

uniform sampler2D tex1;    // Texture, not used in this effect but included for completeness
uniform float time;        // Time value
uniform float hard_radius;      // Effect hard cut-off radius
uniform float soft_radius;      // Effect fade out radius
uniform vec2 resolution;   // Screen resolution
uniform vec2 mouse;        // Mouse Position

in vec2 fragCoord;
out vec4 fragColor;

vec3 palette(float d){
	return mix(vec3(0.2,0.7,0.9),vec3(1.,0.,1.),d);
}

vec2 rotate(vec2 p,float a){
	float c = cos(a);
    float s = sin(a);
    return p*mat2(c,s,-s,c);
}

float map(vec3 p){
    for( int i = 0; i<8; ++i){
        float t = time*0.2;
        p.xz =rotate(p.xz,t);
        p.xy =rotate(p.xy,t*1.89);
        p.xz = abs(p.xz);
        p.xz-=.5;
	}
	return dot(sign(p),p)/5.;
}

vec4 rm (vec3 ro, vec3 rd){
    float t = 0.;
    vec3 col = vec3(0.);
    float d;
    for(float i =0.; i<64.; i++){
		vec3 p = ro + rd*t;
        d = map(p)*.5;
        if(d<0.02){
            break;
        }
        if(d>100.){
        	break;
        }
        //col+=vec3(0.6,0.8,0.8)/(400.*(d));
        col+=palette(length(p)*.1)/(400.*(d));
        t+=d;
    }
    return vec4(col,1./(d*100.));
}
void main ()
{
    vec2 uv = (fragCoord-(resolution.xy/2.))/resolution.x;
	vec3 ro = vec3(0.,0.,-50.);
    ro.xz = rotate(ro.xz,time);
    vec3 cf = normalize(-ro);
    vec3 cs = normalize(cross(cf,vec3(0.,1.,0.)));
    vec3 cu = normalize(cross(cf,cs));

    vec3 uuv = ro+cf*3. + uv.x*cs + uv.y*cu;

    vec3 rd = normalize(uuv-ro);

    vec4 col = rm(ro,rd);


    fragColor = col;
}
"""
# ========================== TECHNO SHIELD FRAG END =========================

# ========================== LIGHTNING FRAG START =========================
lightning_frag_shader = """
uniform float time;
uniform vec2 resolution;
uniform sampler2D tex1;
uniform vec2 mouse;
in vec2 fragCoord;
out vec4 fragColor;

float hash11(float p) {
    p = fract(p * 0.1031);
    p *= p + 33.33;
    return abs(0.5 - fract(p * p * 2.0)) * 2.0;
}

float noise11(float p) {
	float i = floor(p);
	float f = fract(p);
    f *= f * (3.0 - 2.0 * f);
	return mix(hash11(i), hash11(i + 1.0), f);
}

float hash12(vec2 p) {
	vec3 p3 = fract(p.xyx * 0.1031);
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.x + p3.y) * p3.z);
}

float noise(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	float res = mix(
		mix(hash12(i), hash12(i + vec2(1, 0)), f.x),
		mix(hash12(i + vec2(0, 1)), hash12(i + vec2(1)), f.x), f.y);
	return res;	
}

float fbm(vec2 p, int octaves) {
	float s = 0.0, m = 0.0, a = 1.0;
	for(int i = 0; i < octaves; i++) {
		s += a * noise(p);
		m += a;
		a *= 0.5;
		p *= mat2(1.6, 1.2, -1.2, 1.6); 
	}
	return s / m;
}

float lightning(vec2 uv, float i) {
    // Expanding / Warping
    float n = fract(noise11(i * 3.0) * 3.0) * 2.0 - 1.0;
    float bend = n * 0.15;
    bend *= smoothstep(1.0, -0.5, abs(0.5 - gl_FragCoord.x / resolution.x) * 1.6);
    uv.y += (2.0 - uv.x * uv.x) * bend;
    
    uv.x -= time * 0.2;
    
    float d = fbm(uv * vec2(2, 1.4) - vec2(0, i), 6);
    d = (d * 2.0 - 1.0) * 0.45;
    return abs(uv.y - d);
}

vec3 lightnings(vec2 uv) {
    float t2 = time * 0.08;
    float d1 = lightning(uv, 21.17 + t2);
    float d2 = lightning(uv, 63.41 + t2);
    float d3 = lightning(uv, 77.69 + t2);
    float d4 = lightning(uv, 21.99 + t2);
    float dd = max(0.0, 1.0 - sqrt(d1 + d2 * d3 + d3 + d4 * d1) * 0.5);
    float d = 0.007 / sqrt(d1 * d2 * d3 * d4);
    vec3 col = vec3(0.31, 0.5, 0.89) * sqrt(d);
    
    float md = 1.0 - dd;
    col = col * 0.7 + 0.7 * vec3(4.0 * md * md + 3.5 * md, 0.3, 0.6) * md * d;
    col = mix(col, col * col, min(1.0, dd * dd * dd * dd));
    col = (col - 0.5) * 0.6 + 0.3;
    
    return col;
}

void main() {
    vec2 uv = (gl_FragCoord.xy * 2.0 - resolution.xy) / resolution.y;
    vec2 uv0 = uv;
    uv -= (mouse * 2.0 - 1);
    vec4 _ = texture(tex1, uv);
    
    // Get the lightning color
    vec3 color = lightnings(uv);

    // Calculate brightness (luminance) to determine transparency
    float brightness = dot(color, vec3(0.299, 0.587, 0.114)); // Standard luminance formula
    float alpha = smoothstep(0.0, 0.9, brightness); // Adjust thresholds to control transparency

    float dist = length(uv0);
    if (dist > 0.2) {
        discard;  // Skip rendering for pixels outside the radius
     }
    


    // Set the fragment color with transparency
    fragColor = vec4(color, alpha);
}
"""
# ========================== LIGHTNING FRAG END =========================

test = """
#version 330 core

out vec4 fragColor;

uniform sampler2D tex1;
uniform vec2 resolution;
uniform float time;

void main() {

vec2 uv = (gl_FragCoord.xy - resolution.xy / 2.0) / resolution.y;
vec4 _ = texture(tex1, uv);
vec3 col = vec3(0.0);
float time = time;

col += 0.01 / length(uv);


fragColor = vec4(col, 1.0);
}
"""


class ShaderManager:
    def __init__(self, _frag_shader=frag_shader, wild_shader=wild_frag_shader):
        self.ctx = moderngl.create_context()
        self.vert_shader = vert_shader
        self.frag_shader = _frag_shader
        self.wild_shader = wild_shader

        self.program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.frag_shader)
        self.wild_program = self.ctx.program(vertex_shader=self.vert_shader, fragment_shader=self.wild_shader)

        # ===================== QUAD BUFFER AND RENDERED FOR TEXCOORD RELATED EFFECTS ===========================
        self.texcoord_quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,  # topright
            -1.0, -1.0, 0.0, 1.0,  # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))
        self.texcoord_render_object = self.ctx.vertex_array(self.program,
                                                            [(self.texcoord_quad_buffer, '2f 2f', 'vert', 'texcoord')])
        # ===================== QUAD BUFFER AND RENDERED FOR TEXCOORD RELATED EFFECTS ===========================

        # ===================== QUAD BUFFER AND RENDERED FOR FRAGCOORD RELATED EFFECTS ===========================
        self.quad_vertices = [
            -1.0, -1.0,  # Bottom-left
            1.0, -1.0,  # Bottom-right
            -1.0, 1.0,  # Top-left
            1.0, 1.0  # Top-right
        ]
        self.frag_coord_quad_buffer = self.ctx.buffer(data=array('f', self.quad_vertices))
        self.frag_render_object = self.ctx.vertex_array(self.wild_program, [(self.frag_coord_quad_buffer, '2f', 'vert')])
        # ===================== QUAD BUFFER AND RENDERED FOR FRAGCOORD RELATED EFFECTS ===========================

        self.textures = []
        self.t = 0

    def surf_to_texture(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def update_textures(self, surfaces):
        self.t += 0.1
        self.textures = []
        for i, surface in enumerate(surfaces):
            texture = self.surf_to_texture(surface)
            self.textures.append(texture)
            texture.use(i)  # Bind the texture to the correct texture unit

    def update_frag_textures(self, surfaces):
        self.frag_textures = []
        self.t += 0.03
        for i, surface in enumerate(surfaces):
            texture = self.surf_to_texture(surface)
            texture.rect = surface.get_rect()
            self.frag_textures.append(texture)
            texture.use(i)  # Bind the texture to the correct texture unit

    def apply_vignette(self, strength):
        self.program["vignette_strength"] = strength

    def apply_ripple(self, ripple):
        self.program["ripple"] = ripple

    def end_ripple(self):
        self.program["ripple"] = 0

    def apply_side_warble(self, side_warble):
        self.program["side_warble"] = side_warble

    def end_side_warble(self):
        self.program["side_warble"] = 0

    def apply_side_shadow_scroll(self, speed):
        self.program["shadow_speed"] = speed

    def end_side_shadow_scroll(self):
        self.program["shadow_speed"] = 0

    def apply_perlin_noise(self, noise_strength):
        self.program["perlin_toggle"] = noise_strength

    def end_perlin_noise(self):
        self.program["perlin_toggle"] = 0

    def render(self):
        for i, tex in enumerate(self.textures):
            tex.use(i)  # Bind each texture to its corresponding texture unit
            self.program[f'tex{i + 1}'] = i  # Pass the texture unit to the shader
        # Pass the mouse coordinates to the shader
        self.program['time'] = self.t
        self.texcoord_render_object.render(mode=moderngl.TRIANGLE_STRIP)

        for tex in self.textures:
            tex.release()

    def frag_render(self):

        for i, tex in enumerate(self.frag_textures):
            tex.use(i)
            self.wild_program[f'tex{i + 1}'] = i

        self.wild_program['time'] = self.t
        self.frag_render_object.render(mode=moderngl.TRIANGLE_STRIP)

        for tex in self.frag_textures:
            tex.release()



    def frag_coord_render(self, camera, center=(0.5, 0.5), radius=0.1):
        mouse_pos = camera.x, camera.y  # Get the mouse position in pixels
        # mouse_x = mouse_pos[0] / SCREEN_WIDTH  # Normalize to range [0, 1]
        mouse_y = 1.0 - ((mouse_pos[1] + 200) / PANNING_SCREEN_WIDTH)  # Normalize and invert Y-axis for OpenGL coordinates
        mouse_x = (camera.player.position[0] - camera.x + 500) / SCREEN_WIDTH

        self.wild_program['mouse'] = (mouse_x, mouse_y)
        # self.wild_program["soft_radius"] = center
        # self.wild_program["hard_radius"] = radius

        for i, tex in enumerate(self.frag_textures):
            tex.use(i)
            self.wild_program[f'tex{i + 1}'] = i

        self.wild_program['time'] = self.t
        self.frag_render_object.render(mode=moderngl.TRIANGLE_STRIP)

        for tex in self.frag_textures:
            tex.release()


def frag_coord_shader_effect(shader, camera):
    shader.update_frag_textures([])
    shader.wild_program['resolution'] = [PANNING_SCREEN_WIDTH, PANNING_SCREEN_HEIGHT]
    # shader.wild_program['soft_radius'] = 0.3  # Inner Ring Radius
    # shader.wild_program['hard_radius'] = 0.5  # Outer Ring Radius
    shader.frag_coord_render(camera, 0.1, 0.2)


def texcoord_shader_effect(shader, effect_name, effect_strength):
    try:
        shader.program[effect_name] = effect_strength
    except KeyError:
        print(f"Invalid effect name: {effect_name}")