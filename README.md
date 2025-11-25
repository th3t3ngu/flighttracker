# Flighttracker

Is your SO a Flight attendant? Mine too!
This means that you too are familiar with the difficulties of keeping track of when a flight departs, lands, whether there are delays, or other issues.

Flighttracker tries to make it more easy. It is a simple tool in Python 3 that asks the user for a flight number, makes an API request to flightradar24, and displays the key information and a progress bar in the terminal:

	./flighttracker.py
	Enter flight number (z.B. DE1415): FR2201
	[*] Searching for flight... FR2201 …
	[*] Found Flight ID: 3d407b50

	[*] Catching flight data...

	Flight info:
	  Flight   : FR2201
	  Callsign : RYR4KZ
	  Reg      : 9H-QBN
	  Scheduled Departure: 2025-11-25 13:06:51
	  Scheduled Arrival  : 2025-11-25 16:53:36

	=== Status-Update: 2025-11-25 15:27:44 ===
	Status: Estimated- 15:53
	Progress: [########################----------------] 62.13%


By default, the tool retrieves the latest data from [flightradar24](www.flightradar24.com) every 180 seconds (3 minutes) and updates the output. Should work with every airline that flightradar24 lists, I mainly checked with flights by  [Condor](https://www.condor.com/de).