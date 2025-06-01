import dateutil
import astropy.coordinates

from astropy.units import deg
from astropy.units import m


def get_site(site: str, obsdate: str, timezone: str):
    site_map = {
        "omu1p85m": astropy.coordinates.EarthLocation(
            lon=138.472153 * deg, lat=35.940874 * deg, height=1386 * m
        ),
        "nro45": astropy.coordinates.EarthLocation(
            lon=(138 + 28 / 60 + 21.2 / 3600) * deg,
            lat=(35 + 56 / 60 + 40.9 / 3600) * deg,
            height=1350 * m,
        ),
        "nanten2": astropy.coordinates.EarthLocation(
            lon=-67.70308139 * deg,
            lat=-22.96995611 * deg,
            height=4863.85 * m,
        ),
    }

    telescope = site_map.get(site.lower())
    if telescope is None:
        raise ValueError(f"Invalid site: {site}")

    obsdate_ = dateutil.parser.parse(
        "{obsdate} 00:00:00 TZ".format(**locals()),
        tzinfos={"TZ": dateutil.tz.gettz(timezone)},
    )

    return telescope, obsdate_
