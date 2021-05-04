--LocPercent
--Roll-up of country > province > city reporting the  percentage of sales for each group with respect to all sales 
--and reporting the percentage of sales for each group with respect to sales in the immediate super-group 
--(for example, sales for CND-ON-Toronto over CND-ON-ALL).

with 
    Roll (country, province, city, level, sales) as (
        select c.country,
               c.province,
               c.city,
               grouping(country) + grouping(province) + grouping(city) as level,
               sum(p.sale) as sales
        from Customer c, Purchase p
        where c.cust# = p.cust#
        group by rollup(country, province, city)
    ),

    Total (country, province, city, sales) as (
        select country, province, city, sales
        from Roll
        where level = 3
    )

select c.country, 
       c.province, 
       c.city,
       DECIMAL(FLOAT(c.sales) / t.sales, 5, 4) as percent_of_all,
       DECIMAL(FLOAT(c.sales) / p.sales, 5, 4) as percent_in_group
from Roll c, Roll p, Total t
where (p.level = 3 or p.country = c.country) and (p.level = 2 or p.province = c.province) and p.level = c.level + 1
union all
select c.country, 
       c.province, 
       c.city,
       DECIMAL(FLOAT(c.sales) / t.sales, 5, 4) as percent_of_all,
       DECIMAL(FLOAT(c.sales) / p.sales, 5, 4) as percent_in_group
from Roll c, Roll p, Total t
where c.level = 2 and p.level = 3 
union all
select country, province, city, 1.0, 1.0
from Total
order by country, province, city;    