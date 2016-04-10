
select message from messages_en_2014_07_country
where  
        message like '%condition%' OR
        message like '%provided %' OR
        message like '%providing %' OR
        message like '%so long as %' OR
        message like '%unless %' OR
        message like '%whether %' OR
        message like '%suppose %' OR
        message like '%supposing %' OR
        message like '%imagine %' OR
        message like '%rather %' OR
        message like '%envision %' OR
        message like '%envisioning %' OR
        message like '%conceptualize %' OR
        message like '%conceptualizing %' OR
        message like '%conjure %' OR
        message like '%conjuring %' OR
        message like '%visualize %' OR
        message like '%visualizing %'
LIMIT 252;