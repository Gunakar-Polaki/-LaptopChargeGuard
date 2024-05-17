import time
import psutil
from boltiot import Sms, Bolt
import streamlit as st

st.title("Laptop Charge Guard [Battery Monitor with Bolt IoT]")

# Bolt IoT configuration
API_KEY = st.text_input("Enter your Bolt API Key", "")
DEVICE_ID = st.text_input("Enter your Bolt Device ID", "")
TO_NUMBER_INPUT = st.text_input("Enter your mobile number (10 digits)", "")
TO_NUMBER = f"+91{TO_NUMBER_INPUT}" if TO_NUMBER_INPUT else ""

# Twilio configuration
SID = st.text_input("Enter your Twilio Account SID", "")
AUTH_TOKEN = st.text_input("Enter your Twilio Auth Token", "")
FROM_NUMBER = st.text_input("Enter your Twilio Phone Number", "")

# Initialize Bolt and Twilio objects
mybolt = None
sms = None

if API_KEY and DEVICE_ID and TO_NUMBER and SID and AUTH_TOKEN and FROM_NUMBER:
    mybolt = Bolt(API_KEY, DEVICE_ID)
    sms = Sms(SID, AUTH_TOKEN, TO_NUMBER, FROM_NUMBER)
else:
    st.warning("Please enter all required fields to start the monitoring process.")

def control_buzzer(pin, value):
    if mybolt:
        response = mybolt.digitalWrite(pin, value)
        return response

def control_led(pin, value):
    if mybolt:
        response = mybolt.digitalWrite(pin, value)
        return response

blink_count = 5  
interval = 20   

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

def start_monitoring():
    st.session_state.monitoring = True
    st.experimental_rerun()

def stop_monitoring():
    st.session_state.monitoring = False

if st.button('Start Monitoring'):
    st.write("Monitoring started.")
    start_monitoring()

if st.button('Stop Monitoring'):
    st.write("Monitoring stopped.")
    stop_monitoring()

if st.session_state.monitoring:
    battery = psutil.sensors_battery()
    if battery:
        battery_percent = battery.percent
        plugged = battery.power_plugged

        if battery_percent == 100 and plugged:
            st.write("Battery Full - Light and Sound Alert!")
            if sms:
                response = sms.send_sms("ALERT: Battery Full - Light and Sound Alert!")
            control_buzzer('0', 'HIGH')  
            control_led('2', 'HIGH') 
            time.sleep(10)
            control_buzzer('0', 'LOW')  
            control_led('2', 'LOW')  

        elif 60 <= battery_percent < 100:
            if plugged:
                st.write("Battery between 90-100% and plugged in - Light On")
                if sms:
                    response = sms.send_sms("ALERT: Battery between 90-100% and plugged in - Light On")
                control_led('2', 'HIGH')  
                control_buzzer('0', 'LOW') 
            else:
                st.write("Battery between 90-100% and not plugged in - Light Blinking")
                if sms:
                    response = sms.send_sms("ALERT: Battery between 90-100% and not plugged in - Light Blinking")
                for _ in range(blink_count):  
                    control_led('2', 'HIGH')  
                    control_buzzer('0', 'HIGH')  
                    time.sleep(1)  
                    control_led('2', 'LOW')  
                    control_buzzer('0', 'LOW')  
                    time.sleep(1)  
                control_led('2', 'LOW')  

        else:
            st.write("Charging is sufficient or Battery not in the specified range")
            control_led('1', 'LOW')  
            control_led('2', 'LOW')  
            control_buzzer('0', 'LOW')  

    else:
        st.error("Unable to retrieve battery information.")

    time.sleep(interval) 
    st.experimental_rerun()
