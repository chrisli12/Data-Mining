with
    Sales (genre, gg, language, gl, country, province, city, sales) as (
        select B.genre,
               grouping(B.genre),
               B.language,
               grouping(B.language),
               C.country,
               C.province,
               C.city,
               sum(sale) as sales
        from Customer C, Purchase P, Book B
        where C.cust# = P.cust#
          and P.book# = B.book#
        group by cube(B.genre, B.language), C.country, C.province, C.city
    ),

    Ranking (genre, language, rank#, country, province, city, sales) as (
        select genre, language,
               rank() over(partition by genre
                           order by sales desc),
               country, province, city, sales
        from Sales
        where gg = 0 AND gl = 1
        union all
        select genre, language,
               rank() over(partition by language
                           order by sales desc),
               country, province, city, sales
        from Sales
        where gg = 1 AND gl = 0
    )

select genre,
       language,
       smallint(rank#) as rank#,
       country,
       province,
       city,
       decimal(sales, 12, 2) as sales
from Ranking
where rank# <= 2
order by genre, language, rank#;
