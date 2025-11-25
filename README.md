# Flighttracker

Is your SO a Flight attendant? Mine too!
This means that you too are familiar with the difficulties of keeping track of when a flight departs, lands, whether there are delays, or other issues.

Flighttracker tries to make it more easy. It is a simple tool in Python 3 that asks the user for a flight number, makes an API request to flightradar.com, and displays the following information in the terminal:

- Departure
- Scheduled arrival
- Possible delay
- Progress indicator

By default, the tool retrieves the latest data from (www.flightradar24.com)[flightradar24.com] every 180 seconds (3 minutes) and updates the output. Should work with every airline that flightradar24.com lists, I mainly checked with flights by (https://www.condor.com/de)[Condor].