def adjust(player, pitch_slider, tempo_slider, volume_slider, pitch, tempo, volume):
    player.update_pitch(pitch)
    player.update_tempo(tempo)
    player.update_volume(volume)
    pitch_slider.set(pitch)
    tempo_slider.set(tempo)
    volume_slider.set(volume)



# Neutral
def neutral_to_happy(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  1, 1.1, 1.2)

def neutral_to_sad(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.8, 0.8, 0.8)
  
def neutral_to_angry(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1.3, 1.4)
    
def neutral_to_fearful(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.2, 1.2, 1.1)
    
def neutral_to_disgusted(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -1, 0.9, 0.85)
    
def neutral_to_surprised(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.8, 1.4, 1.5)


# Happy
def happy_to_neutral(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0, 1, 1.2)

def happy_to_sad(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.8, 1.1, 1.3)
  
def happy_to_angry(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1.3, 1.2)
    
def happy_to_fearful(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.2, 1.1, 1.2)
    
def happy_to_disgusted(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.5, 0.8, 1.1)
    
def happy_to_surprised(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  1, 1.4, 1.3)


# Sad
def sad_to_neutral(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0, 1, 1.2)

def sad_to_happy(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.8, 1.1, 1.3)
  
def sad_to_angry(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1.3, 1.4)
    
def sad_to_fearful(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.2, 1.2, 1.15)
    
def sad_to_disgusted(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.5, 1.1, 1.1)
    
def sad_to_surprised(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  1.2, 1.5, 1.5)


# Angry
def angry_to_neutral(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1, 0.6)

def angry_to_happy(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0, 1.1, 0.8)
  
def angry_to_sad(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1, 0.6)
    
def angry_to_fearful(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.2, 1.2, 0.9)
    
def angry_to_disgusted(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.5, 1.3, 0.85)
    
def angry_to_surprised(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.5, 1.4, 1.1)


# Fearful
def fearful_to_neutral(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.2, 1, 0.9)

def fearful_to_happy(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.5, 1.1, 1.2)
  
def fearful_to_sad(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.8, 1.2, 0.85)
    
def fearful_to_angry(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1.3, 1.25)
    
def fearful_to_disgusted(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.2, 1.2, 0.9)
    
def fearful_to_surprised(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.8, 1.4, 1.4)


# Disgusted
def disgusted_to_neutral(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -1, 1, 1.15)

def disgusted_to_happy(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.8, 1.1, 1.25)
  
def disgusted_to_sad(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.5, 0.9, 0.85)
    
def disgusted_to_angry(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1.3, 1.3)
    
def disgusted_to_fearful(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.2, 1.2, 1.1)
    
def disgusted_to_surprised(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.8, 1.4, 1.35)


# Surprised
def surprised_to_neutral(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.8, 1, 0.5)

def surprised_to_happy(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  0.2, 1.1, 0.7)
  
def surprised_to_sad(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1.2, 0.5)
    
def surprised_to_angry(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.5, 1.3, 0.8)
    
def surprised_to_fearful(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.2, 1.4, 0.85)
    
def surprised_to_disgusted(player, pitch_slider, tempo_slider, volume_slider):
    adjust(player, pitch_slider, tempo_slider, volume_slider,  -0.5, 1.3, 0.75)
