from flask import Flask, redirect, url_for, render_template, request
import folium
import pandas as pd
import csv
import networkx as nx
import osmnx as ox
from geopy.geocoders import Nominatim

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", content="Parcel tracking number")

@app.route('/map/')
def map():
    # Create a map centered at a specific location
    
    #-----------------Map-------------------------
    
    
    map = folium.Map(
        location=[48.77030162, 9.166415516],
        zoom_start=13
    )

    df = pd.read_csv(r'example.csv', header = None)

    df.columns = ['lat', 'lon', 'id', 'time']

    #THIS IS SWTICHED FOR SOME GOD DAMN REASON
    longitudes = df['lat'].tolist()
    latitudes = df['lon'].tolist()

    id = df['id'].tolist()
    time = df['time'].tolist()

    colors = ['red','red','red','red','blue','blue','blue','green','green','green','purple','purple','purple','pink','pink','pink']

    for i in range(len(longitudes)-1):
        '''
        print(str(i))
        G = ox.graph_from_point((eval(longitudes[i+1]), eval(latitudes[i+1])), network_type='drive')
        node = ox.distance.nearest_nodes(G, eval(longitudes[i+1]), eval(latitudes[i+1]))
        address = ox.geocode((G.nodes[node]['y'], G.nodes[node]['x']))
        '''
        geolocator = Nominatim(user_agent="GreenParcelDelivery")
        location = geolocator.reverse((eval(longitudes[i + 1]), eval(latitudes[i + 1])))

        folium.Marker(
            location=[eval(longitudes[i+1]), eval(latitudes[i+1])],
            popup=location.address + "\n Available starting at: " + str(time[i+1]),
            tooltip="Click Here for information on the address and availability of pickup station P" + str(i) + "!",
            icon=folium.Icon(color=colors[i+1])
        ).add_to(map)

    # Create a map centered at a specific location

    # Define the coordinates that you want to bound the map to
    bounds = [[48.8663994, 9.3160228], [48.6920188, 9.0386007]]

    # Use the fit_bounds() method to set the bounds of the map
    map.fit_bounds(bounds)

    #-----------------Buttons-------------------------

    if request.method == 'POST':
        selected_date = request.form.get('selected_date')
        selected_time = request.form.get('selected_time')
        # do something with the selected date and time
        return 'Selected date: {}<br>Selected time: {}'.format(selected_date, selected_time)
    # Render the template with the map data
    return render_template('map.html', map=map._repr_html_())

if __name__ == "__main__":
	app.run()
    #app.run(debug=True)