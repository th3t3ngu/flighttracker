#!/usr/bin/env python3
import requests
import time
from datetime import datetime
import sys

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.flightradar24.com/",
    "Origin": "https://www.flightradar24.com"
}

def conv(ts):
    if not ts:
        return None
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def get_flight_id(flight):
    print(f"[*] Searching for flight... {flight} …")

    url = f"https://www.flightradar24.com/v1/search/web/find?query={flight}&limit=20"
    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        print("[!] Error on API-request:", r.status_code)
        return None

    data = r.json()

    if "results" not in data:
        print("[!] No valid API-answer.")
        return None

    # wir suchen "type": "live" → enthält die flight_id
    for item in data["results"]:
        if item["type"] == "live" and "detail" in item:
            flight_id = item["id"]
            print(f"[*] Found Flight ID: {flight_id}")
            return flight_id

    print("[!] Flight not found!")
    return None

def get_flight_data(flight_id):
    url = f"https://data-live.flightradar24.com/clickhandler/?flight={flight_id}"
    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        print("[!] Error on clickhandler-Request:", r.status_code)
        return None

    return r.json()

def extract_times(info):

    t = info.get("time", {})

    # Abflug
    sched_dep = t.get("scheduled", {}).get("departure")
    real_dep = t.get("real", {}).get("departure")

    departure = real_dep or sched_dep

    # Ankunft
    sched_arr = t.get("scheduled", {}).get("arrival")
    est_arr = t.get("estimated", {}).get("arrival")
    real_arr = t.get("real", {}).get("arrival")

    # If already landed
    status = info.get("status", {})
    landed_utc = status.get("generic", {}).get("eventTime", {}).get("utc")

    arrival = est_arr or real_arr or sched_arr or landed_utc

    return departure, arrival

def calc_progress(dep, arr):
    now = time.time()
    if dep is None or arr is None:
        return 0.0

    dur = arr - dep
    if dur <= 0:
        return 0.0

    prog = (now - dep) / dur
    return max(0.0, min(1.0, prog))

def main():

    flight = input("Enter flight number (z.B. DE1415): ").strip().upper()

    flight_id = get_flight_id(flight)
    if not flight_id:
        return

    print("\n[*] Catching flight data...")
    info = get_flight_data(flight_id)

    if not info:
        print("[!] No data received.")
        return

    ident = info.get("identification", {}).get("number", {}).get("default", flight)
    callsign = info.get("identification", {}).get("callsign")
    reg = info.get("aircraft", {}).get("registration")

    dep, arr = extract_times(info)

    print("\nFlight info:")
    print(f"  Flight   : {ident}")
    print(f"  Callsign : {callsign}")
    print(f"  Reg      : {reg}")
    print(f"  Scheduled Departure: {conv(dep)}")
    print(f"  Scheduled Arrival  : {conv(arr)}\n")

    while True:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prog = calc_progress(dep, arr)

        print(f"=== Status-Update: {now} ===")
        status_line = info.get("status", {}).get("text", "Unknown")
        print("Status:", status_line)

        bar_len = 40
        filled = int(bar_len * prog)
        bar = "#" * filled + "-" * (bar_len - filled)

        print(f"Flight progress: [{bar}] {prog*100:5.2f}%\n")

        if prog >= 1.0:
            print("[*] Plane seems to have landed")
            break

        time.sleep(180)  # wait 3 minutes, then refresh
        info = get_flight_data(flight_id)
        dep, arr = extract_times(info)

main()
