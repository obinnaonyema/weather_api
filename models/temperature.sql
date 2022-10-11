select season, year, avg(tavg) tavg
from gsom.dbo.station_data
group by season, year
order by year
offset {} rows fetch next 100 rows only