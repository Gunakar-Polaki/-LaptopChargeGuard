### Project Description: Laptop Charge Guard using Bolt IoT

**Objective**:
The goal of this project is to monitor the battery status of a laptop and provide real-time alerts through SMS and visual/audio signals using Bolt IoT and Twilio services. The system will alert the user when the battery is fully charged, when the battery is between 90-100%, and whether the laptop is plugged in or not.

**Components**:
1. **Bolt IoT Module**: A Wi-Fi-enabled microcontroller that communicates with sensors and actuators.
2. **Buzzer**: To provide audio alerts.
3. **LED**: To provide visual alerts.
4. **Twilio API**: To send SMS alerts to the user's phone.
5. **Laptop**: The device whose battery status is being monitored.

**Connections**:
1. **Bolt IoT Module**:
   - Connect the positive pin of the buzzer to digital pin `0` of the Bolt module.
   - Connect the positive pin of the LED to digital pin `2` of the Bolt module.
   - Connect the negative pins of both the buzzer and the LED to the ground (GND) pin of the Bolt module.

**Working**:
1. **Initialization**:
   - The Bolt IoT module and Twilio SMS service are initialized using their respective API keys and authentication tokens.
   - The user's phone number is also configured to receive SMS alerts.

2. **Battery Monitoring Loop**:
   - The system enters an infinite loop where it continuously monitors the laptop's battery status using the `psutil` library.
   - The battery status is checked every 20 seconds.

3. **Alert Conditions**:
   - **Battery Full (100% and plugged in)**:
     - A message is sent to the user's phone via Twilio.
     - The buzzer and LED are turned on for 10 seconds.
   - **Battery between 90-100%**:
     - **If plugged in**: The LED is turned on, and a message is sent to the user.
     - **If not plugged in**: The LED and buzzer blink five times, with each blink lasting for 1 second.
   - **Other Conditions**:
     - A message is sent to indicate that the battery is not in the specified range, and all alerts are turned off.


### Detailed Explanation:

1. **Imports and Configuration**:
   - The necessary libraries are imported: `time` for sleep intervals, `psutil` for accessing battery status, and `boltiot` for interacting with the Bolt IoT module and Twilio SMS service.
   - The Bolt IoT module and Twilio service are configured using their respective API keys and tokens.

2. **Initialization**:
   - `mybolt` and `sms` objects are created for controlling the Bolt IoT module and sending SMS alerts.

3. **Control Functions**:
   - `control_buzzer(pin, value)`: Sends a command to the Bolt IoT module to turn the buzzer on or off.
   - `control_led(pin, value)`: Sends a command to the Bolt IoT module to turn the LED on or off.

4. **Main Loop**:
   - The loop runs indefinitely, checking the laptop's battery status every 20 seconds.
   - Depending on the battery percentage and whether the laptop is plugged in, different actions are taken:
     - If the battery is full and plugged in, both the buzzer and LED are activated for 10 seconds.
     - If the battery is between 90-100%:
       - If plugged in, the LED is turned on.
       - If not plugged in, the LED and buzzer blink five times.
     - For other battery levels, a notification is sent, and all alerts are turned off.

5. **Alerts and Actions**:
   - SMS alerts are sent to the user based on the battery status.
   - The buzzer and LED provide visual and audio alerts to the user.

This project provides a practical solution for monitoring and managing laptop battery charging, helping to avoid overcharging and extend battery life.
