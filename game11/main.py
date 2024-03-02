import pygame
import random
import os
import sys

pygame.init()

WIDTH, HEIGHT = 1234, 705
FPS = 30
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симулятор броска монеты")

coin_folder = "images"
coin_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(coin_folder, "heads.png")), (150, 150)),
    pygame.transform.scale(pygame.image.load(os.path.join(coin_folder, "tails.png")), (150, 150))
]

animation_folder = "animation"
animation_frames = [pygame.transform.scale(pygame.image.load(os.path.join(animation_folder, f"coin_animation_{i}.png")), (150, 150)) for i in range(1, 12)]

button_font = pygame.font.SysFont("monospace", 27)
button_text = button_font.render(" Бросить монету ", True, BLUE)
button_rect = button_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
bet_text = button_font.render("Сделать ставку", True, BLUE)
bet_rect = bet_text.get_rect(center=(WIDTH // 4, HEIGHT - 50))

result_font = pygame.font.Font(None, 48)

is_flipping = False
animation_speed = 0
current_frame = 0
result_text = ""
coin_chosen = False  # Переменная для отслеживания выбора монеты
animation_triggered = False  # Переменная для отслеживания, была ли включена анимация


count_heads = 3
count_tails = 3

clock = pygame.time.Clock()
running = True
pygame.mixer.init()
flip_sound = pygame.mixer.Sound(os.path.join("sounds", "zvukk.mp3"))

place_bet = False
user_choice = None

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not is_flipping:
            if button_rect.collidepoint(mouse_x, mouse_y):
                if not place_bet:
                    is_flipping = True
                    animation_speed = 0
                    current_frame = 0
                    result_text = ""
                    flip_sound.play()
                else:
                    if user_choice is not None:
                        result_number = random.randint(1, 2)
                        result_text = "Орел" if result_number == 1 else "Решка"

                        if result_text == "Орел" and user_choice == "Heads":
                            count_heads += 1
                        elif result_text == "Решка" and user_choice == "Tails":
                            count_tails += 1
                        else:
                            count_tails -= 1

                        user_choice = None



            # Обработка нажатия кнопки "Сделать ставку"
            elif not place_bet and bet_rect.collidepoint(mouse_x, mouse_y):
                place_bet = True

            # Обработка нажатия кнопок выбора стороны "Орел" и "Решка"
            elif place_bet and user_choice is None:
                if heads_rect.collidepoint(mouse_x, mouse_y):
                    user_choice = "Heads"
                    coin_chosen = True
                elif tails_rect.collidepoint(mouse_x, mouse_y):
                    user_choice = "Tails"
                    coin_chosen = True

        # Обработка отпускания кнопок (все кнопки, где нужно)
        elif event.type == pygame.MOUSEBUTTONUP:
            if not place_bet and bet_rect.collidepoint(mouse_x, mouse_y):
                # Отпускание кнопки "Сделать ставку"
                place_bet = True
            # Отпускание кнопок выбора стороны "Орел" и "Решка"
            elif place_bet and user_choice is None:
                if heads_rect.collidepoint(mouse_x, mouse_y):
                    user_choice = "Heads"
                elif tails_rect.collidepoint(mouse_x, mouse_y):
                    user_choice = "Tails"


    mouse_x, mouse_y = pygame.mouse.get_pos()
    if count_heads <= 0 or count_tails <= 0:
        game_over_text = result_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect.topleft)
        pygame.display.flip()
        pygame.time.delay(2000)
        running = False

    pygame.draw.rect(screen, WHITE, bet_rect, border_radius=10)
    screen.blit(bet_text, bet_rect.topleft)

    if not place_bet and bet_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, (200, 200, 200), bet_rect, border_radius=10)
    elif not place_bet:
        pygame.draw.rect(screen, WHITE, bet_rect, border_radius=10)

    pygame.draw.rect(screen, WHITE, button_rect, border_radius=10)
    screen.blit(button_text, button_rect.topleft)

    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, (200, 200, 200), button_rect, border_radius=10)

    if is_flipping:
        animation_speed += 1
        if animation_speed >= len(animation_frames) * 4:
            is_flipping = False
            result_number = random.randint(1, 2)
            result_text = "Орел" if result_number == 1 else "Решка"
            if result_text == "Решка":
                current_frame = 6 * 4
                flip_sound.stop()

            if result_text == "Орел":
                count_heads += 1
            elif result_text == "Решка":
                count_tails += 1

    if coin_chosen and not is_flipping:
        is_flipping = True
        animation_speed = 0
        current_frame = 0
        result_text = ""
        flip_sound.play()
        coin_chosen = False

    bg = pygame.image.load("imgonline-com-ua-Resize-qLAL0SbRqXmhl5.jpg")
    screen.blit(bg, (0, 0))

    if is_flipping:
        current_frame = (current_frame + 1) % (len(animation_frames) * 4)
        screen.blit(animation_frames[current_frame // 4], (WIDTH // 2 - 75, HEIGHT // 2 - 75))
    else:
        if result_text == "Орел":
            screen.blit(coin_images[0], (WIDTH // 2 - 75, HEIGHT // 2 - 75))
        elif result_text == "Решка":
            screen.blit(coin_images[1], (WIDTH // 2 - 75, HEIGHT // 2 - 75))

    pygame.draw.rect(screen, WHITE, button_rect, border_radius=10)
    screen.blit(button_text, button_rect.topleft)

    if result_text != "":
        result_surface = result_font.render(result_text, True, BLUE)
        result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(result_surface, result_rect.topleft)

    counter_text = result_font.render(f"Орел: {count_heads}   Решка: {count_tails}", True, WHITE)
    counter_rect = counter_text.get_rect(topleft=(20, 20))
    screen.blit(counter_text, counter_rect.topleft)

    if not place_bet:
        bet_text = button_font.render("Сделать ставку", True, BLUE)
        bet_rect = bet_text.get_rect(center=(WIDTH // 4, HEIGHT - 50))
        pygame.draw.rect(screen, WHITE, bet_rect, border_radius=10)
        screen.blit(bet_text, bet_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bet_rect.collidepoint(event.pos):
                    place_bet = True

    elif place_bet and user_choice is None:
        choice_text = button_font.render("Выберите сторону", True, BLUE)
        heads_button_text = button_font.render("Орел", True, BLUE)
        tails_button_text = button_font.render("Решка", True, BLUE)

        choice_rect = choice_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        heads_rect = heads_button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
        tails_rect = tails_button_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
        pygame.draw.rect(screen, WHITE, choice_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, heads_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, tails_rect, border_radius=10)

        screen.blit(choice_text, choice_rect.topleft)
        screen.blit(heads_button_text, heads_rect.topleft)
        screen.blit(tails_button_text, tails_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if heads_rect.collidepoint(event.pos):
                    user_choice = "Heads"
                elif tails_rect.collidepoint(event.pos):
                    user_choice = "Tails"

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()