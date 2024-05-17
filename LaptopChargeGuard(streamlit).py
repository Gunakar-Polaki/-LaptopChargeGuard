import time
import psutil
from boltiot import Sms, Bolt
import streamlit as st

# Streamlit user inputs
st.title("Laptop Charge Guard [Battery Monitor with Bolt IoT]")
API_KEY = st.text_input("Enter your Bolt API Key", "")
DEVICE_ID = st.text_input("Enter your Bolt Device ID", "")
TO_NUMBER_INPUT = st.text_input("Enter your mobile number (10 digits)", "")
TO_NUMBER = f"+91{TO_NUMBER_INPUT}" if TO_NUMBER_INPUT else ""

# Constants
SID = 'ACe72fa30869d550609f3ecbe95c436110'  # Twilio Account SID
AUTH_TOKEN = 'ac68f99cff23cf83d9fa891d37c22f73'  # Twilio Auth Token
FROM_NUMBER = '+16362541170'  # Twilio Trial Number

# Initialize Bolt and SMS objects if credentials are provided
if API_KEY and DEVICE_ID and TO_NUMBER:
    mybolt = Bolt(API_KEY, DEVICE_ID)
    sms = Sms(SID, AUTH_TOKEN, TO_NUMBER, FROM_NUMBER)
else:
    st.warning("Please enter all required fields to start the monitoring process.")

def control_buzzer(pin, value):
    response = mybolt.digitalWrite(pin, value)
    st.write(f"Buzzer response: {response}")

def control_led(pin, value):
    response = mybolt.digitalWrite(pin, value)
    st.write(f"LED response: {response}")

blink_count = 5  # Number of times to blink the LED
interval = 20   # Time interval between consecutive API requests in seconds

if 'monitoring' not in st.session_state:
    st.session_state.monitoring = False

def start_monitoring():
    st.session_state.monitoring = True

def stop_monitoring():
    st.session_state.monitoring = False

st.button('Start Monitoring', on_click=start_monitoring)
st.button('Stop Monitoring', on_click=stop_monitoring)

if st.session_state.monitoring:
    st.write("Monitoring started...")
    while st.session_state.monitoring:
        battery = psutil.sensors_battery()
        plugged = battery.power_plugged
        percent = battery.percent

        if percent == 100 and plugged:
            st.write("Battery Full - Light and Sound Alert!")
            response = sms.send_sms("ALERT: Battery Full - Light and Sound Alert!")
            control_buzzer('0', 'HIGH')  # Turn on the buzzer
            control_led('2', 'HIGH')  # Turn on the light
            time.sleep(10)
            control_buzzer('0', 'LOW')  # Turn off the buzzer
            control_led('2', 'LOW')  # Turn off the light

        elif 90 <= percent < 100:
            if plugged:
                st.write("Battery between 90-100% and plugged in - Light On")
                response = sms.send_sms("ALERT: Battery between 90-100% and plugged in - Light On")
                control_led('2', 'HIGH')  # Turn on the light
                control_buzzer('0', 'LOW')  # Turn off the buzzer
            else:
                st.write("Battery between 90-100% and not plugged in - Light Blinking")
                response = sms.send_sms("ALERT: Battery between 90-100% and not plugged in - Light Blinking")
                for _ in range(blink_count):  # Blink the light
                    control_led('2', 'HIGH')  # Turn on the light
                    control_buzzer('0', 'HIGH')  # Turn on the buzzer
                    time.sleep(1)  # Wait for 1 second
                    control_led('2', 'LOW')  # Turn off the light
                    control_buzzer('0', 'LOW')  # Turn off the buzzer
                    time.sleep(1)  # Wait for 1 second
            control_led('2', 'LOW')  # Ensure the LED is off after blinking

        else:
            st.write("Charging is sufficient or Battery not in the specified range")
            control_led('1', 'LOW')  # Turn off the light
            control_led('2', 'LOW')  # Turn off the light
            control_buzzer('0', 'LOW')  # Ensure the buzzer is off

        time.sleep(interval)  # Wait for the specified interval before making the next API call
else:
    st.write("Monitoring stopped.")
