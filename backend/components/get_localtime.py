import dateutil
import numpy
import astropy.time


def get_localtime(obsdate_: str, telescope: str):
    localtime = numpy.array(
        list(
            dateutil.rrule.rrule(
                freq=dateutil.rrule.MINUTELY,
                interval=10,
                dtstart=obsdate_,
                until=obsdate_ + dateutil.relativedelta.relativedelta(days=+1),
            )
        )
    )

    localtime_ap = astropy.time.Time(localtime, format="datetime", location=telescope)
    lst = localtime_ap.sidereal_time("apparent")

    return localtime, localtime_ap, lst
