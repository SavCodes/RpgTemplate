import shader
import pygame
import random
import numpy as np

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
    f_color = vec4(col, 1.0);
}
'''


#FRAG_SHADER = shader.wild_frag_shader
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600), pygame.OPENGL | pygame.DOUBLEBUF)
test_shader = shader.ShaderManager(_frag_shader=point_glow_shader)

def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True


# Generate 50 random positions within the screen resolution (e.g., 1920x1080)
num_points = 50
random_positions = np.random.rand(num_points, 2) * [screen.width, screen.height]


# Assuming 'shader_program' is the compiled shader program
test_shader.program['color'] = (0,1,1)
test_shader.program['resolution'] = [screen.width, screen.height]
test_shader.program['point_size'] = 0.0005

def particle_drifter(shader, positions):
    for position in positions:
        position[0] += random.randint(30,50) / 10
        position[1] += random.randint(40,50) / 10

    positions[:, 1] %= screen.height
    positions[:, 0] %= screen.width
    shader.program['positions'] = positions

def main():
    running = True
    while running:
        particle_drifter(test_shader, random_positions)
        running = event_checker()
        test_shader.update_textures([screen])
        test_shader.render()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()