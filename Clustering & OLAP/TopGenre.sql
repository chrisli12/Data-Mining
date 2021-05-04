--TopGenre
--For the top genre by sales for each country, province, city, show the top three customers by sales in that genre.
with
    Sale_per_customer ( country, province, city, genre, cust#, sales) as (
        select C.country,
               C.province,
               C.city,
               B.genre,
               P.cust#,
               sum(P.sale) as sales
        from Purchase P 
        left join Customer C on C.cust# = P.cust# 
        left join Book B on P.book# = B.book#
        group by C.country, C.province, C.city, B.genre, P.cust#
    ),

    Sales_per_genre(country, gc, province, gp, city,  gcc, genre, sales) as (
        select C.country,
               grouping(C.country),
               C.province,
               grouping(C.province),
               C.city,
               grouping(C.city),
               B.genre,
               sum(sale) as sales
        from Customer C, Purchase P, Book B
        where C.cust# = P.cust# and P.book# = B.book# 
        group by cube(C.country, C.province, C.city), genre
    ),
    --Genre ranking in each country, provice, city
    Rank_genre(country, province, city, genre, rank#, sales) as (
        select country, 
               province, 
               city, 
               genre, 
               rank() over (partition by country, province, city order by sales desc),
               sales
        from Sales_per_genre
        where gc = 0 and gp = 0 and gcc = 0
    ),
    --return the top 1 genre in each country, provinc, city
    Top_genre (country, province, city, genre, sales) as (
        select country, 
                province,
                city, 
                genre, 
                sales
        from Rank_genre
        where rank# = 1
    ),

    Top_cust (country, province, city, genre, cust#, rank#, sales) as (
    select S.country, 
           S.province, 
           S.city, 
           S.genre, 
           S.cust#, 
           rank() over (partition by S.country, S.province, S.city order by S.sales desc),
           S.sales
    from Top_genre t left join Sale_per_customer S
    on t.country = S.country and t.province = S.province and t.city = S.city and t.genre = S.genre
    )

    select country, province, city, genre, int(cust#) as cust#, smallint(rank#) as rank#, decimal(sales, 12, 2) as sales
    from Top_cust
    where rank# <= 3
    order by country, province, city, genre, rank#, cust#;