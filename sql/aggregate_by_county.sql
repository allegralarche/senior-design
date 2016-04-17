INSERT INTO county_counterfactuals_2012 (SELECT county, COUNT(message_id), SUM(cf), SUM(cf)/COUNT(message_id) FROM county_tweet_cf_2012
GROUP BY county);