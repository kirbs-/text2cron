# text2cron
Project aims to simplify tasks schedulesConvert a text phrase to a cron schedule expression.

## Examples
Verbose phrase
```python
>>> from text2cron import CronExp
>>> phrase = 'Tuesdays @1pm'
>>> cron_expression = CronExp(schedule_phrase = phrase)
>>> cron_expression
'Tues @1am CT cron expression "0 1 * * 2"'

>>> str(cron_expression)
'0 1 * * 2'

# Convert to UTC
>>> import pendulum
>>> pendulum.now().tzname()
'EST'
>>> str(cron_expression)
'0 1 * * 2'
>>> cron_expression.utc
'0 7 * * 2'
```

## Installation
`pip install text2cron`

## Enhancements
- convert between timezones.
- convert cron expression to word phrase.
