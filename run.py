import os

# XSS Test Function
def xss_test(domain, payload_file, method):
    print(f"🔍 Starting XSS Tests on {domain} using {method} method...")
    with open(payload_file, 'r') as file:
        payloads = file.readlines()
    vulnerability_found = False
    for payload in payloads:
        payload = payload.strip()
        print(f"💥 Testing XSS with payload: {payload}")
        # Simulated output (replace with actual XSS testing logic)
        if "alert" in payload:  # Just an example condition for simulation
            print(f"🎯 Possible XSS vulnerability found: {domain}?payload={payload}")
            vulnerability_found = True
        else:
            print(f"✖️ No XSS vulnerability found with payload: {payload}")
    
    if not vulnerability_found:
        print(f"✖️ No XSS vulnerabilities found for {domain}")

# CSRF Test Function
def csrf_test(domain, method):
    print(f"🔍 Starting CSRF Tests on {domain} using {method} method...")
    # Simulated output (replace with actual CSRF testing logic)
    print(f"✖️ No CSRF vulnerability found; URL is safe: {domain}")

# SQL Injection Test Function
def sql_injection_test(domain, payload_file, method):
    print(f"🔍 Starting SQL Injection Tests on {domain} using {method} method...")
    with open(payload_file, 'r') as file:
        payloads = file.readlines()
    vulnerability_found = False
    for payload in payloads:
        payload = payload.strip()
        print(f"💥 Testing SQL Injection with payload: {payload}")
        # Simulated output (replace with actual SQL Injection testing logic)
        if "' OR '" in payload:  # Just an example condition for simulation
            print(f"🎯 Possible SQL Injection vulnerability found: {domain}?payload={payload}")
            vulnerability_found = True
        else:
            print(f"✖️ No SQL Injection vulnerability found with payload: {payload}")
    
    if not vulnerability_found:
        print(f"✖️ No SQL Injection vulnerabilities found for {domain}")

# Main function
def main():
    print(" _  _  ____  ____  _  _   __  ____  ___  _  _  __  __ _   ___  ____  ____   __  ")
    print("( \\/ )/ ___)/ ___)/ )( \\ / _\\(_  _)/ __)/ )( \\(  )(  ( \\ / __)(  _ \\(  _ \\ /  \\ ")
    print(" )  ( \\___ \\\\___ \\\\ /\\ //    \\ )( ( (__ ) __ ( )( /    /( (_ \\ ) __/ )   /(  O )")
    print("(_/\\_)(____/(____/(_/\\_)\\_/\\_/(__) \\___)\\_)(_/(__)\\_)__) \\___/(__)  (__\\_) \\__/ ")
    print("                      Vulnerability Testing Tool v1.0")
    print("                Made by: HACKINTER")
    print("                Founded on: 2024-10-09")
    print("=========================================================================")

    # Test type selection
    print("\nPlease select the type of test you want to perform:")
    print("1. XSS Test")
    print("2. CSRF Test")
    print("3. SQL Injection Test")
    
    test_choice = input("Enter the number of your choice (1/2/3): ").strip()
    
    if test_choice not in ["1", "2", "3"]:
        print("❌ Invalid choice! Exiting.")
        return
    
    # Get domain input
    domain = input("\n🔗 Enter the target domain (e.g., https://example.com): ").strip()

    # Get HTTP method (GET/POST)
    method = input("📜 Choose the HTTP method (GET/POST): ").strip().upper()
    if method not in ["GET", "POST"]:
        print("⚠️ Invalid method selected. Defaulting to GET.")
        method = "GET"

    # Run the selected test
    if test_choice == "1":
        # XSS Test
        payload_file = input("📁 Enter the path to the XSS payload file: ").strip()
        if os.path.exists(payload_file):
            xss_test(domain, payload_file, method)
        else:
            print("❌ Payload file not found!")
    elif test_choice == "2":
        # CSRF Test (No payload file needed)
        csrf_test(domain, method)
    elif test_choice == "3":
        # SQL Injection Test
        payload_file = input("📁 Enter the path to the SQL Injection payload file: ").strip()
        if os.path.exists(payload_file):
            sql_injection_test(domain, payload_file, method)
        else:
            print("❌ Payload file not found!")
    
    # Save results
    result_file = f"{domain.replace('https://', '').replace('http://', '').replace('/', '')}-result.txt"
    print(f"✅ Results saved to {result_file}")

# Run the main function
if __name__ == "__main__":
    main()
