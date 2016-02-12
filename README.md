# wordpress-seo-spam-remover

A tool to remove SEO spam from your wordpress website. This malware will appear on sucuri sitecheck with the definition "MW:SPAM:SEO?s" and look something like this:

    <div class="_all_wplink_rwPUIFu9_cc" style="position:absolute;opacity:0.001;z-index:10;filter:alpha(opacity=0)"> ... spammy text and links to knockoff fashion sites ... </div>

The script works in the following way:

- connects to your wordpress mysql database
- finds all posts containing the string "\_all\_wplink\_"
- uses a simple regex to identify and remove the div from the post html
- presents you with a diff of all the changes it will make to the database
- asks you to confirm you are happy with the diff
- if you select yes it will update your database accordingly
- if you select no, no changes to your database will be made

# Setup

- Install mysql-connector-python (http://stackoverflow.com/questions/34489271/i-cannot-install-mysql-connector-python-using-pip)
- Install meld

# Usage

    python wordpress_seo_spam_remover.py -d mysql_database_name -u mysql_username -p mysql_password -o mysql_hostname

# Disclaimer

I have personally used this script and it has worked perfectly; I am releasing it to the open source community because it may be of help to somebody else, but if it breaks anything or does anything that you didn't expect, I take absolutely no responsibility! Before using it, make sure you read and fully understand what it will do, and of course, as always, make full backups of your website so you can restore it to it's previous state in case anything goes wrong.

This script comes with no warranty and I accept no responsibility for it's use.

# Support

If you need any support feel free to contact me, the developer, Max Mumford, on my website http://www.cocept.io
