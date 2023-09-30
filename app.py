import pygame
import random
from pygame.locals import *

pygame.init()

# Atur ukuran layar
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Warna
WHITE = (255, 255, 255)

# Titik sebagai karakter burung
bird_color = (255, 0, 0)  # Misalnya, gunakan warna merah
bird_radius = 10  # Ukuran titik burung

bird_x = 100
bird_y = SCREEN_HEIGHT // 2
bird_speed = 5  # Kecepatan naik/turun

# Pergerakan latar belakang
background_x = 0
background_speed = 2  # Kecepatan pergerakan latar belakang

# Kecepatan awal pipa
pipe_speed = 4  # Kecepatan pipa

# List untuk menyimpan pipa
pipes = []

# Variabel game over
game_over = False

# Variabel game active (untuk mengindikasikan apakah permainan sedang berjalan)
game_active = True

# Variabel skor
score = 0

# Variabel level
level = 1  # Dimulai dari level 1

# Variabel untuk melacak apakah skor telah ditambahkan saat melewati pipa
score_added = False

# Fungsi untuk membuat pipa baru secara acak
def create_pipe():
    pipe_height = random.randint(100, 400)
    pipe_x = SCREEN_WIDTH
    top_pipe = pygame.Rect(pipe_x, 0, 50, pipe_height)
    bottom_pipe = pygame.Rect(pipe_x, pipe_height + 150, 50, SCREEN_HEIGHT - pipe_height - 150)
    return top_pipe, bottom_pipe

# Inisialisasi pipa pertama
pipes.append(create_pipe())

# Font untuk teks "Game Over", "Press Space to Restart", skor, dan level
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Restart permainan jika tombol spasi ditekan setelah game over
        if event.type == KEYDOWN and event.key == K_SPACE:
            if game_over:
                bird_y = SCREEN_HEIGHT // 2
                pipes.clear()
                pipes.append(create_pipe())
                game_active = True  # Aktifkan kembali permainan
                score = 0  # Reset skor
                background_speed = 2  # Reset kecepatan latar belakang
                game_over = False  # Reset game over
                score_added = False  # Reset status penambahan skor
                level = 1  # Reset level ke level 1
                pipe_speed = 4 + (level - 1) * 0.1  # Mengatur ulang kecepatan pipa berdasarkan level

    if game_active:  # Hanya perbarui permainan jika sedang aktif
        # Mendeteksi input keyboard
        keys = pygame.key.get_pressed()

        if keys[K_w] or keys[K_UP]:
            bird_y -= bird_speed  # Bergerak ke atas
        if keys[K_s] or keys[K_DOWN]:
            bird_y += bird_speed  # Bergerak ke bawah

        # Pergerakan latar belakang
        background_x -= background_speed

        # Ciptakan efek loop pada latar belakang
        if background_x < -SCREEN_WIDTH:
            background_x = 0

        # Buat dan gerakkan pipa-pipa
        for top_pipe, bottom_pipe in pipes:
            top_pipe.x -= pipe_speed
            bottom_pipe.x -= pipe_speed

        # Hentikan pergerakan pipa saat game over
        if not game_active:
            pipes = []

        # Hapus pipa yang sudah keluar dari layar
        pipes = [(top_pipe, bottom_pipe) for top_pipe, bottom_pipe in pipes if top_pipe.right > 0]

        # Buat pipa baru jika yang pertama sudah cukup ke kiri
        if pipes and pipes[-1][0].right < SCREEN_WIDTH - 200:
            pipes.append(create_pipe())

        # Deteksi tabrakan antara karakter burung dan pipa
        for top_pipe, bottom_pipe in pipes:
            if bird_x + bird_radius > top_pipe.left and bird_x - bird_radius < top_pipe.right:
                if bird_y - bird_radius < top_pipe.bottom or bird_y + bird_radius > bottom_pipe.top:
                    game_active = False
                    game_over = True

        # Deteksi jika karakter burung melewati pipa dan tambahkan skor
        if pipes and bird_x > pipes[0][0].right:
            if not score_added:
                score += 1
                score_added = True
                # Peningkatan level setiap 10 poin
                if score % 10 == 0:
                    level += 1
                    # Peningkatan kecepatan pipa setiap naik level
                    pipe_speed = 4 + (level - 1) * 0.1
            pipes.pop(0)  # Hapus pipa yang sudah dilewati
        else:
            score_added = False

    # Bersihkan layar
    screen.fill(WHITE)

    # Gambar latar belakang yang bergerak
    pygame.draw.rect(screen, (0, 128, 255), (background_x, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Gambar titik sebagai karakter burung
    pygame.draw.circle(screen, bird_color, (bird_x, bird_y), bird_radius)

    # Gambar pipa-pipa
    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(screen, (0, 255, 0), top_pipe)
        pygame.draw.rect(screen, (0, 255, 0), bottom_pipe)

    # Tampilkan skor di pojok kanan atas
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_text_rect = score_text.get_rect(topleft=(SCREEN_WIDTH - 150, 20))
    screen.blit(score_text, score_text_rect)

    # Tampilkan level di pojok kiri atas
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    level_text_rect = level_text.get_rect(topleft=(20, 20))
    screen.blit(level_text, level_text_rect)

    if game_over:
        # Tampilkan teks "Game Over" di tengah layar
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        # Tampilkan teks "Press Space to Restart" di bawahnya
        restart_text = font.render("Press Space to Restart", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()

    # Mengakhiri permainan jika skor mencapai 100
    if score >= 100:
        game_active = False
        game_over = True

    clock.tick(60)

pygame.quit()
