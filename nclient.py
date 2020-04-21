#!/usr/bin/env python3
import sys
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
from subprocess import check_call


def _start_client():
    check_call(["python3", "client.py"])


def main():
    parser = argparse.ArgumentParser(description="Client runner")
    parser.add_argument("--count", help="Number of clients", default=1, type=int)

    args = parser.parse_args()
    count = args.count

    print("Starting %d client" % count)

    try:
        with ThreadPoolExecutor(max_workers=count) as pool:
            for i in range(count):
                pool.submit(_start_client)
    except Exception as error:
        print(str(error))
        return 1


if __name__ == "__main__":
    main()
