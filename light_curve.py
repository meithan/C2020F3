from datetime import datetime
from math import log10
import sys

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

# ==============================================================================

# JPL Horizons data file (for distances to Sun and Earth)
data_fname = "horizons_C2020F3NEOWISE.txt"

# Light curve fit
# m0 + m1 log ∆ + m2 log r
# where
# Δ: comet-Earth distance, AU
# r: comet-Sun distance, AU
# Source: http://astro.vanbuitenen.nl/comet/2020F3
# Updated 15 jul
m0 = 7.05
k1 = 12.01
def get_magnitude(r, D):
  return m0 + 5*log10(D) + k1*log10(r)

# ==============================================================================

# Read Horizons data file
data = []
with open(data_fname) as f:
  for i in range(70):
    f.readline()
  for i in range(92):
    line = f.readline()
    date = datetime.strptime(line[1:12], "%Y-%b-%d")
    Tmag = float(line[72:78])
    Nmag = float(line[80:86])
    r = float(line[88:102])
    D = float(line[115:130])
    mag = get_magnitude(r, D)
    elong = float(line[145:153])
    pos = line[154]
    data.append((date, Tmag, Nmag, mag, r, D, elong, pos))

dates, Tmags, Nmags, mags, rs, Ds, elongs, pos = zip(*data)

now = datetime.utcnow()
now = datetime(now.year, now.month, now.day)
for i in range(len(dates)):
  if now <= dates[i]:
    break
now_date = dates[i]
now_mag = mags[i]
now_r = rs[i]
now_D = Ds[i]

# ---------------------------------------------
# LIGHT CURVE

plt.figure(figsize=(8,6))

plt.axvline(dates[i], color="0.5")
plt.annotate(dates[i].strftime("%d %b").lstrip("0"), xy=(now_date, 0.97), xycoords=("data", "axes fraction"), xytext=(5, 0), textcoords="offset pixels")

ln1, = plt.plot(dates, mags, color="k", label="Magnitude, $m$")
ax1 = plt.gca()

plt.scatter([now_date], [now_mag], color="k", zorder=10)
plt.annotate("$m=${:.1f}".format(now_mag), xy=(now_date, now_mag), xytext=(10, 0), textcoords="offset pixels")

plt.xlim(datetime(2020,6,20), datetime(2020,7,31))
plt.ylim(6, 0.8)

plt.ylabel("Magnitude")
plt.title("C/2020 F3 (NEOWISE) estimated light curve")
notes = ["$m = m_0 + 5 log_{10}(Δ) + k_1 log_{10}(r)$", "$m_0$ = {}, $k_1$ = {}".format(m0, k1), "Δ: Earth dist, AU", "r: Sun dist, AU"]
y0 = 0.99
dy = 0.04
bbox = dict(facecolor="white", edgecolor='none', pad=0, alpha=0.5)
for i,text in enumerate(notes):
  plt.text(0.01, y0-dy*i, text, transform=plt.gca().transAxes, va="top", bbox=bbox)

# ---------------------------------------------
# DISTANCES

ax2 = plt.gca().twinx()

color = "C1"
ln2, = ax2.plot(dates, rs, color=color, label="Sun distance, $r$")
plt.scatter([now_date], [now_r], zorder=10, color=color)
plt.annotate("$r=${:.2f} AU".format(now_r), xy=(now_date, now_r), xytext=(10, -10), textcoords="offset pixels", color=color)

color = "C2"
ln3, = ax2.plot(dates, Ds, color=color, label="Earth distance, Δ")
plt.scatter([now_date], [now_D], zorder=10, color=color)
plt.annotate("$Δ=${:.2f} AU".format(now_D), xy=(now_date, now_D), xytext=(10, 0), textcoords="offset pixels", color=color)

plt.ylabel("Distance [AU]")

plt.legend(handles=[ln1, ln2, ln3])

# ---------------------------------------------
# DECORATIONS

plt.sca(ax1)

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
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(5,35,5)))
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d"))
# plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=1))

plt.grid(ls="-", which="major")
plt.grid(ls=":", which="minor")
plt.gca().set_axisbelow(True)

# ---------------------------------------------

plt.tight_layout()

if "--save" in sys.argv:
  fname = "light_curve.png"
  plt.savefig(fname)
  print("Wrote", fname)
else:
  plt.show()
