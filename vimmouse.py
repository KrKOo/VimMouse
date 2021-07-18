from pynput import keyboard
from pynput.mouse import Button, Controller
import signal
import sys

mouse = Controller()

# Set of currently pressed keys
current = set()

# The state of mouse control
ENABLED = False

# Shift + direction
SHIFT_MOVE_SIZE = 250

# Ctrl + direction
CTRL_MOVE_SIZE = 20

# Shift + Ctrl + direction
SHIFT_CTRL_MOVE_SIZE = 5

# Movement without modifiers
MOVE_SIZE = 50 

# Scroll
SCROLL_SIZE = 1

# List of keyboard combinations to handle
COMBINATIONS = [
    # LEFT MOVEMENT
    ({keyboard.Key.shift,
     keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('H')}, lambda: moveLeftHandler(SHIFT_CTRL_MOVE_SIZE)),

    ({keyboard.Key.shift,
     keyboard.KeyCode.from_char('H')}, lambda: moveLeftHandler(SHIFT_MOVE_SIZE)),

    ({keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('h')}, lambda: moveLeftHandler(CTRL_MOVE_SIZE)),

    ({keyboard.KeyCode.from_char('h')}, lambda: moveLeftHandler(MOVE_SIZE)),

    # DOWN MOVEMENT
    ({keyboard.Key.shift,
     keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('J')}, lambda: moveDownHandler(SHIFT_CTRL_MOVE_SIZE)),

    ({keyboard.Key.shift,
     keyboard.KeyCode.from_char('J')}, lambda: moveDownHandler(SHIFT_MOVE_SIZE)),

    ({keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('j')}, lambda: moveDownHandler(CTRL_MOVE_SIZE)),

    ({keyboard.KeyCode.from_char('j')}, lambda: moveDownHandler(MOVE_SIZE)),

    # UP MOVEMENT
    ({keyboard.Key.shift,
     keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('K')}, lambda: moveUpHandler(SHIFT_CTRL_MOVE_SIZE)),

    ({keyboard.Key.shift,
     keyboard.KeyCode.from_char('K')}, lambda: moveUpHandler(SHIFT_MOVE_SIZE)),

    ({keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('k')}, lambda: moveUpHandler(CTRL_MOVE_SIZE)),

    ({keyboard.KeyCode.from_char('k')}, lambda: moveUpHandler(MOVE_SIZE)),

    # RIGHT MOVEMENT
    ({keyboard.Key.shift,
     keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('L')}, lambda: moveRightHandler(SHIFT_CTRL_MOVE_SIZE)),

    ({keyboard.Key.shift,
     keyboard.KeyCode.from_char('L')}, lambda: moveRightHandler(SHIFT_MOVE_SIZE)),

    ({keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('l')}, lambda: moveRightHandler(CTRL_MOVE_SIZE)),

    ({keyboard.KeyCode.from_char('l')}, lambda: moveRightHandler(MOVE_SIZE)),


    # SCROLL
    ({keyboard.Key.alt,
     keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('j')}, lambda: mouse.scroll(0, -SCROLL_SIZE)),

    ({keyboard.Key.alt,
     keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('k')}, lambda: mouse.scroll(0, SCROLL_SIZE)),

    ({keyboard.Key.alt,
     keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('h')}, lambda: mouse.scroll(-SCROLL_SIZE, 0)),

    ({keyboard.Key.alt,
     keyboard.Key.ctrl,
     keyboard.KeyCode.from_char('k')}, lambda: mouse.scroll(SCROLL_SIZE, 0)),

    # CLICK
    ({keyboard.Key.space}, lambda: mouse.click(Button.left)),
    ({keyboard.Key.enter}, lambda: mouse.click(Button.left)),
    ({keyboard.Key.shift_r}, lambda: mouse.click(Button.right)),

    # EXIT
    ({keyboard.Key.esc}, lambda: exitMouseMode())
]

# Listen for the ENABLE key
def startListener(key):
    global ENABLED
    try:
        # Enable mouse control with F9
        if key == keyboard.Key.f9:
            ENABLED = True
            raise keyboard.Listener.StopException
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def exitMouseMode():
    global ENABLED
    ENABLED = False
    current.clear()
    raise keyboard.Listener.StopException


def moveLeftHandler(n):
    mouse.move(-n, 0)


def moveRightHandler(n):
    mouse.move(n, 0)


def moveUpHandler(n):
    mouse.move(0, -n)


def moveDownHandler(n):
    mouse.move(0, n)


def on_press(key):
    current.add(key)

    for combination in COMBINATIONS:
        if current == combination[0]:
            combination[1]()


def on_release(key):
    try:
        # fixes problem with the release order of shift required symbols
        if(key == keyboard.Key.shift):
            current.clear()

        current.remove(key)
    except KeyError:
        pass


# Listen for key events when mouse control is enabled
def getMouseModeListener():
    return keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True)

# Listen for key events when mouse control is disabled
def getStartListener():
    return keyboard.Listener(on_press=startListener)


def main():
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))

    listener = None
    while(True):
        if(ENABLED):
            listener = getMouseModeListener()
        else:
            listener = getStartListener()

        with listener:
            listener.wait()
            listener.join()


if __name__ == '__main__':
    main()
