import json
import timeit
import pandas as pd
from datasketch import HyperLogLog


LOG_FILE_PATH = "task_2/lms-stage-access.log"


def load_ip_addresses(log_file: str) -> list:
    ip_addresses = []

    with open(log_file, "r", encoding="utf-8") as file:
        for row in file:
            try:
                log_entry = json.loads(row)
                ip_address = log_entry.get("remote_addr")
                if ip_address:
                    ip_addresses.append(ip_address.encode('utf-8'))
            except json.JSONDecodeError:
                continue

    return ip_addresses


def count_unique_simple(ip_addresses: list) -> int:
    return len(set(ip_addresses))


def count_unique_hyperloglog(ip_addresses: list, presision: int = 14) -> int:
    hll = HyperLogLog(p=presision)
    for ip in ip_addresses:
        hll.update(ip)
    return int(hll.count())


def compare_methods(log_file: str):
    ip_addresses = load_ip_addresses(log_file)

    time_simple = timeit.timeit(lambda: count_unique_simple(ip_addresses), number=1)
    count_simple = count_unique_simple(ip_addresses)

    time_hll = timeit.timeit(lambda: count_unique_hyperloglog(ip_addresses), number=1)
    count_hll = count_unique_hyperloglog(ip_addresses)

    results = pd.DataFrame(
        {
            "Метод": ["Точний підрахунок", "HyperLogLog"],
            "Унікальні елементи": [count_simple, count_hll],
            "Час виконання (сек.)": [time_simple, time_hll],
        }
    )

    return results


if __name__ == "__main__":
    results = compare_methods(LOG_FILE_PATH)

    print("Результати порівняння:")
    print(results)
