select station,season, year, count(tavg) data_points, avg(tavg) tavg
            from gsom.dbo.station_data
            where LATITUDE between {} and {}
            and LONGITUDE between {} and {}
            and year between {} and {}
            group by station,season, year
            order by station, year
            offset {} rows fetch next 100 rows only