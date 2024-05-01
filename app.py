from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

date_now = 0


@app.route('/')
def home():
    api_key = "290808586775338600ff6149740938ac"
    city = "Adelaide"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={api_key}"
    data = requests.get(url).json()
    temp_data_all = {}
    print(url)

    # Check if the request was successful
    if data["cod"] == "200":
        # Extract the list of forecasts
        forecasts = data["list"]
        # Initialize a dictionary to store timestamps for each day
        timestamps_per_day = {}
        # Get the current date
        current_date = datetime.utcfromtimestamp(forecasts[0]["dt"])

        # Loop through each forecast
        for forecast in forecasts:
            temp_data = {}
            # Extract the timestamp
            timestamp = forecast["dt"]
            # Convert timestamp to date
            date = datetime.utcfromtimestamp(timestamp)
            temp_data["datetime"] = timestamp
            temp_data["temp_min"] = round(forecast["main"]["temp"] - 273.15)
            temp_data_all[date.strftime("%A")] = temp_data
            print(temp_data_all)

            # If it's a new day, store the timestamp
            if date.date() != current_date.date():
                timestamps_per_day[current_date.date()] = current_date.timestamp()
                current_date = date

        # Add the last day's timestamp
        timestamps_per_day[current_date.date()] = current_date.timestamp()

        # Print the timestamps for each day
        for day, timestamp in timestamps_per_day.items():
            print(f"Day: {day}, Timestamp: {timestamp}")

    else:
        print("Failed to retrieve data from the API.")

    def extract_temperatures(forecast_list):
        daily_temperatures = {}
        for forecast in forecast_list:
            dt_txt = forecast['dt_txt']
            date_key = dt_txt.split()[0]  # Extract date from datetime
            temp_celsius = forecast['main']['temp_min'] - 273.15  # Convert to Celsius
            if date_key not in daily_temperatures:
                daily_temperatures[date_key] = {'min_temp': temp_celsius, 'max_temp': temp_celsius}
            else:
                daily_temperatures[date_key]['min_temp'] = min(daily_temperatures[date_key]['min_temp'], temp_celsius)
                daily_temperatures[date_key]['max_temp'] = max(daily_temperatures[date_key]['max_temp'], temp_celsius)
        return daily_temperatures

    def get_current_date():
        now = datetime.now()
        return now.strftime("%Y-%m-%d")


# forecast_ilist = response["list"]
# icon_dict = []
# index = 0
# while index < len(forecast_ilist):
#     icon = (forecast_ilist[index]["weather"][0]["icon"])
#
#     icon_dict = {
#         "icon": icon
#     }
#     index +=8
#     print(icon)

def extract_icon(forecast_list):
    icon_bydate = {}
    for forecast in forecast_list:
        timestamp = forecast["dt"]
        date = datetime.utcfromtimestamp(timestamp)
        dt_txt = forecast['dt_txt']
        date_key = dt_txt.split()[0]
        temp_icon = forecast['weather']['icon'](".png")
        return icon_bydate

    # for date_now in range(0, 6):
    #     day_temp = [forecast['main']['temp'] for forecast in data.get("list", []) if
    #                 forecast['dt_txt'].startswith(str(date_now))]
    #     min_temp = min(day_temp) - 273.15  # Convert to Celsius
    #     max_temp = max(day_temp) - 273.15  # Convert to Celsius
    #     date_key = (data.get("list", [])[date_now]['dt_txt']).split()[0]  # Extract date from datetime
    daily_temperatures = {'min_temp': 15, 'max_temp': 20}

    return render_template('home.html', data=temp_data_all)


# omg code cooking :D


if __name__ == "__main__":
    app.run(debug=True)

# index = 0
# while index <len(forecast_list):
# print(forecast_list[index]["dt_txt"])
# print(forecast_list[index]["main"]["temp"])
# print(forecast_list[index]["weather"]["icon"])
# index += 8
