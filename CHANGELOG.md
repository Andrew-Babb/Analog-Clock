# Changelog

## v1.1

- Replaced the fixed UTC offset with Python's `zoneinfo.ZoneInfo`.
- Set the clock timezone to `America/New_York`.
- Removed the manual `timedelta(hours=-4)` adjustment so daylight saving time
  is handled automatically.

## v1.0

- Initial terminal analog clock implementation.
- Added a bordered clock face with hour markers.
- Added hour, minute, and second hands.
- Added a centered digital time readout.
- Added keyboard exit support with `q` and `Q`.
