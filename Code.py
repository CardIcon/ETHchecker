import requests
import json
import time
from eth_account import Account
import secrets
import sys
import os

# --- Project & Author Info ---
__author__ = "XZLKT"
__maintainer__ = "CardIcon (@CardIcon)"
__version__ = "1.0.0"
__description__ = "Script for generating random Ethereum wallets and checking their balance via Etherscan API. For educational and research purposes only."

# --- CONFIGURATION ---
# ETHERSCAN_API_KEY must be set as an environment variable for security.
# Get your free key: https://etherscan.io/myaccount
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")

ETHERSCAN_API_URL = "https://api.etherscan.io/api"
OUTPUT_FILE = "found_wallets.txt"

# Delay between API requests to avoid hitting rate limits (e.g., 0.2s for 5 req/sec).
REQUEST_DELAY = 0.2

# Etherscan free plan daily call limit.
DAILY_CALL_LIMIT = 100000

# --- CONSOLE COLORS ---
COLOR_RED = '\033[91m'
COLOR_RESET = '\033[0m'
COLOR_YELLOW = '\033[93m'
COLOR_GREEN = '\033[92m'
COLOR_BLUE = '\033[94m'
COLOR_CYAN = '\033[96m'

# --- HELPER FUNCTIONS ---

def generate_wallet():
    """Generates a new random Ethereum private key and its corresponding address."""
    account = Account.create()
    return account.key.hex(), account.address

def get_balance(address, api_key):
    """
    Checks the ETH balance for a given address using Etherscan API.
    Returns balance in Wei (smallest ETH unit), -1 for API/request errors, or -2 for invalid/missing API key.
    """
    if not api_key:
        print(f" {COLOR_RED}[!] ERROR: Etherscan API key not set in environment variable.{COLOR_RESET}")
        return -2

    params = {
        "module": "account",
        "action": "balance",
        "address": address,
        "apikey": api_key,
        "tag": "latest"
    }

    try:
        response = requests.get(ETHERSCAN_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "1" and data.get("message") == "OK":
            return int(data.get("result", "0"))
        elif data.get("message") == "NOTOK" and "Invalid API Key" in data.get("result", ""):
             print(f" {COLOR_RED}[!] ERROR: Invalid Etherscan API key. Check your configuration. {COLOR_RESET}")
             return -2
        else:
            error_message = data.get('result', 'Unknown API error')
            if "rate limit" in error_message.lower() or "limit exceeded" in error_message.lower():
                 print(f" {COLOR_YELLOW}[!] Rate limit exceeded or too frequent requests for {address}. {error_message}{COLOR_RESET}")
            else:
                print(f" {COLOR_RED}[!] API error for address {address}: {error_message}{COLOR_RESET}")
            return -1

    except requests.exceptions.RequestException as e:
        print(f" {COLOR_RED}[!] Request error for address {address}: {e}{COLOR_RESET}")
        return -1
    except json.JSONDecodeError:
         print(f" {COLOR_RED}[!] Failed to parse JSON response for address {address}{COLOR_RESET}")
         return -1
    except ValueError:
         print(f" {COLOR_RED}[!] Failed to convert balance to number for address {address}. Received: {data.get('result')}{COLOR_RESET}")
         return -1

def wei_to_eth(balance_wei):
    """Converts balance from Wei to Ether."""
    return balance_wei / 1e18

# --- MAIN PROGRAM ---

print(f"{COLOR_BLUE}Starting Ethereum wallet balance scanner...{COLOR_RESET}")

if not ETHERSCAN_API_KEY:
    print(f"{COLOR_RED}!!! WARNING: 'ETHERSCAN_API_KEY' environment variable is not set. !!!{COLOR_RESET}")
    print(f"{COLOR_RED}!!! Please get a free API key from https://etherscan.io/myaccount and set it. !!!{COLOR_RESET}")
    print(f"{COLOR_RED}Example: export ETHERSCAN_API_KEY='YOUR_KEY_HERE'{COLOR_RESET}")
    sys.exit("Program stopped due to missing API key.")
else:
     print(f"{COLOR_GREEN}Etherscan API key detected.{COLOR_RESET}")

print(f"Wallets with balance > 0 will be saved to '{OUTPUT_FILE}'")
print(f"Configured request delay: {REQUEST_DELAY} sec ({1/REQUEST_DELAY} requests/sec)")
print(f"Daily API call limit (free plan): {DAILY_CALL_LIMIT}")
print(f"Press Ctrl+C to stop.{COLOR_RESET}")
print("-" * 60)

daily_calls_count = 0

try:
    while True:
        if daily_calls_count >= DAILY_CALL_LIMIT:
            print(f"\n{COLOR_RED}" + "=" * 60 + COLOR_RESET)
            print(f"{COLOR_RED}!!! DAILY API LIMIT ({DAILY_CALL_LIMIT} calls) REACHED. !!!{COLOR_RESET}")
            print(f"{COLOR_RED}!!! Further Etherscan API checks are not possible today. !!!{COLOR_RESET}")
            print(f"{COLOR_RED}" + "=" * 60 + COLOR_RESET + "\n")
            break

        daily_calls_count += 1
        private_key, address = generate_wallet()

        print(f"[{daily_calls_count: >6}/{DAILY_CALL_LIMIT}] Checking address: {address}", end="")

        balance_wei = get_balance(address, ETHERSCAN_API_KEY)

        if balance_wei == -1:
            print(" -> Skipping (API error, potentially temporary)")
            time.sleep(REQUEST_DELAY * 2)
            continue
        if balance_wei == -2:
             print(" -> CRITICAL ERROR: Invalid/missing API key. Stopping.")
             break

        balance_eth = wei_to_eth(balance_wei)

        if balance_wei > 0:
            print(f" -> {COLOR_GREEN}Balance: {balance_eth:.18f} ETH{COLOR_RESET}")
        else:
            print(f" -> Balance: {balance_eth:.18f} ETH")

        if balance_wei > 0:
            print("\n" + "=" * 70)
            print(f"{COLOR_CYAN}!!! WALLET WITH BALANCE FOUND !!!{COLOR_RESET}")
            print(f"  Address: {address}")
            print(f"  Private Key: {private_key}")
            print(f"  Balance: {balance_eth:.18f} ETH")
            print("=" * 70 + "\n")

            line_to_save = f"Private Key: {private_key}, Address: {address}, Balance: {balance_eth:.18f} ETH\n"

            try:
                with open(OUTPUT_FILE, "a") as f:
                    f.write(line_to_save)
                print(f"{COLOR_YELLOW}Information saved to '{OUTPUT_FILE}'{COLOR_RESET}")
            except IOError as e:
                print(f"{COLOR_RED}!!! ERROR WRITING TO FILE '{OUTPUT_FILE}': {e} !!!{COLOR_RESET}")

        time.sleep(REQUEST_DELAY)

except KeyboardInterrupt:
    print(f"\n{COLOR_YELLOW}Program stopped by user (Ctrl+C).{COLOR_RESET}")
except Exception as e:
    print(f"\n{COLOR_RED}An unexpected error occurred: {e}{COLOR_RESET}")

print(f"{COLOR_BLUE}Program finished.{COLOR_RESET}")
print(f"Total addresses checked (API attempts): {daily_calls_count}")
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, 'r') as f:
            found_count = sum(1 for line in f)
        print(f"Found wallets with balance > 0, written to '{OUTPUT_FILE}': {found_count}")
    except IOError:
         print(f"Could not count found wallets in '{OUTPUT_FILE}'.")
