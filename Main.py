import sys
import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                                QVBoxLayout,QLabel,QLineEdit, QHBoxLayout,
                                        QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather",self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.exit_button = QPushButton("Exit",self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setWindowIcon(QIcon("icon.png"))
        #Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        hbox_exit = QHBoxLayout()
        hbox_exit.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox_exit.addWidget(self.exit_button)
        vbox.addLayout(hbox_exit)
        self.setLayout(vbox)
        #Align Text
        self.city_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        #Set names
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.exit_button.setObjectName("exit_button")
        self.description_label.setObjectName("description_label")
        # Set Style
        self.setStyleSheet("""
            QLabel,QPushButton {
                font-family: Arial;
            }
            QPushButton#get_weather_button {
                background-color: rgb(255, 255, 255);
                border: 1px solid;
                border-radius: 10px; 
                font-size: 30px;
                font-weight: bold;
            }
            QPushButton#get_weather_button:hover {
                background-color: rgba(0,0,0,0);
            }
            QLabel#city_label,QLineEdit#city_input{ 
                font-size: 40px;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QPushButton#exit_button{
                background-color: hsl(354, 91%, 55%);
                font-weight: bold;
                border: 1px solid;
                border-radius: 10px; 
                font-size: 30px;
                padding: 5px;
            }
            QPushButton#exit_button:hover{
                background-color: hsl(354, 91%, 75%);
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }            
        """)
        self.get_weather_button.clicked.connect(self.get_weather)
        self.exit_button.clicked.connect(self.close)
    def get_weather(self):
        api_key = "446c7521cca0808e04dd9a91625b3413"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"]==200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("Not Found\nCity not found")
                case 500:
                    self.display_error("Internal Server Error\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway\nPlease try again later")
                case 503:
                    self.display_error("Service Unavailable\nPlease try again later")
                case 504:
                    self.display_error("Gateway Timeout\nPlease try again later")
                case _:
                    self.display_error(f"HTTP Error occurred\nPlease try again later")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error\nPlease try again later")
        except requests.exceptions.TooManyRedirects:
            self.display_error("TooManyRedirects\nPlease try again later")
        except requests.exceptions.RequestException:
            self.display_error("Request Error\nPlease try again later")

    def display_error(self,message):
        self.emoji_label.clear()
        self.description_label.clear()
        self.temperature_label.setText(message)
        self.temperature_label.setStyleSheet("font-size: 30px;")

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature = data["main"]["temp"] - 273.15
        self.temperature_label.setText(f"{temperature:.0f}°C")
        self.description_label.setText(data["weather"][0]["description"])
        self.emoji_label.setText(self.get_weather_emoji(data["weather"][0]["id"]))

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id < 300:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id < 400:
            return "🌦️"  # Drizzle
        elif 500 <= weather_id < 600:
            return "🌧️"  # Rain
        elif 600 <= weather_id < 700:
            return "❄️"  # Snow
        elif 700 <= weather_id < 800:
            return "🌫️"  # Atmosphere (fog, dust, etc.)
        elif weather_id == 800:
            return "☀️"  # Clear sky
        elif 801 <= weather_id < 900:
            return "☁️"  # Clouds
        else:
            return "🌍"  # Default / Unknown

def main():
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()