import pygame
import shader
import time
import slider
pygame.init()




fog_frag_shader = """
#version 330 core

in vec2 uvs;                // Texture coordinates passed from vertex shader
out vec4 finalColor;        // Final color output

uniform sampler2D tex1; // The rendered scene texture
uniform vec3 fogColor;         // Fog color
uniform float fogDensity;      // Fog density
uniform float time;            // Time for animated fog movement

// Pseudorandom number generator
float rand(vec2 co) {
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453123);
}

// Perlin-like noise function
float perlinNoise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);

    f = f * f * (3.0 - 2.0 * f); // Smoothstep interpolation

    float a = rand(i + vec2(0.0, 0.0));
    float b = rand(i + vec2(1.0, 0.0));
    float c = rand(i + vec2(0.0, 1.0));
    float d = rand(i + vec2(1.0, 1.0));

    return mix(mix(a, b, f.x), mix(c, d, f.x), f.y);
}

void main() {

    
    // Fetch the base scene texture color
    vec4 sceneColor = texture(tex1, uvs);

    // Simulate fog depth using the texture coordinate's distance from the center
    vec2 fogCoord = uvs * 2.0 - 1.0; // Map uvs to [-1, 1] range
    float fogDepth = length(fogCoord); // Distance from screen center

    // Add dynamic noise to fog density for a more realistic effect
    float noise = perlinNoise(fogCoord * 0.5 + vec2(time * 0.1));
    float fogFactor = clamp(fogDensity * (fogDepth + noise * 0.2), 0.0, 1.0);

    // Blend scene color with fog color based on fog factor
    vec3 blendedColor = mix(sceneColor.rgb, fogColor, fogFactor);
    finalColor = vec4(blendedColor, sceneColor.a);
}
"""
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600), pygame.OPENGL | pygame.DOUBLEBUF)
test_shader = shader.ShaderManager(_frag_shader=fog_frag_shader)
test_image = pygame.image.load("../../game_assets/concept_art/start_menu_2.png").convert_alpha()


# Sliders
color_slider, color_output = slider.initialize_slider(screen, 200, 400, 400, 0, 1, 0.01)
density_slider, density_output = slider.initialize_slider(screen, 200, 500, 400, 0, 1, 0.01)


def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True
def main():
    running = True

    while running:
        color = color_slider.getValue()
        density = density_slider.getValue()

        test_shader.program['fogColor'] = (color, color, color)
        test_shader.program['fogDensity'] = density

        running = event_checker()
        screen.blit(test_image, (0, 0))
        slider.draw_slider(color_slider, color_output, "Color")
        slider.draw_slider(density_slider, density_output, "Density")

        test_shader.update_textures([screen])





        test_shader.render()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()