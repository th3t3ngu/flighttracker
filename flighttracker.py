#!/usr/bin/env python3
import requests
import time
from datetime import datetime
import sys
import os
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


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
    print(f"[*] Searching for flight {flight} …")

    url = f"https://www.flightradar24.com/v1/search/web/find?query={flight}&limit=20"
    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        print("[!] Error at API-Request:", r.status_code)
        return None

    data = r.json()

    if "results" not in data:
        print("[!] No valid API-Response.")
        return None

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
        print("[!] Error at clickhandler-Request:", r.status_code)
        return None

    return r.json()


def extract_times(info):

    t = info.get("time", {})

<<<<<<< HEAD
=======
    # Departure
>>>>>>> 01e80d8f05a9aac63f9126356f97b1dae7e3e09b
    sched_dep = t.get("scheduled", {}).get("departure")
    real_dep = t.get("real", {}).get("departure")

    departure = real_dep or sched_dep

<<<<<<< HEAD
=======
    # Arrival
>>>>>>> 01e80d8f05a9aac63f9126356f97b1dae7e3e09b
    sched_arr = t.get("scheduled", {}).get("arrival")
    est_arr = t.get("estimated", {}).get("arrival")
    real_arr = t.get("real", {}).get("arrival")

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

    flight = input("Please enter flight number (z.B. DE1415): ").strip().upper()

    flight_id = get_flight_id(flight)
    if not flight_id:
        return

    print("\n[*] Catching Flight data…")
    info = get_flight_data(flight_id)

    if not info:
        print("[!] No Data received.")
        return

    ident = info.get("identification", {}).get("number", {}).get("default", flight)
    callsign = info.get("identification", {}).get("callsign")
    reg = info.get("aircraft", {}).get("registration")

    dep, arr = extract_times(info)

    flight_info_text = (
        "\nFlight info:\n"
        f"  Flight   : {ident}\n"
        f"  Callsign : {callsign}\n"
        f"  Reg      : {reg}\n"
        f"  Scheduled Departure: {conv(dep)}\n"
        f"  Scheduled Arrival  : {conv(arr)}\n"
)

    while True:
        clear_screen()

        print(flight_info_text)

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prog = calc_progress(dep, arr)

        print(f"=== Status-Update: {now} ===")
        status_line = info.get("status", {}).get("text", "Unknown")
        print("Status:", status_line)

        bar_len = 40
        filled = int(bar_len * prog)
        bar = "#" * filled + "-" * (bar_len - filled)

        print(f"Progress: [{bar}] {prog*100:5.2f}%\n")

        if prog >= 1.0:
            print("[*] Plane seems to have landed")
            break

        time.sleep(180)  # wait 3 minutes
        info = get_flight_data(flight_id)
        dep, arr = extract_times(info)



main()
