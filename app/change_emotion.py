def adjust(player, pitch, tempo, volume):
    player.update_pitch(pitch)
    player.update_tempo(tempo)
    player.update_volume(volume)


# Neutral
def neutral_to_happy(player):
    adjust(player, 1, 1.2, 1.2)

def neutral_to_sad(player):
    adjust(player, -1, 0.8, 0.8)
  
def neutral_to_angry(player):
    adjust(player, 1.5, 1.3, 1.4)
    
def neutral_to_fearful(player):
    adjust(player, 0.5, 1.1, 1.1)
    
def neutral_to_disgusted(player):
    adjust(player, -0.5, 0.9, 0.85)
    
def neutral_to_surprised(player):
    adjust(player, 2, 1.4, 1.5)


# Happy
def happy_to_neutral(player):
    adjust(player, -1, 0.8, 0.8)

def happy_to_sad(player):
    adjust(player, -2, 0.6, 0.7)
  
def happy_to_angry(player):
    adjust(player, 0.5, 1.1, 1.2)
    
def happy_to_fearful(player):
    adjust(player, -0.5, 0.9, 0.9)
    
def happy_to_disgusted(player):
    adjust(player, -1.5, 0.8, 0.75)
    
def happy_to_surprised(player):
    adjust(player, 1, 1.2, 1.3)


# Sad
def sad_to_neutral(player):
    adjust(player, 1, 1.2, 1.2)

def sad_to_happy(player):
    adjust(player, 2, 1.4, 1.3)
  
def sad_to_angry(player):
    adjust(player, 1.5, 1.3, 1.4)
    
def sad_to_fearful(player):
    adjust(player, 0.5, 1.1, 1.15)
    
def sad_to_disgusted(player):
    adjust(player, 0, 1.1, 1.1)
    
def sad_to_surprised(player):
    adjust(player, 2.5, 1.5, 1.5)


# Angry
def angry_to_neutral(player):
    adjust(player, -1.5, 0.7, 0.6)

def angry_to_happy(player):
    adjust(player, -0.5, 0.9, 0.8)
  
def angry_to_sad(player):
    adjust(player, -1.5, 0.7, 0.6)
    
def angry_to_fearful(player):
    adjust(player, -0.5, 0.8, 0.9)
    
def angry_to_disgusted(player):
    adjust(player, -1, 0.8, 0.85)
    
def angry_to_surprised(player):
    adjust(player, 0.5, 1.1, 1.1)


# Fearful
def fearful_to_neutral(player):
    adjust(player, -0.5, 0.9, 0.9)

def fearful_to_happy(player):
    adjust(player, 0.5, 1.2, 1.2)
  
def fearful_to_sad(player):
    adjust(player, -1, 0.8, 0.85)
    
def fearful_to_angry(player):
    adjust(player, 0.5, 1.2, 1.25)
    
def fearful_to_disgusted(player):
    adjust(player, -0.5, 0.9, 0.9)
    
def fearful_to_surprised(player):
    adjust(player, 1, 1.3, 1.4)


# Disgusted
def disgusted_to_neutral(player):
    adjust(player, 0.5, 1.1, 1.15)

def disgusted_to_happy(player):
    adjust(player, 1.5, 1.2, 1.25)
  
def disgusted_to_sad(player):
    adjust(player, -0.5, 0.9, 0.85)
    
def disgusted_to_angry(player):
    adjust(player, 1, 1.3, 1.3)
    
def disgusted_to_fearful(player):
    adjust(player, 0.5, 1.1, 1.1)
    
def disgusted_to_surprised(player):
    adjust(player, 1.5, 1.4, 1.35)


# Surprised
def surprised_to_neutral(player):
    adjust(player, -2, 0.6, 0.5)

def surprised_to_happy(player):
    adjust(player, -1, 0.8, 0.7)
  
def surprised_to_sad(player):
    adjust(player, -2.5, 0.5, 0.5)
    
def surprised_to_angry(player):
    adjust(player, -1.5, 0.7, 0.8)
    
def surprised_to_fearful(player):
    adjust(player, -1, 0.8, 0.85)
    
def surprised_to_disgusted(player):
    adjust(player, -1.5, 0.7, 0.75)
