from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import websocket
import json
import threading
import urllib.parse
from twilio.rest import Client
import time
import pygame
import keyboard
import requests
import datetime

def Location():

    #Get Info
    response = requests.get("https://ipinfo.io")
    
    if response.status_code == 200:
        data = response.json()
       
        city = data.get("city")
        region = data.get("region")
        country = data.get("country")
        location = data.get("loc")
        y = location,[city,region,country]
    else:
        print("Failed to retrieve geolocation information.")

    x = (y[0]).split(',')
    lat = x[0]
    lon = x[1]

    lat_lon = f"{lat},{lon}"
    base_url = "https://www.google.com/maps/search/"
    params = {"api": 1, "query": lat_lon}
    url = base_url + "?" + urllib.parse.urlencode(params)

    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")

    return(url, y[0], y[1], current_time)

def Send_Text():
    content = Location()
    text = (f"""
          EMERGENCY at {content[1]} \n ({content[2][0]}, {content[2][1]}, {content[2][2]})
          \nCar accident on highway with injuries. Need ambulance and police assistance immediately. 
          
          Time of Accident: {content[3]}
          Link To The Location: 
          {content[0]}
          """)
    #Auth And SID
    sid = "AC32d193612554c3838e66a0d927c7b9fb"
    auth = "9ec3883047408abef629fe6d0b362cac"
    client = Client(sid,auth)

    #Messaging Number
    from_no = "+15637702700"
    to_no = "+918618856297"
    
    #Sending Text
    message = client.messages.create(
        body = text,
        from_=from_no,
        to=to_no
    )

def Module_3():
    #shared data
    x_data = []
    y_data = []
    z_data = []
    time_data = []

    x_data_color = "#d32f2f"   # red
    y_data_color = "#7cb342"   # green
    z_data_color = "#0288d1"   # blue

    background_color = "#fafafa" # white (material)

    for i in range(20):
        print("\n")


    class Sensor:
        #constructor
        def __init__(self,address,sensor_type):
            self.address = address
            self.sensor_type = sensor_type
        
        # called each time when sensor data is recieved
        def on_message(self,ws, message):
            values = json.loads(message)['values']
            timestamp = json.loads(message)['timestamp']

            x_data.append(values[0])
            y_data.append(values[1])
            z_data.append(values[2])

            time_data.append(float(timestamp/1000000))

        def on_error(self,ws, error):
            print("\nError Occured")
            print(error)

        def on_close(self,ws, close_code, reason):
            print("\nConnection Closed")
            print("Close Code : ", close_code)
            print("Close Reason : ", reason  )

        def on_open(self,ws):
            print(f"\nConnection Succesful : {self.address}")

        # Call this method on seperate Thread
        def make_websocket_connection(self):
            ws = websocket.WebSocketApp(f"ws://192.168.1.12:8080/sensor/connect?type={self.sensor_type}",
                                    on_open=self.on_open,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

            # blocking call
            ws.run_forever() 
        
        # make connection and start recieving data on sperate thread
        def connect(self):
            thread = threading.Thread(target=self.make_websocket_connection)
            thread.start()           



    class MainWindow(QtWidgets.QMainWindow):

        def __init__(self, *args, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)

            self.graphWidget = pg.PlotWidget()
            self.setCentralWidget(self.graphWidget)

            self.graphWidget.setBackground(background_color)

            self.graphWidget.setTitle("Accelerometer Plot", color="#8d6e63", size="20pt")
            
            # Add Axis Labels
            styles = {"color": "#f00", "font-size": "15px"}
            self.graphWidget.setLabel("left", "m/s^2", **styles)
            self.graphWidget.setLabel("bottom", "Time (miliseconds)", **styles)
            self.graphWidget.addLegend()

            self.x_data_line =  self.graphWidget.plot([],[], name="x", pen=pg.mkPen(color=x_data_color))
            self.y_data_line =  self.graphWidget.plot([],[], name="y", pen=pg.mkPen(color=y_data_color))
            self.z_data_line =  self.graphWidget.plot([],[], name="z", pen=pg.mkPen(color=z_data_color))
        
            self.timer = QtCore.QTimer()
            self.timer.setInterval(50)
            self.timer.timeout.connect(self.update_plot_data) # call update_plot_data function every 50 milisec
            self.timer.start()

        def update_plot_data(self):
            
            # limit lists data to 1000 items 
            limit = -1000 

            # Update the data.
            self.x_data_line.setData(time_data[limit:], x_data[limit:])  
            self.y_data_line.setData(time_data[limit:], y_data[limit:])
            self.z_data_line.setData(time_data[limit:], z_data[limit:])
            for item in z_data[limit:]:
                print (item)
            for item in z_data[limit:]:
                k = item+1
                if k-item >= 20:
                    print ("crash")
                    break
                else:
                    item = item + 1

        def detect_crash(self):
            # Detect a crash based on a sudden change in acceleration (greater than 20 m/s^2)
            threshold = 20

            if len(x_data) >= 2:
                # Get the most recent acceleration values
                current_x_acceleration = x_data[-1]
                current_y_acceleration = y_data[-1]
                current_z_acceleration = z_data[-1]

                
                prev_x_acceleration = x_data[-2]
                prev_y_acceleration = y_data[-2]
                prev_z_acceleration = z_data[-2]

                
                delta_x_acceleration = abs(current_x_acceleration - prev_x_acceleration)
                delta_y_acceleration = abs(current_y_acceleration - prev_y_acceleration)
                delta_z_acceleration = abs(current_z_acceleration - prev_z_acceleration)

                # Check if any axis's acceleration change is greater than the threshold
                if (
                    delta_x_acceleration > threshold
                    or delta_y_acceleration > threshold
                    or delta_z_acceleration > threshold
                ):
                    try:
                        print("\n")
                        print("           VEHICLE CRASH DETECTED           ")
                        print("CONTACTING FIRST RESPONDERS / EMERGENCY HELP")
                        print("\n")

                        pygame.init()
                        pygame.mixer.music.load("D:\Code Of Honour\Mod2\Alarm.mp3")
                        pygame.mixer.music.set_endevent(pygame.USEREVENT)
                        pygame.mixer.music.play()

                        for i in range(10,0,-1):                            
                                print(f"{i} Sec Util Emergency Help...")
                                
                                if keyboard.is_pressed('q'):
                                    pygame.mixer.music.stop()
                                    break                       

                                if i==1:
                                    Send_Text()
                                    print("\nEmergency call initiated with ID : SOS-003-LXZ ")
                                    break
                                time.sleep(1)

                                for event in pygame.event.get():
                                    if event.type == pygame.USEREVENT:
                                        pygame.mixer.music.play()
                        
                        pygame.mixer.music.stop()

                    except KeyboardInterrupt():
                        pass
                    
        def update_plot_data(self):
            # Limit lists data to 1000 items
            limit = -1000

            # Update the data.
            self.x_data_line.setData(time_data[limit:], x_data[limit:])
            self.y_data_line.setData(time_data[limit:], y_data[limit:])
            self.z_data_line.setData(time_data[limit:], z_data[limit:])

            # Detect a crash
            self.detect_crash()


    sensor = Sensor(address = "192.168.0.102:8081", sensor_type="android.sensor.accelerometer")
    sensor.connect() # asynchronous call


    app = QtWidgets.QApplication(sys.argv)

    # call on Main thread
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())        
    #End Of Code

if __name__ == "__main__":
    Module_3()
    