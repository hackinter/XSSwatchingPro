import os
import requests
import datetime
import time
import urllib.parse
import shutil

# ANSI color codes for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Function to clear terminal screen
def clear_screen():
    if os.name == 'posix':
        os.system('clear')  # For Linux/OS X
    else:
        os.system('cls')  # For Windows

# ASCII Art for the Tool Name (Centered)
tool_name = r"""

██╗      ██████╗ ██╗  ██╗██╗ █████╗ 
██║     ██╔═══██╗╚██╗██╔╝██║██╔══██╗
██║     ██║   ██║ ╚███╔╝ ██║███████║
██║     ██║   ██║ ██╔██╗ ██║██╔══██║
███████╗╚██████╔╝██╔╝ ██╗██║██║  ██║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
                        LOXIA__v1.0
                        Made by:LOXIA@HACKINTER
"""

def display_info():
    terminal_width = shutil.get_terminal_size().columns
    centered_tool_name = '\n'.join([line.center(terminal_width) for line in tool_name.splitlines()])
    print(centered_tool_name)
    print("=" * terminal_width)

def load_payloads(filepath):
    """Load payloads from a specified file."""
    if not os.path.isfile(filepath):
        print(f"{Colors.FAIL}🚨 Payloads file not found: {filepath}{Colors.ENDC}")
        return []
    with open(filepath, 'r') as file:
        payloads = [line.strip() for line in file if line.strip()]  # Remove empty lines
    print(f"{Colors.OKGREEN}✅ Loaded {len(payloads)} payloads from {filepath}{Colors.ENDC}")
    return payloads

def loading_indicator():
    """Display a loading indicator."""
    for _ in range(3):
        print(f"{Colors.WARNING}🔄 Loading{'.' * _}{Colors.ENDC}", end='\r')
        time.sleep(0.5)
    print(" " * 20, end='\r')  # Clear the loading line

def xss_test(domain, payloads, method):
    print(f"\n{Colors.OKBLUE}🔍 Starting XSS Tests on {domain} using {method} method...\n{Colors.ENDC}")
    results = []
    for payload in payloads:
        encoded_payload = urllib.parse.quote(payload)
        
        # Check if the URL already contains '?payload=' to avoid appending it again
        if "?payload=" in domain:
            url = f"{domain}&payload={encoded_payload}"  # Append with '&' if '?payload=' is already present
        else:
            url = f"{domain}?payload={encoded_payload}"  # Add '?payload=' if it's the first one
        
        try:
            loading_indicator()  # Show loading indicator while waiting for response
            
            if method.upper() == 'POST':
                response = requests.post(domain, data={'payload': payload})
            else:  # Default to GET
                response = requests.get(url)

            time.sleep(2)  # Delay between requests for analysis
            
            # Analyze response for vulnerability
            if payload in response.text:
                result = f"{Colors.FAIL}💥 Possible XSS vulnerability found: {url} with payload: {payload}{Colors.ENDC}"
            else:
                result = f"{Colors.OKGREEN}❌No vulnerability found; URL is safe: {url} with payload: {payload}{Colors.ENDC}"
        except requests.exceptions.RequestException as e:
            result = f"{Colors.WARNING}⚠️ Error connecting to server: {e}; URL: {url}{Colors.ENDC}"
        
        results.append(result)
        print(result)  # Print each result

    print("\n📊 Analysis complete. Summary of results:")
    for res in results:
        print(res)

    # Save results to a file with dynamic naming
    base_filename = f"{domain.replace('https://', '').replace('http://', '').replace('/', '')}-result.txt"
    filename = base_filename
    count = 1
    while os.path.isfile(filename):
        filename = f"{base_filename[:-4]}_{count}.txt"
        count += 1
        
    save_option = input(f"{Colors.OKBLUE}💾 Do you want to save the results to a file? (Y/N): {Colors.ENDC}")
    if save_option.strip().lower() == 'y':
        with open(filename, 'w') as result_file:
            result_file.write("\n".join(results))
            print(f"{Colors.OKGREEN}✅ Results saved to {filename}{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}⚠️ Results not saved.{Colors.ENDC}")

if __name__ == "__main__":
    clear_screen()  # Clear the terminal before starting the tool
    display_info()
    
    target_domain = input(f"{Colors.OKBLUE}🔗 Enter the target domain (e.g., https://example.com): {Colors.ENDC}")
    
    # User specifies file path
    payload_file_path = input(f"{Colors.OKBLUE}📁 Enter the path to the payload file: {Colors.ENDC}")
    
    # Method selection
    method = input(f"{Colors.OKBLUE}📜 Choose the HTTP method (GET/POST): {Colors.ENDC}").strip().upper()
    if method not in ['GET', 'POST']:
        print(f"{Colors.FAIL}⚠️ Invalid method selected. Defaulting to GET.{Colors.ENDC}")
        method = 'GET'

    xss_payloads = load_payloads(payload_file_path)
    if not xss_payloads:
        print(f"{Colors.FAIL}⚠️ No payloads available for testing.{Colors.ENDC}")
    else:
        # Testing against subdomains
        subdomains = [target_domain, f"sub1.{target_domain}", f"sub2.{target_domain}"]  # Add more subdomains as needed
        for sub in subdomains:
            print(f"\n{Colors.OKBLUE}🔍 Testing subdomain: {sub}{Colors.ENDC}")
            xss_test(sub, xss_payloads, method)
