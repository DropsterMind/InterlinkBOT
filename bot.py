from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout,
    BasicAuth
)
from aiohttp_socks import ProxyConnector
from base64 import urlsafe_b64decode
from datetime import datetime
from colorama import *
import asyncio, time, json, pytz, re, os

wib = pytz.timezone('Asia/Jakarta')

class Interlink:
    def __init__(self) -> None:
        self.HEADERS = {
            "Accept-Encoding": "*/*",
            "User-Agent": "okhttp/4.12.0",
            "Accept-Encoding": "gzip"
        }
        self.BASE_API = "https://prod.interlinklabs.ai/api/v1"
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message_type, message, details="", color=Fore.WHITE):
        timestamp = f"{Fore.CYAN}{datetime.now().astimezone(wib).strftime('%H:%M:%S')}{Style.RESET_ALL}"
        type_display = f"{color}{Style.BRIGHT}{message_type:<10}{Style.RESET_ALL}"
        message_display = f"{Fore.WHITE}{message}{Style.RESET_ALL}"
        details_display = f"{Fore.YELLOW}{details}{Style.RESET_ALL}" if details else ""
        
        print(f"{timestamp} ┃ {type_display} ┃ {message_display} {details_display}", flush=True)

    def log_success(self, message, details=""):
        self.log("SUCCESS", message, details, Fore.GREEN)

    def log_error(self, message, details=""):
        self.log("ERROR", message, details, Fore.RED)

    def log_warning(self, message, details=""):
        self.log("WARNING", message, details, Fore.YELLOW)

    def log_info(self, message, details=""):
        self.log("INFO", message, details, Fore.BLUE)

    def log_process(self, message, details=""):
        self.log("PROCESS", message, details, Fore.MAGENTA)

    def welcome(self):
        self.clear_terminal()
        print(f"""
{Fore.CYAN + Style.BRIGHT}
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    ██╗███╗   ██╗████████╗███████╗██████╗ ██╗     ██╗███╗   ██╗║
║    ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██║     ██║████╗  ██║║
║    ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝██║     ██║██╔██╗ ██║║
║    ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██║     ██║██║╚██╗██║║
║    ██║██║ ╚████║   ██║   ███████╗██║  ██║███████╗██║██║ ╚████║║
║    ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                {Fore.GREEN}Interlink-BOT by DROPSTERMIND{Fore.CYAN}               ║
╚════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
        """)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "tokens.json"
        try:
            if not os.path.exists(filename):
                self.log_error("File Not Found", f"{filename} not found")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    self.log_success("Accounts Loaded", f"{len(data)} accounts found")
                    return data
                return []
        except json.JSONDecodeError:
            self.log_error("JSON Error", "Invalid JSON format")
            return []
    
    async def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log_error("File Not Found", f"{filename} not found")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log_warning("No Proxies", "No proxies found in file")
                return

            self.log_success("Proxies Loaded", f"Total: {len(self.proxies)} proxies")
        
        except Exception as e:
            self.log_error("Proxy Load Failed", str(e))
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy:
            return None, None, None

        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy)
            return connector, None, None

        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                username, password, host_port = match.groups()
                clean_url = f"http://{host_port}"
                auth = BasicAuth(username, password)
                return None, clean_url, auth
            else:
                return None, proxy, None

        raise Exception("Unsupported Proxy Type.")
    
    def decode_token(self, token: str):
        try:
            header, payload, signature = token.split(".")
            decoded_payload = urlsafe_b64decode(payload + "==").decode("utf-8")
            parsed_payload = json.loads(decoded_payload)
            exp_time = parsed_payload["exp"]
            
            return exp_time
        except Exception as e:
            return None
    
    def mask_account(self, account):
        if "@" in account:
            local, domain = account.split('@', 1)
            mask_account = local[:3] + '*' * 3 + local[-3:]
            return f"{mask_account}@{domain}"

    def print_question(self):
        print(f"\n{Fore.CYAN}┌───────────────── Configuration ─────────────────{Style.RESET_ALL}")
        while True:
            try:
                print(f"{Fore.WHITE}│ 1. Run With Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE}│ 2. Run Without Proxy{Style.RESET_ALL}")
                proxy_choice = int(input(f"{Fore.BLUE}│ Choose [1/2] → {Style.RESET_ALL}").strip())

                if proxy_choice in [1, 2]:
                    proxy_type = (
                        "With" if proxy_choice == 1 else 
                        "Without"
                    )
                    self.log_success(f"Run {proxy_type} Proxy Selected")
                    break
                else:
                    self.log_error("Invalid choice", "Please enter 1 or 2")
            except ValueError:
                self.log_error("Invalid input", "Enter a number (1 or 2)")

        rotate_proxy = False
        if proxy_choice == 1:
            while True:
                rotate_proxy = input(f"{Fore.BLUE}│ Rotate Invalid Proxy? [y/n] → {Style.RESET_ALL}").strip()
                if rotate_proxy in ["y", "n"]:
                    rotate_proxy = rotate_proxy == "y"
                    break
                else:
                    self.log_error("Invalid input", "Enter 'y' or 'n'")

        print(f"{Fore.CYAN}└──────────────────────────────────────────────────{Style.RESET_ALL}")
        return proxy_choice, rotate_proxy
    
    async def check_connection(self, proxy_url=None):
        connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=10)) as session:
                async with session.get(url="https://api.ipify.org?format=json", proxy=proxy, proxy_auth=proxy_auth) as response:
                    response.raise_for_status()
                    return True
        except (Exception, ClientResponseError) as e:
            self.log_error("Connection Failed", str(e))
            return None
    
    async def token_balance(self, email: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/token/get-token"
        headers = {
            **self.HEADERS,
            "Authorization": f"Bearer {self.access_tokens[email]}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log_error("GET Token Balance Failed", str(e))

        return None
            
    async def claimable_check(self, email: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/token/check-is-claimable"
        headers = {
            **self.HEADERS,
            "Authorization": f"Bearer {self.access_tokens[email]}"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, proxy=proxy, proxy_auth=proxy_auth, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log_error("GET Claim Status Failed", str(e))

        return None
            
    async def claim_airdrop(self, email: str, proxy_url=None, retries=1):
        url = f"{self.BASE_API}/token/claim-airdrop"
        headers = {
            **self.HEADERS,
            "Authorization": f"Bearer {self.access_tokens[email]}",
            "Content-Length": "2",
            "Content-Type": "application/json"
        }
        await asyncio.sleep(3)
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, json={}, proxy=proxy, proxy_auth=proxy_auth, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.log_error("Claim Failed", str(e))

        return None
    
    async def process_check_connection(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None
            self.log_info("Proxy", proxy if proxy else "No Proxy")

            is_valid = await self.check_connection(proxy)
            if is_valid: 
                self.log_success("Connection Test", "Connected successfully")
                return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(email)
                await asyncio.sleep(1)
                continue

            return False
            
    async def process_accounts(self, email: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(email, use_proxy, rotate_proxy)
        if not is_valid: 
            self.log_error("Account Processing", "Connection validation failed")
            return

        proxy = self.get_next_proxy_for_account(email) if use_proxy else None

        balance = await self.token_balance(email, proxy)
        if balance:
            token_balance = balance.get("data", {}).get("interlinkTokenAmount", 0)
            silver_balance = balance.get("data", {}).get("interlinkSilverTokenAmount", 0)
            gold_balance = balance.get("data", {}).get("interlinkGoldTokenAmount", 0)
            diamond_balance = balance.get("data", {}).get("interlinkDiamondTokenAmount", 0)

            self.log_success("Balance Check", "Retrieved successfully")
            self.log_info("Interlink", f"{token_balance}")
            self.log_info("Silver", f"{silver_balance}")
            self.log_info("Gold", f"{gold_balance}")
            self.log_info("Diamond", f"{diamond_balance}")

        claimable = await self.claimable_check(email, proxy)
        if claimable:
            is_claimable = claimable.get("data", {}).get("isClaimable", False)

            if is_claimable:
                claim = await self.claim_airdrop(email, proxy)
                if claim:
                    reward = claim.get("data") or "N/A"
                    self.log_success("Claim Successful", f"Reward: {reward}")
            
            else:
                next_frame_ts = claimable.get("data", {}).get("nextFrame", 0) / 1000
                next_frame_wib = datetime.fromtimestamp(next_frame_ts).astimezone(wib).strftime('%x %X %Z')
                self.log_warning("Already Claimed", f"Next claim: {next_frame_wib}")
        
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log_error("No Accounts", "No accounts loaded")
                return

            proxy_choice, rotate_proxy = self.print_question()

            while True:
                self.welcome()
                self.log_success("Accounts Loaded", f"Total: {len(accounts)} accounts")

                use_proxy = True if proxy_choice == 1 else False
                if use_proxy:
                    await self.load_proxies()
        
                print(f"\n{Fore.CYAN}┌───────────────── Processing Accounts ────────────────{Style.RESET_ALL}")
                for idx, account in enumerate(accounts, start=1):
                    if account:
                        email = account["email"]
                        token = account["token"]
                        
                        self.log_process(f"Processing Account {idx}/{len(accounts)}", self.mask_account(email))

                        if not "@" in email or not token:
                            self.log_error("Invalid Data", "Missing email or token")
                            continue

                        self.log_info("Account", self.mask_account(email))

                        exp_time = self.decode_token(token)
                        if not exp_time:
                            self.log_error("Token Error", "Invalid token format")
                            continue

                        if int(time.time()) > exp_time:
                            self.log_error("Token Expired", "Token has expired")
                            continue

                        self.access_tokens[email] = token
                        
                        await self.process_accounts(email, use_proxy, rotate_proxy)
                        await asyncio.sleep(3)
                        if idx < len(accounts):
                            print(f"{Fore.CYAN}├──────────────────────────────────────────────────{Style.RESET_ALL}")

                print(f"{Fore.CYAN}└──────────────────────────────────────────────────{Style.RESET_ALL}")

                self.log_success("All Accounts Processed", "Waiting for next cycle")
                seconds = 4 * 60 * 60
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN}{datetime.now().astimezone(wib).strftime('%H:%M:%S')}{Style.RESET_ALL} ┃ "
                        f"{Fore.MAGENTA}{Style.BRIGHT}WAIT     {Style.RESET_ALL} ┃ "
                        f"{Fore.WHITE}Next cycle in {formatted_time}...{Style.RESET_ALL}",
                        end="\r"
                    )
                    await asyncio.sleep(1)
                    seconds -= 1
                print()

        except Exception as e:
            self.log_error("Main Process Error", str(e))
            raise e

if __name__ == "__main__":
    try:
        bot = Interlink()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"\n{Fore.CYAN}{datetime.now().astimezone(wib).strftime('%H:%M:%S')}{Style.RESET_ALL} ┃ "
            f"{Fore.RED}{Style.BRIGHT}EXIT     {Style.RESET_ALL} ┃ "
            f"{Fore.WHITE}Interlink-BOT by DROPSTERMIND - Stopped by user{Style.RESET_ALL}"
        )
