"""
4. Application Health Checker:
Please write a script that can check the uptime of an application and determine if it is functioning correctly or not. The script must accurately assess the application's status by checking HTTP status codes. 
It should be able to detect if the application is 'up', meaning it is functioning correctly, or 'down', indicating that it is unavailable or not responding.
"""

import requests
import time
import argparse


def log_message(message, log_file):
    """
    Log a message to the log file and print it to the console.

    Args:
        message (str): The message to log.
        log_file (str): Path to the log file.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as file:
        file.write(f"{timestamp} - {message}\n")
    print(f"{timestamp} - {message}")


def check_application_status(url, status_codes_ok, log_file):
    """
    Check the application's status by sending a GET request to the URL and
    logging the HTTP status code.

    Args:
        url (str): The URL of the application to check.
        status_codes_ok (list): List of HTTP status codes that indicate the application is 'up'.
        log_file (str): Path to the log file.
    """
    try:
        response = requests.get(url)
        if response.status_code in status_codes_ok:
            log_message(
                f"Application is up. Status code: {response.status_code}", log_file
            )
        else:
            log_message(
                f"Application is down. Status code: {response.status_code}", log_file
            )
    except requests.RequestException as e:
        log_message(f"Application is down. Error: {e}", log_file)


def main(url, status_codes_ok, check_interval, log_file):
    """
    Continuously check the application's status at regular intervals.

    Args:
        url (str): The URL of the application to check.
        status_codes_ok (list): List of HTTP status codes that indicate the application is 'up'.
        check_interval (int): Time interval between checks in seconds.
        log_file (str): Path to the log file.
    """
    log_message("Starting uptime check...", log_file)
    while True:
        check_application_status(url, status_codes_ok, log_file)
        time.sleep(check_interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Application Uptime Monitoring Script")
    parser.add_argument("url", help="The URL of the application to check")
    parser.add_argument(
        "status_codes_ok",
        nargs="+",
        type=int,
        help="List of HTTP status codes that indicate the application is 'up'",
    )
    parser.add_argument(
        "check_interval", type=int, help="Time interval between checks in seconds"
    )
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    main(args.url, args.status_codes_ok, args.check_interval, args.log_file)
