from datetime import datetime, timedelta
from math import degrees
import os
import sys
import urllib.request

import base

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import ephem

# ==============================================================================
# PROGRAM CONFIGURATION

# Dates are *local* time
start_date = datetime(2020, 7, 11, 5, 30)
end_date = datetime(2020, 7, 11, 7, 10)

# Observer location
location = base.locations["Mexico City"]
# location = base.locations["Guadalajara"]
# location = base.locations["Grenoble"]

# Filename with elements in XEphem format
elems_fname = "comets.txt"

# ==============================================================================

# ------------------------------------------------------------------------------
# LOAD COMET ELEMENTS

comets = base.load_elements(elems_fname)
elements = comets["C/2020 F3 (NEOWISE)"]

# ------------------------------------------------------------------------------
# COMPUTE EPHEMERIS

obs = ephem.Observer()
obs.lon = str(location.longitude)
obs.lat = str(location.latitude)
obs.elevation = location.elevation
utc_delta = timedelta(hours=location.utc_offset)
# obs.pressure = 0

comet = ephem.readdb(elements)

print("\nLocation: {} ({}, {})".format(location.name, base.nice_lat(location.latitude), base.nice_lon(location.longitude)))

dates = []
sunrise_alts = []
sunset_alts = []
date = datetime(2020, 7, 1, 12)
while date <= datetime(2020, 7, 31, 12):

  dates.append(date.date())
  obs.date = date-utc_delta

  utc_sunrise = obs.previous_rising(ephem.Sun()).datetime()
  utc_sunset = obs.next_setting(ephem.Sun()).datetime()

  # Sunrise
  obs.date = utc_sunrise
  comet.compute(obs)
  sun = ephem.Sun(obs)
  sunrise_alt = comet.alt
  sunrise_alts.append(degrees(float(sunrise_alt)))

  # Sunrise
  obs.date = utc_sunset
  comet.compute(obs)
  sun = ephem.Sun(obs)
  sunset_alt = comet.alt
  sunset_alts.append(degrees(float(sunset_alt)))

  print()
  print("Sunrise: {}, {}".format((utc_sunrise+utc_delta).strftime("%Y-%m-%d %H:%M:%S UTC{}".format(location.utc_offset)), base.nice_angle(sunrise_alt)))
  print("Sunset: {}, {}".format((utc_sunset+utc_delta).strftime("%Y-%m-%d %H:%M:%S UTC{}".format(location.utc_offset)), base.nice_angle(sunset_alt)))

  date += timedelta(days=1)

plt.plot(dates, sunrise_alts, "o-", ms=4, label="At sunrise")
plt.plot(dates, sunset_alts, "o-", ms=4, label="At sunset")

plt.axhline(0, color="gray")

plt.title("C/2020 F3 (NEOWISE) altitude over horizon at sunrise & sunset\n{} ({}, {})".format(location.name, base.nice_lat(location.latitude), base.nice_lon(location.longitude)))
plt.ylabel("Altitude [degrees]")

def fmt(x, pos):
  date = mdates.num2date(x)
  if date.day % 5 == 0:
    return str(date.day)
  else:
    return ""
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
plt.gca().xaxis.set_minor_formatter(ticker.FuncFormatter(fmt))

plt.legend()
plt.grid(ls="-", which="major")
plt.grid(ls=":", which="minor")
plt.gca().set_axisbelow(True)

plt.xlim(dates[0]-timedelta(hours=12), dates[-1]+timedelta(hours=12))

plt.tight_layout()

if "--save" in sys.argv:
  fname = "rise_set_alts_{}.png".format(location.name.replace(" ", "_"))
  plt.savefig(fname)
  print("Wrote", fname)
else:
  plt.show()
