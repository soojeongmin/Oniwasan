
import time
from evdev import InputDevice, categorize, ecodes                   # pip install evdev
gamepad = InputDevice('/dev/input/MY_CONTROLLER_EVENT_NUMBER')      # "cd /dev/input" then "ls -al" to see your connections

button_presses = {                          # ecodes.EV_KEY
    304: 'a',
    305: 'b',
    307: 'x',
    308: 'y',
    310: 'topLeft',
    311: 'topRight',
    314: 'select',
    315: 'start',
}

button_values = {                           # ecodes.EV_KEY button press values
    0: 'up',
    1: 'down'
}

arrowpad_codes = {
    0: 'left-right arrows',
    1: 'up-down arrows'
}

arrowpad_left_right_values = {
    0: 'left pressed',
    127: 'released',
    255: 'right pressed'
}

arrowpad_up_down_values = {
    0: 'up pressed',
    127: 'released',
    255: 'down pressed'
}

if __name__ == '__main__':
    print(gamepad)

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_KEY and event.code in button_presses:                # any button press other than leftpad
            button, direction = button_presses[event.code], button_values[event.value]
            print(f'{button} {direction}')

        if event.type == ecodes.EV_ABS and event.code in arrowpad_codes:
            arrow, action = 'unknown arrow', 'unknown action'
            if event.code == 0 and event.value in arrowpad_left_right_values:           # left-right arrows
               arrow = 'left/right'
               action = arrowpad_left_right_values[event.value]
            elif event.code == 1 and event.value in arrowpad_up_down_values:            # up-down arrows
                arrow = 'up/down'
                action = arrowpad_up_down_values[event.value]

            print(f'{arrow}: {action}')
