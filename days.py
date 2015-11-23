import sys
import datetime as dt
import argparse
import pandas as pd


class RainyDays(object):
    '''
    Docstring goes here.
    '''
    def __init__(self, station, sDate, eDate,
                 verbose=False):
        self.station = station
        firstDOW = sDate.isoweekday()
        lastDOW = eDate.isoweekday()
        if (lastDOW % 7) + 1 != firstDOW:
            while True:
                err = ('Analysis begins on a {:%A}, and ends on a {:%A}. This'
                       ' may cause an inaccurate count based on the number of'
                       ' weeks for each day. Do you want to modify your start'
                       ' or end dates?'.format(sDate, eDate))
                print(err)
                response = raw_input('[Y/n] ')
                if response.startswith(('Y', 'y')) or response == '':
                    sys.exit('Modify start and/or end date.')
                elif response.startswith(('N', 'n')):
                    break
                else:
                    print('I didn\'t recognize that response.')
        self.startDate = sDate
        self.endDate = eDate
        self.verbose = verbose
        self.baseURL = ('https://mesonet.agron.iastate.edu/cgi-bin/request/'
                        'asos.py?')
        self.URL = None
        self.days = [
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday']
        self.rainDays = None

    def computeRain(self):
        self._createURL()
        self._computeData()

    def printStats(self):
        for d in self.days:
            print('{:<9s}: {:>5d}'.format(d, self.rainDays.count(d)))

    def _createURL(self):
        url_segments = [
            'station={:}'.format(self.station[1:]),
            'data=p01i',                           # 1-hr precip in inches
            'year1={:}'.format(self.startDate.year),
            'month1={:}'.format(self.startDate.month),
            'day1={:}'.format(self.startDate.day),
            'year2={:}'.format(self.endDate.year),
            'month2={:}'.format(self.endDate.month),
            'day2={:}'.format(self.endDate.day),
            'tz=Etc%2FUTC',
            'format=tdf',
            'latlon=no',
            'direct=no']
        url_end = '&'.join(url_segments)
        self.URL = '&'.join([self.baseURL, url_end])
        if self.verbose:
            print('Remote URL is {:}'.format(self.URL))

    def _computeData(self):
        data = pd.read_csv(self.URL,
                           sep='\t',
                           header=5,
                           parse_dates=[1])
        rainObs = data[data[' p01i '] > 0.00]
        rainDates = [i.date() for i in rainObs['valid']]
        uniqueDates = set(rainDates)
        if self.verbose:
            print('Out of {:} total observations, {:} contained rain.'.format(
                len(data), len(rainObs)))
            print('Out of those {:} raining observations, {:} occurred on '
                  'unique days.'.format(len(rainDates), len(uniqueDates)))
        self.rainDays = [i.strftime('%A') for i in uniqueDates]

    def __repr__(self):
        print('Rainy days for {:}'.format(self.station))


def parse_args(opts):
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
    parser.add_argument('-s', '--start-date',
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
    return parser.parse_args(opts)


def _parse_date(dateStr):
    fullTime = dt.datetime.strptime(dateStr, '%Y-%m-%d')
    return fullTime.date()


def main(station, sDate, eDate, verbose=False):
    dayStats = RainyDays(station, sDate, eDate, verbose=verbose)
    dayStats.computeRain()
    dayStats.printStats()

if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    startDate = _parse_date(args.start_date)
    endDate = _parse_date(args.end_date)
    main(
        args.station,
        startDate,
        endDate,
        args.verbose)
