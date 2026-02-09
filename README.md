# Flighttracker

Is your SO a Flight attendant? Mine too!
This means that you too are familiar with the difficulties of keeping track of when a flight departs, lands, whether there are delays, or other issues.

Flighttracker tries to make it more easy. It is a simple tool in Python 3 that asks the user for a flight number, makes a web request to flightradar24, and displays the key information and a progress bar in the terminal:

	./flighttracker.py 
	Enter flight number (z.B. DE1415): DE1403
	[*] Searching for flight... DE1403 …
	[*] Found Flight ID: 3d40b962

	[*] Catching flight data...

	Flight info:
	  Flight   : DE1403
	  Callsign : CFG9KL
	  Reg      : D-AIAS
	  Scheduled Departure: 2025-11-25 14:39:51
	  Scheduled Arrival  : 2025-11-25 18:42:24

	=== Status-Update: 2025-11-25 15:50:31 ===
	Status: Estimated- 18:42
	Flight progress: [###########-----------------------------] 29.14%


By default, the tool retrieves the latest data from [flightradar24](https://www.flightradar24.com) every 180 seconds (3 minutes) and updates the output. Should work with every airline that flightradar24 lists, I mainly checked with flights by  [Condor](https://www.condor.com/de).

## Push notifications
You have the option to send a push notification when the tracked flight lands using the `--push` option. The script uses [simplepush.io](https://simplepush.io) for this.

To send the push notification, you first need to create the "landed" event in Simplepush and generate a key. Then you can call flighttracker.py with your key:
```python
./flighttracker.py --push --push-key KEY
```
The script will then send a push notification to your smartphone after the flight has landed.
(If you don't want to remmember your key every time, just set a bash/zsh-variable to the above command, so flighttracker gets called every time with your key.)