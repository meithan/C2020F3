import os
import urllib.request

# ==============================================================================

class Location:
  def __init__(self, name, latitude, longitude, elevation, utc_offset):
    self.name = name
    self.latitude = latitude
    self.longitude = longitude
    self.elevation = elevation
    self.utc_offset = utc_offset

locations_list = [
  Location("Mexico City", 19.279889, -99.178444, 2320, -5),
  Location("Guadalajara", 20.676216, -103.346928, 1500, -5),
  Location("Tonalá", 20.624140, -103.242150, 1540, -5),
  Location("Grenoble", 45.174480, 5.721035, 215, +2),
]

locations = {x.name: x for x in locations_list}

# ==============================================================================

def nice_lat(latitude):
  """Formats a decimal latitude (positive towards North) as a nice string"""
  degs, mins, secs = degs2dms(latitude)
  return "{:.0f}°{:.0f}'{:.1f}\"{}".format(abs(degs), mins, secs, "N" if latitude >= 0 else "S")

def nice_lon(longitude):
  """Formats a decimal longitude (positive towards East) as a nice string"""
  degs, mins, secs = degs2dms(longitude)
  return "{:.0f}°{:.0f}'{:.1f}\"{}".format(abs(degs), mins, secs, "E" if longitude >= 0 else "W")

def degs2dms(angle):
  """Converts a decimal angle, in degrees, to degrees, minutes, seconds"""
  a = abs(angle)
  mins, secs = divmod(a*3600, 60)
  degs, mins = divmod(mins, 60)
  if angle < 0: degs *= 1
  return (int(degs), int(mins), secs)

def nice_angle(angle):
  """Convert a pyephem Angle to a nice string"""
  return "{}°{}'{}\"".format(*(str(angle).split(":")))

# ==============================================================================

def load_elements(elems_fpath, force_download=False, verbose=True, url=None):
  """Loads comet elements from a file containing elements in XEphem format
  Returns a dict using the full comet names as keys and the XEphem elements
  as value.
  Default url is list maintained by Minor Planet Center"""

  if url is None:
    url = "https://minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt"
    # url = "http://astro.vanbuitenen.nl/cometelements?format=xephem"

  if force_download:
    download = True
  else:
    if not os.path.exists(elems_fpath):
      if verbose:
        print("{} not found, downloading elements ...".format(elems_fpath))
      download = True
    else:
      download = False

  if download:

    with urllib.request.urlopen(url) as doc:
      text = doc.read().decode("utf-8")
    with open(elems_fpath, "w") as fout:
      fout.write(text)
    if verbose:
      print("Downloaded new elements and saved them to {}".format(elems_fpath))

  else:

    with open(elems_fpath) as f:
      text = f.read()
    if verbose:
      print("Loaded elements from {}".format(elems_fpath))

  elements = {}
  for line in text.split("\n"):
    if line.startswith("#"):
      continue
    tokens = line.split(",")
    if tokens[0] != "":
      elements[tokens[0]] = line

  return elements

# ==============================================================================
