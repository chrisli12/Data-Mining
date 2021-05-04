-- Smoothing
-- Report sales by day, smoothing over 31 days
-- (30 days preceding through the current day).

with
    Daily_Sales (year, month, day, sales) as (
        select year(when)  as year,
               month(when) as month,
               day(when)   as day,
               sum(sale)   as sales
        from Purchase P
        group by year(when), month(when), day(when)
    )
select year, month, day,
       avg(sales) over (order by year, month, day
                        rows
                        between 30 preceding
                        and current row)
           as smoothed_sales
from Daily_Sales D
order by year, month, day;

