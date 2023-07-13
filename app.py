from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily, Hourly, Point
from geopy.geocoders import Nominatim
from flask import Flask, request, render_template
import io
import base64

# Set time period
start = datetime(1940, 1, 1)
end = datetime.now()

# Initialize geolocator with user_agent
geolocator = Nominatim(user_agent="http")

# Define a function to get the latitude and longitude of a city
def get_location(city):
    location = geolocator.geocode(city)
    return (location.latitude, location.longitude)

# Define a function to plot snow data for a given city and number of stations
def plot_snow(city_name, n):
    # Get the latitude and longitude of the city
    city_location = get_location(city_name)
    
    # Get weather stations near the city location
    stations = Stations().nearby(lon=city_location[1], lat=city_location[0]).inventory("hourly")
    
    # Create a subplots figure with a specified size
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Loop through the specified number of stations
    for i in range(n):
        # Get the i-th station
        station = stations.fetch(n).to_dict("records")[i]
        
        # Create Point object with station latitude, longitude, and elevation
        location = Point(station['latitude'], station['longitude'], station['elevation'])
        
        # Get daily snow data for the location and time period
        data = Daily(location, start, end).fetch()
        
        # Plot line chart of snow data, including station name and varying line widths
        #ax.plot(data.snow,'.',markerfacecolor="none",label=station['name'],alpha=.7,lw =(-(i/4)+4))
        ax.plot(data['snow'].resample('Y').mean(),'-o',markerfacecolor="none",label=station['name'],alpha=.7,lw =(-(i/4)+4))
    # Add legend and label y-axis
    ax.legend(loc='center left', bbox_to_anchor=(0, 0.88))
    ax.set_ylabel('Yearky mean of snow depth mm')
    
    # Save the plot to a BytesIO object and encode it to base64 for display on the web page
#    buffer = io.BytesIO()
    plt.savefig('test.png', format='png')
#    plot_data = base64.b64encode(buffer.getvalue()).decode()
    
    # Clear the plot and close the figure to free up memory
#    plt.clf()
#    plt.close()
    
#    return plot_data

# Create a Flask web app
app = Flask(__name__)

# Define the home page route and function
@app.route('/')
def index():
    return '''
        <form method="post" action="/result">
            <label>Enter city name:</label>
            <input type="text" name="name" />
            <label> Enter n :</label>
            <input type="number" name="n" />
            <button type="submit">Submit</button>
        </form>
    '''
@app.route('/result', methods=['POST'])
def result():
    name = request.form['name']
    n     =request.form['n']
    print(name, n)
    plot_snow(name, int(n))
    

# Run the web app
if __name__ == '__main__':
    #app.run(debug=True)
    if __name__ == '__main__':
        app.run(debug=True, port=8000)
