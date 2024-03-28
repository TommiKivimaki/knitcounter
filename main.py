# import launcher  # noqa F401

import badger2040
badger = badger2040.Badger2040()

# Constants
WIDTH, HEIGHT = badger.get_bounds() # (296, 128)

# Counters in global scope
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

# Uses the screen width information to right align text
def display_right_align(text, y, scale):
    text_width = badger.measure_text(text, scale)
    badger.text(text, WIDTH - text_width, y, scale=scale)   

def display_right_align_partial_update(counter, text, y, scale):
    init_screen_update()
    text_width = badger.measure_text(text, scale)
    badger.text(text, WIDTH - text_width, y, scale=scale)
    ya = 16 if counter == "A" else 80
    badger.partial_update(WIDTH - text_width, ya, text_width, 32)   
    
def partial_update_label_B(value):
    display_right_align_partial_update("B", str(value), 95, 1) # counterB label
    
def partial_update_label_A(value):
    display_right_align_partial_update("A", str(value), 35, 1) # counterA label
    
# Resets counter value and updates the labels
def reset_counter(counter):
    if counter == "A":
        update_counter("counterA", 0)
    elif counter == "B":
        update_counter("counterB", 0)
    
    update_labels(counterA, counterB) 
    
# updates counterA and counterB labels and updates the whole screen.  
def update_labels(valueA, valueB):
    init_screen_update()
    display_right_align(str(valueA), 35, 1) # counterA label
    display_right_align(str(valueB), 95, 1) # counterB label
    update_screen()
    
# Updates the global counter values and persists the values to files
def update_counter(counter, value):
    global counterA
    global counterB
    
    if counter == "counterA":
        counterA = value
    elif counter == "counterB":
        counterB = value
        
    if counter == "counterA" or counter == "counterB":    
        filename = counter + ".txt"
        file = open(filename, "w")
        file.write(str(value))
        file.close()

# Gets saved counter value from a file
def get_saved_value(counter):
    filename = counter + ".txt"
    value = 0 # default value
    
    try:
        file = open(filename, "r")
        read_value = file.read()
        file.close()
        value = int(read_value)
    except:
        value = 0 # Just keep the default value
        print("except")

    return value

# Get's saved counter values and calls update on them
def restore_counters():
    valueA = get_saved_value("counterA")
    valueB = get_saved_value("counterB")
        
    update_counter("counterA", valueA)
    update_counter("counterB", valueB)

# Handles all that's needed in the initialization of thr board
def initialize_badger():
    badger.led(111)
    badger.set_update_speed(0) # normal = best quality and slowest for the first draw
    restore_counters()
    global counterA
    global counterB
    update_labels(counterA, counterB)
    badger.set_update_speed(2) # fast = lower quality but quicker. Affects also partial_update() speed

#######
# Start
#######

initialize_badger()

while True:
    if badger.pressed(badger2040.BUTTON_A):
        reset_counter("A")
    if badger.pressed(badger2040.BUTTON_B):
        reset_counter("B")
    if badger.pressed(badger2040.BUTTON_C):
        print("Button C")   
    if badger.pressed(badger2040.BUTTON_UP):
        newValue = counterA + 1
        update_counter("counterA", newValue)
        partial_update_label_A(newValue)
    if badger.pressed(badger2040.BUTTON_DOWN):
        newValue = counterB + 1
        update_counter("counterB", newValue)
        partial_update_label_B(newValue)