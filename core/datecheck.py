from datetime import datetime

# Strings representing dates with timezone info
d1 = '2024-08-31 00:00:00+05:45'
d2 = '2022-09-04 00:00:00+05:45'

# Converting strings to datetime objects with timezone awareness
fmt = '%Y-%m-%d %H:%M:%S%z'  # Format string for parsing the date with timezone
dt1 = datetime.strptime(d1, fmt)
dt2 = datetime.strptime(d2, fmt)

# Subtracting the two datetime objects
difference = dt1 - dt2

# Getting the number of days difference
days_diff = difference.days

print(f"Difference in days: {days_diff}")
