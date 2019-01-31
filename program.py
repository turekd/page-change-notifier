import requests
from pathlib import Path
import smtplib

# Config
email = "target_email_here"

server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server_ssl.ehlo()
server_ssl.login("login", "password")

pages = {
    "page1": "http://example.com/1.html",
    "page2": "http://example.com/2.html",
    "page3": "http://example.com/3.html",
}

# Code

for name, url in pages.items():
    print("###Processing ", name, "-", url)
    content = requests.get(url).text
    cache_name = "local_db/" + name + ".txt"
    cache_exists = Path(cache_name)
    if cache_exists.is_file():
        print("Local content found")
        cache_read = open(cache_name, "r")
        cache_read_content = cache_read.read()
        cache_read.close()
        if content != cache_read_content:
            print("Different content. Updating")
            open(cache_name, "w").close()
            cache_write = open(cache_name, "w")
            cache_write.write(content)
            cache_write.close()
            print("Local cache updated.")
            print("Sending email")
            # Send the mail
            msg = "Change on website " + name + " has been detected"
            server_ssl.sendmail("dturek.test@gmail.com", email, msg)
            print("OK")
        else:
            print("Contents are identical. Nothing to do")
    else:
        print("Creating", cache_name)
        save_cache = open(cache_name, "w")
        save_cache.write(content)
        save_cache.close()
    print("\n")
