#!/usr/bin/python
# https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?
#    station=SGR&
#    data=presentwx&
#    year1=2015&
#    month1=1&
#    day1=1&
#    year2=2015&
#    month2=11&
#    day2=20&
#    tz=Etc%2FUTC&
#    format=tdf&
#    latlon=no&
#    direct=no

import sys
import datetime as dt
import argparse


def parse_args(args):
    defaults = {
        'station':    'KIAH',
        'start-date': '2015-01-01',
        'end-date':   dt.date.today().isoformat()}
    parser = argparse.ArgumentParser(
        prog='Rainy Days',
        description=('Scans historical ASOS observations to count the number '
                     'of raining days of the week.'))
    parser.add_argument('station',
                        default=defaults['station'],
                        help=('ICAO station identifier. Defaults to '
                              '{:}'.format(defaults['station'])))
    parser.add_argument('-s', '--start-time',
                        default=defaults['start-date'],
                        help=('First date to analyze in YYYY-MM-DD '
                              'format. Defaults to {:}.'.format(
                                  defaults['start-date'])))
    parser.add_argument('-e', '--end-date',
                        default=dt.date.today().isoformat(),
                        help=('Last date to analyze in YYYY-MM-DD format. '
                              'Defaults to {:}.'.format(
                                  defaults['end-date'])))
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        default=False,
                        help='Prints verbose information.')
    # add plot option here; for now, we'll just print it out to the screen
    return parser.parse_args(args)


def end_time():
    pass


if __name__ == '__main__':
    print('Running main')
    parse_args(sys.argv)
