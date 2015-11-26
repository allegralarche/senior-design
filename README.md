**** USAGE ****

Make sure you do this:
mysql -u root
GRANT SELECT ON randomTwitter_by_month.* TO 'username'@'localhost';
GRANT SELECT ON randomTwitter_by_month.* TO 'username'@'%';

First run in command prompt: 
ssh username@ssh.wwbp.org -i "path_to_private_key" -L 3306:127.0.0.1:3306:3306 -N

Second run in different command prompt:
python getSQLfile.py <username> <sql query file> <path to output file>