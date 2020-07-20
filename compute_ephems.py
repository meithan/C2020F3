from datetime import datetime, timedelta
from math import degrees
import os
import sys
import urllib.request

import base

import ephem

# ==============================================================================
# PROGRAM CONFIGURATION

# Dates are *local* time
start_date = datetime(2020, 7, 20, 20, 15)
end_date = datetime(2020, 7, 20, 21, 30)
interval = timedelta(minutes=5)

# Observer location
location = base.locations["Mexico City"]
# location = base.locations["Guadalajara"]
# location = base.locations["Grenoble"]
# location = base.locations["Tallinn"]

# Filename with elements in XEphem format
elems_fname = "comets.txt"

# ==============================================================================

# ------------------------------------------------------------------------------
# DOWNLOAD OR LOAD COMET ELEMENTS

if "--download" or "--update" in sys.argv:
  force_download = True
else:
  force_download = False
comets = base.load_elements(elems_fname, force_download=force_download)
elements = comets["C/2020 F3 (NEOWISE)"]

# ------------------------------------------------------------------------------
# COMPUTE EPHEMERIS

obs = ephem.Observer()
obs.lon = str(location.longitude)
obs.lat = str(location.latitude)
obs.elevation = location.elevation
comet = ephem.readdb(elements)
utc_delta = timedelta(hours=location.utc_offset)

print("\nEphemeris for {}".format(comet.name))
print("Location: {} ({}, {})".format(location.name, base.nice_lat(location.latitude), base.nice_lon(location.longitude)))
print("Start: {} UTC{:+}".format(start_date, location.utc_offset))
print("End: {} UTC{:+}".format(end_date, location.utc_offset))

print("\n{:<21s} {:<13s} {:<13s} {:<13s} {:<13s}".format("Local date/time", "Comet Alt", "Comet Az", "Sun Alt", "Sun Az"))
local_date = start_date
while local_date <= end_date:
  utc_date = local_date-utc_delta
  obs.date = utc_date
  comet.compute(obs)
  sun = ephem.Sun(obs)
  alt_dif = degrees(float(comet.alt) - float(sun.alt))
  print("{:<21s} {:<13s} {:<13s} {:<13s} {:<13s}".format(str(local_date), base.nice_angle(comet.alt), base.nice_angle(comet.az), base.nice_angle(sun.alt), base.nice_angle(sun.az)))
  local_date += interval
