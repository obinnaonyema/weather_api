select station,season, year, count(tavg) data_points
from gsom.dbo.station_data
group by station,season, year
order by station,year
offset {} rows fetch next 100 rows only