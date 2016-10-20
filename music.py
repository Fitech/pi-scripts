import random
import time
from pygame import mixer

print("Play a song")
mixer.init()
mixer.music.load("RockNRoll.mp3")
mixer.music.play()

while mixer.music.get_busy() == True:
    continue
print("Played Rock")