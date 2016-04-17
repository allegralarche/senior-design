use twitterGH;
select message from twt_1mil
where  
        message like '%could%' OR
        message like '%could\'ve' OR
        message like '%cudda%' OR
        message like '%culda%' OR
        message like '%cudve%' OR
        message like '%may%' OR
        message like '%might%' OR
        message like '%might\'ve%' OR
        message like '%must%' OR
        message like '%mustve%' OR
        message like '%must\'ve%' OR
        message like '%should%' OR
        message like '%should\'ve%' OR
        message like '%shuld\'ve%' OR
        message like '%shulda%' OR
        message like '%shuda%' OR
        message like '%shudda%' OR
        message like '%shudve%' OR
        message like '%would%' OR
        message like '%would\'ve%' OR
        message like '%wuda%' OR
        message like '%wulda%' OR
        message like '%wudda%' OR
        message like '%wudve%' OR
        message like '%wlda%' OR
        message like '%ought%' OR
        message like '%i\'d%' OR
        message like '%id%' OR
        message like '%i d%' OR
        message like '%we\'d%' OR
        message like '%wed%' OR
        message like '%we d%' OR
        message like '%youd%' OR
        message like '%you\'d%' OR
        message like '%you d%' OR
        message like '%they\'d%' OR
        message like '%wish%' OR
        message like '%rather%'
LIMIT 1000;