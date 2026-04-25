import pygame
import os

class MusicPlayer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 36)

        self.playlist = [
            "week11/music_player/music/The Academy Allstars - Pocketful Of Sunshine - (muzmos.net).mp3",
            "week11/music_player/music/Fugees_-_Killing_Me_Softly_with_His_Song_48008079.mp3",
            "week11/music_player/music/Miki_Matsubara_-_Stay_With_Me_72255446.mp3"
        ]

        self.current = 0
        self.playing = False
        self.time = 0

    def play(self):
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        self.playing = True

    def next(self):
        self.current = (self.current + 1) % len(self.playlist)
        self.play()

    def previous(self):
        self.current = (self.current - 1) % len(self.playlist)
        self.play()

    def handle_key(self, key):
        if key == pygame.K_p:
            self.play()
        if self.playing and key == pygame.K_s:
            pygame.mixer.music.pause()
            self.playing = False
        elif not self.playing and key == pygame.K_s:
            pygame.mixer.music.unpause()
            self.playing = True
        elif key == pygame.K_n:
            self.next()
        elif key == pygame.K_b:
            self.previous()
        elif key == pygame.K_q:
            pygame.quit()

    def update(self):
        if not pygame.mixer.music.get_busy() and self.playing:
            self.next()
        

    def draw(self):
        track_name = os.path.basename(self.playlist[self.current])

        pos_ms = pygame.mixer.music.get_pos()
        pos_sec = max(0, pos_ms // 1000)
        minutes = pos_sec // 60
        seconds = pos_sec % 60


        time_text = f"{minutes}:{seconds:02}"

        text = self.font.render(f"Track: {track_name}", True, (255, 255, 255))
        timer = self.font.render(time_text, True, (255, 200, 0))
        status = self.font.render("Playing" if self.playing else "Stopped", True, (200, 200, 200))

        self.screen.blit(text, (50, 100))
        self.screen.blit(timer, (50, 150))
        self.screen.blit(status, (50, 200))