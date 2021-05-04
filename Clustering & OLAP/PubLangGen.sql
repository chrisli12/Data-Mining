with 
    BookCount (publisher, language, genre) as (
        select publisher, 
               language,
               genre,
        from Book
        group by cube(publisher, language, genre)
    )
select
    publisher,
    language,
    genre,
    decimal(total /SUM(total), 5, 4) as percentage
from BookCount
order by publisher, language, genre;