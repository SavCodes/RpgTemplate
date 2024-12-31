
import shader
import pygame

from shader import full_screen_blood_burst_frag_shader

#FRAG_SHADER = shader.wild_frag_shader
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600), pygame.OPENGL | pygame.DOUBLEBUF)
test_img = pygame.image.load('./game_assets/concept_art/start_menu_2.png')
test_shader = shader.ShaderManager(_frag_shader=full_screen_blood_burst_frag_shader)

# ================ ENABLE FOR TECHNO MAGIC SHIELD SHADER ================
# test_shader.wild_program['u_resolution'] = (screen.width, screen.height)

# test_shader.wild_program['soft_radius'] = 0.3   # Inner Ring Radius
# test_shader.wild_program['hard_radius'] = 0.5   # Outer Ring Radius



def event_checker():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def main():
    running = True
    x = (0, 0)
    while running:
        screen.blit(test_img, (0, 0))
        running = event_checker()
        # test_shader.apply_vignette(0.6)
        # test_shader.apply_side_warble(4)
        # test_shader.apply_ripple(0.1)
        # test_shader.apply_side_shadow_scroll(10)
        # test_shader.program['blood_burst'] = 10
        # test_shader.update_textures([screen])
        # test_shader.render()


        # test_shader.program['center'] = (pygame.mouse.get_pos()[0] / screen.get_width(), pygame.mouse.get_pos()[1] / screen.get_height())
        # test_shader.program['fall_speed'] = 10
        # test_shader.program['pulse_speed'] = 10
        # test_shader.program['particle_color'] = (1.0, 0.8, 0.9, 1.0)
        # test_shader.program['particle_color'] = (1.0, 1.0, 1.0, 1.0)
        # test_shader.wild_program['resolution'] = (screen.get_width(), screen.get_height())
        # test_shader.program['time'] = pygame.time.get_ticks() / 10000.0
        # test_shader.program['burst_color'] = (1.0, 0.8, 0.9, 1.0)
        # test_shader.program['origin'] = pygame.mouse.get_pos()[0]/ screen.get_width(), pygame.mouse.get_pos()[1]/ screen.get_height()
        # test_shader.program['fog_intensity'] = 0.01
        x = (x[0] + 0.01, x[1] + 0.01)
        test_shader.update_textures([screen])
        test_shader.render()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()