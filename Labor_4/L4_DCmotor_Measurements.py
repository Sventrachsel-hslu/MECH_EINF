"""-----------------------------------------------------
¦    File name: L4_DCmotor_Measurement.py               ¦
¦    Version: 1.0                                       ¦
¦    Author: Jonas Josi                                 ¦
¦    Date created: 2024/05/01                           ¦
¦    Last modified: 2024/05/01                          ¦
¦    Python Version: 3.7.3                              ¦
------------------------------------------------------"""

# ----------- import external Python module -----------
import pigpio  # library to create hardware-based PWM signals on Raspberry Pi
import time

# ----------- global constant -----------
# assign motor driver interface to GPIO's of Raspberry Pi
M1 = 20
M2 = 21
D1 = 26  # enable/disable output pins M1, M2

# settings
VOLTAGE = 6  # *** CHANGE ME *** Voltage for DC motor [V] between 0 und 12 V (Voltage from power supply is always 12 V)
MOVEMENT_DRIVE_TIME = 2  # *** CHANGE ME *** Time in [s] to drive the DC motor for each movement
MOVEMENT_STOP_TIME = 2  # *** CHANGE ME ***  Pause in [s] between two consecutive movements (up/down) of slide on linear guideway
CYCLE_START_DIRECTION = 0  # *** CHANGE ME ***  Direction (0 or 1) of first movement of slide on linear guideway
CYCLE_NUMBER = 3  # *** CHANGE ME ***  Number of cycles (movement of slide on linear guideway in one direction, followed by movement in the opposite direction)

# auxiliary parameters
MAX_VOLTAGE = 12  # supply voltage of motor driver is 12 V (which equals the max. rated voltage of the DC motor)
PWM_FREQUENCY = 4000  # Hz
PWM_DUTYCYCLE_RESOLUTION = 8  # 8 bit -> value range of PWM_DUTYCYCLE is between 0 (OFF) and 255 (FULLY ON)
PWM_DUTYCYCLE = round((2 ** PWM_DUTYCYCLE_RESOLUTION - 1) / MAX_VOLTAGE * VOLTAGE, 0)  # PWM_DUTYCYCLE from 0 (OFF) to 255 bit (FULLY ON)


# ----------- function definition -----------
def stop_motor():
    """
    Set state of both output pins of the motor driver (M1, M2) to LOW (0 V).
    Then disable the motor driver output pins (M1, M2).
    """
    # enable motor driver output pins (M1 and M2)
    pi1.write(D1, 1)

    # set state of motor driver outputs (M1 and M2) to low (0 V)
    pi1.write(M1, 0)
    pi1.write(M2, 0)

    # disable motor driver output pins (M1 and M2)
    pi1.write(D1, 0)

    print("\nMotor stopped")


# ----------- main code -----------
if __name__ == "__main__":
    # initialize pigpio
    pi1 = pigpio.pi()  # Create an Object of class pigpio.pi

    # enable motor driver output pins (M1 and M2)
    pi1.write(D1, 1)

    # set frequency of PWM signal on outputs "M1" and "M2"
    pi1.set_PWM_frequency(M1, PWM_FREQUENCY)
    pi1.set_PWM_frequency(M2, PWM_FREQUENCY)

    """ start measurement """
    try:
        direction = CYCLE_START_DIRECTION
        cycle = 0
        # endless loop
        while cycle < CYCLE_NUMBER:
            if direction == 0:
                # set output "M2" on motor driver to low (0 V)
                pi1.write(M2, 0)
                # drive motor
                pi1.set_PWM_dutycycle(M1, PWM_DUTYCYCLE)
                time.sleep(MOVEMENT_DRIVE_TIME)
                # stop motor
                pi1.set_PWM_dutycycle(M1, 0)
            elif direction == 1:
                # set output "M1" on motor driver to low (0 V)
                pi1.write(M1, 0)
                # drive motor
                pi1.set_PWM_dutycycle(M2, PWM_DUTYCYCLE)
                time.sleep(MOVEMENT_DRIVE_TIME)
                # stop motor
                pi1.set_PWM_dutycycle(M2, 0)

            direction = not direction  # change direction
            cycle += 0.5

            # check if last movement of measurement is not already done
            if cycle != CYCLE_NUMBER:
                # wait between movements
                time.sleep(MOVEMENT_STOP_TIME)

        stop_motor()
        pi1.stop()  # Terminate the connection to the pigpiod instance and release resources
        print("Exit Python")
        exit(0)  # exit python with exit code 0

    # detect exception - usually triggered by a user input, stopping the script
    except KeyboardInterrupt:
        stop_motor()
        pi1.stop()  # Terminate the connection to the pigpiod instance and release resources
        print("Exit Python")
        exit(0)  # exit python with exit code 0