from aiohttp import ClientResponseError, ClientSession, ClientTimeout, BasicAuth
from aiohttp_socks import ProxyConnector
from datetime import datetime
from colorama import *
import asyncio, json, pytz, re, os

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
        filename = "accounts.json"
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
        
    def save_tokens(self, new_accounts):
        filename = "tokens.json"
        try:
            if os.path.exists(filename) and os.path.getsize(filename) > 0:
                with open(filename, 'r') as file:
                    existing_accounts = json.load(file)
            else:
                existing_accounts = []

            account_dict = {acc["email"]: acc for acc in existing_accounts}

            for new_acc in new_accounts:
                account_dict[new_acc["email"]] = new_acc

            updated_accounts = list(account_dict.values())

            with open(filename, 'w') as file:
                json.dump(updated_accounts, file, indent=4)

            self.log_success("Tokens Saved", f"{len(new_accounts)} tokens updated")

        except Exception as e:
            self.log_error("Save Tokens Failed", str(e))
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
                    self.log_success("Connection Test", "Connected successfully")
                    return True
        except (Exception, ClientResponseError) as e:
            self.log_error("Connection Failed", str(e))
            return None
        
    async def request_otp(self, email: str, passcode: str, interlink_id: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/auth/send-otp-email-verify-login"
        data = json.dumps({"loginId":int(interlink_id), "passcode":int(passcode), "email":email})
        headers = {
            **self.HEADERS,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth, ssl=False) as response:
                        response.raise_for_status()
                        result = await response.json()
                        self.log_success("OTP Request", "OTP sent successfully")
                        return result
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    self.log_warning("OTP Request", f"Retrying... ({attempt + 1}/{retries})")
                    await asyncio.sleep(5)
                    continue
                else:
                    self.log_error("OTP Request Failed", str(e))
                    return None
        
    async def verify_otp(self, interlink_id: str, otp_code: str, proxy_url=None, retries=5):
        url = f"{self.BASE_API}/auth/check-otp-email-verify-login"
        data = json.dumps({"loginId":int(interlink_id), "otp":int(otp_code)})
        headers = {
            **self.HEADERS,
            "Content-Length": str(len(data)),
            "Content-Type": "application/json"
        }
        for attempt in range(retries):
            connector, proxy, proxy_auth = self.build_proxy_config(proxy_url)
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, proxy=proxy, proxy_auth=proxy_auth) as response:
                        response.raise_for_status()
                        result = await response.json()
                        self.log_success("OTP Verification", "OTP verified successfully")
                        return result
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    self.log_warning("OTP Verification", f"Retrying... ({attempt + 1}/{retries})")
                    await asyncio.sleep(5)
                    continue
                else:
                    self.log_error("OTP Verification Failed", str(e))
                    return None
        
    async def process_check_connection(self, email: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(email) if use_proxy else None
            self.log_info("Proxy", proxy if proxy else "No Proxy")

            is_valid = await self.check_connection(proxy)
            if is_valid: return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(email)
                await asyncio.sleep(1)
                continue

            return False

    async def process_accounts(self, email: str, passcode: str, interlink_id: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(email, use_proxy, rotate_proxy)
        if not is_valid:
            self.log_error("Account Processing", "Connection validation failed")
            return

        proxy = self.get_next_proxy_for_account(email) if use_proxy else None

        request = await self.request_otp(email, passcode, interlink_id, proxy)
        if not request: return

        timestamp = f"{Fore.CYAN}{datetime.now().astimezone(wib).strftime('%H:%M:%S')}{Style.RESET_ALL}"
        type_display = f"{Fore.BLUE}{Style.BRIGHT}INPUT    {Style.RESET_ALL}"
        otp_code = input(f"{timestamp} ┃ {type_display} ┃ {Fore.WHITE}Enter OTP Code → {Style.RESET_ALL}")

        verify = await self.verify_otp(interlink_id, otp_code, proxy)
        if not verify: return

        token = verify.get("data", {}).get("jwtToken")
        if not token:
            self.log_error("Token Error", "No token received from authentication")
            return

        if email and token:
            account_data = [{"email":email, "token":token}]
            self.save_tokens(account_data)
            self.log_success("Account Setup", f"{self.mask_account(email)} completed successfully")
        else:
            self.log_error("Setup Failed", "Invalid response data")
    
    async def main(self):
        try:
            accounts = self.load_accounts()
            if not accounts:
                self.log_error("No Accounts", "No accounts loaded from accounts.json")
                return
            
            proxy_choice, rotate_proxy = self.print_question()

            self.welcome()

            use_proxy = True if proxy_choice == 1 else False
            if use_proxy:
                await self.load_proxies()

            print(f"\n{Fore.CYAN}┌───────────────── Processing Accounts ────────────────{Style.RESET_ALL}")
            for idx, account in enumerate(accounts, start=1):
                email = account["email"]
                passcode = account["passcode"]
                interlink_id = account["interlinkId"]

                if not "@" in email or not passcode or not interlink_id:
                    self.log_error("Invalid Data", "Missing email, passcode or interlinkId")
                    continue

                self.log_process(f"Processing Account {idx}/{len(accounts)}", self.mask_account(email))

                await self.process_accounts(email, passcode, interlink_id, use_proxy, rotate_proxy)
                await asyncio.sleep(3)
                if idx < len(accounts):
                    print(f"{Fore.CYAN}├──────────────────────────────────────────────────{Style.RESET_ALL}")

            print(f"{Fore.CYAN}└──────────────────────────────────────────────────{Style.RESET_ALL}")
            self.log_success("Setup Complete", "All accounts processed successfully")

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
