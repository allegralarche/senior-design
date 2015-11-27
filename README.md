--------------------------------
Make sure you do this:
mysql -u root
GRANT SELECT ON randomTwitter_by_month.* TO 'username'@'localhost';
GRANT SELECT ON randomTwitter_by_month.* TO 'username'@'%';
--------------------------------
Scripts

getTweetsFromSQL.py is used to parse the results of an SQL query to a text file. To run, use do the following two steps.

1. Run in command prompt: 
ssh username@ssh.wwbp.org -i "path_to_private_key" -L 3306:127.0.0.1:3306:3306 -N

2. Run in different command prompt:
python getTweetsFromSQL.py <username> <sql query file> <path to output file>

getTaggedFile.py is used to tag the Tweets that were output from getTweetsFromSQL.py
Usage: python getTaggedFile.py <input file> <output file>
---------------------------------