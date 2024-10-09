import requests
import datetime
import time
import os

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

# ASCII Art for the Tool Name
tool_name = r"""
 _  _  ____  ____  _  _   __  ____  ___  _  _  __  __ _   ___  ____  ____   __  
( \/ )/ ___)/ ___)/ )( \ / _\(_  _)/ __)/ )( \(  )(  ( \ / __)(  _ \(  _ \ /  \ 
 )  ( \___ \\___ \\ /\ //    \ )( ( (__ ) __ ( )( /    /( (_ \ ) __/ )   /(  O )
(_/\_)(____/(____/(_/\_)\_/\_/(__) \___)\_)(_/(__)\_)__) \___/(__)  (__\_) \__/ 

                     XSSwatchingPro v1.0
                Made by: HACKINTER
                Founded on: {date}
                Description: An automatic tool for testing XSS vulnerabilities on specified domains.
"""

def display_info():
    print(tool_name.format(date=datetime.datetime.now().strftime('%Y-%m-%d')))
    print("=" * 75)

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
        url = f"{domain}?payload={payload}"  # Modify URL to include payload in query string
        try:
            loading_indicator()  # Show loading indicator while waiting for response
            
            if method.upper() == 'POST':
                response = requests.post(url, data={'payload': payload})
            else:  # Default to GET
                response = requests.get(url)

            time.sleep(2)  # Delay between requests for analysis
            
            # Analyze response for vulnerability
            if payload in response.text:
                result = f"{Colors.FAIL}💥 Possible XSS vulnerability found: {url} with payload: {payload}{Colors.ENDC}"
            else:
                result = f"{Colors.FAIL}❎ No vulnerability found; URL is safe: {url} with payload: {payload}{Colors.ENDC}"
        except requests.exceptions.RequestException:
            result = f"{Colors.WARNING}⚠️ Error connecting to server; URL is not accessible for testing: {url}{Colors.ENDC}"
        
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
        filename = f"{base_filename[:-4]}{count}.txt"
        count += 1
        
    with open(filename, 'w') as result_file:
        result_file.write("\n".join(results))
        print(f"{Colors.OKGREEN}✅ Results saved to {filename}{Colors.ENDC}")

if __name__ == "__main__":
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
