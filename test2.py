# import datetime module
import datetime

# consider the start date as 2021-february 1 st
start_date = datetime.date(2021, 2, 1)

# consider the end date as 2021-march 1 st
end_date = datetime.date(2021, 3, 1)

# delta time
delta = datetime.timedelta(days=1)

# iterate over range of dates
while (start_date <= end_date):
	print(start_date, end="\n")
	start_date += delta
