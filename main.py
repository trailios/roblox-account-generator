from src.roblox import Roblox
from threading  import Thread
from random     import choice
from src        import Log

proxies = open("input/proxies.txt").read().splitlines()
http_version = Log.prompt("http version (h1/h2/h3/auto, default: auto): ")
debug = Log.prompt("Print errors? (yes/no, default: no): ")

def worker() -> None:
    while True:
        try:
            r = Roblox(choice(proxies), http_version)
            r.signup()
        except Exception as e:
            if debug == "yes":
                Log.error("Failed to create account: " + str(e))
            continue

if __name__ == "__main__":
    amount_threads = int(Log.prompt("Amount of threads (default: 20): ")) or 20

    threads: list[Thread] = []

    for i in range(amount_threads):
        thread = Thread(target=worker)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()