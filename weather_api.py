from time import strftime


class Weather:
    def __init__(self, response):
        self.json_response = response.json()
        self.data = self.json_response['data']
        self.place = self.data['request'][0]['query']
        self.time = strftime('%H:%M:%S')
        self.current_condition = self.data['current_condition'][0]
        self.temperature_Cels = self.current_condition['temp_C']
        self.weatherDesc = self.current_condition['weatherDesc']
        self.wind_speed = int(int(self.current_condition['windspeedKmph']) * 1000 / 3600)

    def get_wind_speed(self):
        return self.wind_speed

    def get_temp_in_celsius(self):
        return self.temperature_Cels

    def get_time(self):
        return self.time

    def get_place(self):
        return self.place

