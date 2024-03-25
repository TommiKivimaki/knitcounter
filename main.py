# import launcher  # noqa F401

import badger2040
badger = badger2040.Badger2040()

# Constants
WIDTH, HEIGHT = badger.get_bounds() # (296, 128)

# Counters
counterA = 0
counterB = 0

def init_screen_update():
    # Clear screen to white
    badger.set_pen(15)
    badger.clear()
    # Write with black
    badger.set_pen(0)
    badger.set_thickness(2)
    badger.set_font("sans")
    setup_reset_label()
    
def setup_reset_label():
    badger.text("RESET", 20, 120, scale=0.5)
    badger.line(40, 105, 40, 35)
    badger.line(40, 35, 165, 35)
    
    badger.text("RESET", 125, 120, scale=0.5)
    badger.line(145, 105, 145, 95)
    badger.line(145, 95, 165, 95)
    
def update_screen():
    badger.update()

def display_right_align(text, y, scale):
    text_width = badger.measure_text(text, scale)
    badger.text(text, WIDTH - text_width, y, scale=scale)

# Handles updating the counterA data in variable and the write data in display buffer
def update_counterA_to(value):
    counterA = value
    display_right_align(str(value), 35, 1)
    
def update_counterB_to(value):
    counterB = value
    display_right_align(str(value), 95, 1)

def reset_counter(counter):
    init_screen_update()
    
    if counter == "A":
        update_counterA_to(0)
        update_counterB_to(counterB)
    elif counter == "B":
        update_counterA_to(counterA)
        update_counterB_to(0)
    else:
        update_counterA_to(0)
        update_counterB_to(0)
    
    update_screen()  
    
def counter_labels_to(valueA, valueB):
    init_screen_update()
    update_counterA_to(valueA)
    update_counterB_to(valueB)
    update_screen()
    
def initialize_badger():
    # LED ON when we are running
    badger.led(111)
    reset_counter("AB")


###
# Start
###

initialize_badger()

# Read buttons
while True:
    if badger.pressed(badger2040.BUTTON_A):
        reset_counter("A")
    if badger.pressed(badger2040.BUTTON_B):
        reset_counter("B")
    if badger.pressed(badger2040.BUTTON_C):
        print("Button C")   
    if badger.pressed(badger2040.BUTTON_UP):
        counterA += 1
        counter_labels_to(counterA, counterB)
    if badger.pressed(badger2040.BUTTON_DOWN):
        counterB += 1
        counter_labels_to(counterA, counterB)
