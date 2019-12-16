import pendulum
import re


class CronExp():
    
    def __init__(self, **kwargs):
        self.minute = kwargs.get('minute', '*')
        self.hour = kwargs.get('hour', '*')
        self.day_of_month = kwargs.get('day_of_month', '*')
        self.month = kwargs.get('month', '*')
        self.day_of_week = kwargs.get('day_of_week', '*')
        self.schedule_phrase = kwargs.get('schedule_phrase')
        self.tz = kwargs.get('timezone', pendulum.now().utcoffset().total_seconds()/3600)
        
        if self.schedule_phrase:
            self.parse(self.schedule_phrase)
        
    def parse(self, schedule_phrase):
        self.schedule_phrase = schedule_phrase
        tokens = schedule_phrase.split()
        tokens = dict(zip(list(map(self._token_type, tokens)), tokens ))
        
        for token_type, token in tokens.items():
#             print(token_type, ':', token)
            self.__dict__[token_type.lower()] = CronExp.ACTION[token_type](self, token)
        
        self._time_to_hours_minutes()
            
    def _day_to_int(self, day_of_week):
        return CronExp.DAYS_OF_WEEK[day_of_week.lower()[:3]]
    
    @property
    def utc(self):
        return '{} {} {} {} {}'.format(self.minute, self.hour - self._utcoffset, self.day_of_month, self.month, self.day_of_week)
        
    def _token_type(self, token):
        if len(token) == 2:
            return 'TZ'
        elif '@' in token:
            return 'TIME'
        elif token[0:3].lower() in CronExp.DAYS_OF_WEEK:
            return 'DAY_OF_WEEK'
        else:
            return 'DAY_OF_MONTH'
    
    @property
    def _utcoffset(self):
        return int(pendulum.now(tz=self.tz).utcoffset().total_seconds()/3600)
        
    def _time_to_hours_minutes(self):
        if self.time:
            self.hour = self.time[0]
            self.minute = self.time[1]
            
    def _tz(self, timezone):
        if timezone in CronExp.TZ:
            timezone = CronExp.TZ[timezone]
        return timezone
    
    def __str__(self):
        return '{} {} {} {} {}'.format(self.minute, self.hour, self.day_of_month, self.month, self.day_of_week)
    
    def __repr__(self):
        return '{} cron expression \'{}\''.format(self.schedule_phrase, str(self))
        
    def _convert24(self, time):
        try:
            hours, minutes = list(map(int, re.search('(\d+):(\d+)', time).groups()))
        except:
            hours = int(re.search('(\d+)', time).groups()[0])
            minutes = 0

        if time[-2:] == 'pm' and hours != 12:
            hours += 12

        return hours, minutes
    
    ACTION = {'DAY_OF_WEEK': _day_to_int,
              'TIME': _convert24,
              'TZ': _tz}
    
    DAYS_OF_WEEK = {
        'sun': '0',
        'mon': '1',
        'tue': '2',
        'wed': '3',
        'thu': '4',
        'fri': '5',
        'sat': '6',
        'daily': '*',
        'weekdays': '1-5'
    }
    
    HOURS = {
        'noon': '12',
        'midnight': '0'
    }
    
    TZ = {'ET': 'America/New_York',
          'CT': 'America/Chicago'}