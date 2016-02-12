#!/usr/bin/python
import re
import sys
from optparse import OptionParser
import mysql.connector
from subprocess import call
import tempfile

# get command line arguments
parser = OptionParser()
parser.add_option("-d", "--database", dest="database", help="Database name")
parser.add_option("-u", "--username", dest="username", help="MySQL user name")
parser.add_option("-p", "--password", dest="password", help="MySQL password", default='')
parser.add_option("-o", "--hostname", dest="hostname", help="Hostname", default='localhost')
options, args = parser.parse_args()

# required options
if not options.database:
    parser.error('Database name not given')
if not options.username:
    parser.error('Usernamename not given')
if not options.password:
    parser.error('password name not given')
if not options.hostname:
    parser.error('hostname name not given')

# connect to db
print("Connecting to database")
mysql_connection = mysql.connector.connect(user=options.username, password=options.password,
                                        host=options.hostname, database=options.database)
mysql_cursor = mysql_connection.cursor()

# find posts with spam
print("Finding posts that contain seo spam")
query = "SELECT `ID`, `post_content` FROM `wp_posts` WHERE `post_content` like '%_all_wplink_%'"
mysql_cursor.execute(query)
posts = mysql_cursor.fetchall()
posts = [list(post) for post in posts]

if not posts:
    sys.stdout.write("No posts containing SEO spam found")
    sys.exit()

# remove the spam
print("Removing spam from html (not yet modifying the database)")
regex = re.compile('<div class="_all_wplink_.*?>.*?</div>', re.S)
for post in posts:
    post_id = post[0]
    original_content = post[1]

    modified_content = re.sub(regex, '', original_content)
    post.append(modified_content)

# create files for diff
originals_file = tempfile.NamedTemporaryFile()
modified_file = tempfile.NamedTemporaryFile()

# write each posts original and modified contents to the appropriate temp files
print("Writing old and new html to files for meld diff")
for post in posts:
    post_id = post[0]
    original_content = post[1]
    modified_content = post[2]

    originals_file.write(original_content.encode('utf8') + '\n')
    modified_file.write(modified_content.encode('utf8') + '\n')

# run meld
print("Opening meld - please check if you are happy with the changes to be made, "
                "then close meld and accept the prompt that will follow")
call(["meld", originals_file.name, modified_file.name])

# ask for confirmation
confirmed = False
while True:
    print('')
    sys.stdout.write("Do you confirm you have checked the diff in meld, "
                        "backed up your database, are happy to proceed with "
                        "the modifications to your database, and you agree "
                        "not to hold the developer of this script "
                        "responsible for what happens next? [y/n]")
    choice = raw_input().lower().strip()
    if choice == 'y':
        confirmed = True
        break
    elif choice == 'n':
        break
    else:
        sys.stdout.write("Please respond with 'y' or 'n'.\n")

# update db
if confirmed:
    # update db with modified html
    print("Updating the database with the modified html")
    counter = 1
    for post in posts:
        post_id = post[0]
        original_content = post[1]
        modified_content = post[2]

        query = 'UPDATE `wp_posts` SET `post_content` = %s WHERE `ID` = %s'
        mysql_cursor.execute(query, (modified_content, post_id))
else:
    print("No changes have been made to your database")

# close connection and files
print("Script complete!")
mysql_connection.close()
originals_file.close()
modified_file.close()
