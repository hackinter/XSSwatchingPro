def main():
    print("""
     _  _  ____  ____  _  _   __  ____  ___  _  _  __  __ _   ___  ____  ____   __  
    ( \/ )/ ___)/ ___)/ )( \ / _\(_  _)/ __)/ )( \(  )(  ( \ / __)(  _ \(  _ \ /  \ 
     )  ( \___ \\___ \\ /\ //    \ )( ( (__ ) __ ( )( /    /( (_ \ ) __/ )   /(  O )
    (_/\_)(____/(____/(_/\_)\_/\_/(__) \___)\_)(_/(__)\_)__) \___/(__)  (__\_) \__/ 
    
                         Vulnerability Testing Tool v1.0
                    Made by: HACKINTER | Copyright © 2024
        ===========================================================
        """)
    
    print("🎯 Choose the type of test to run:")
    print("1. XSS Testing")
    print("2. CSRF Testing")
    print("3. SQL Injection Testing")
    
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        print("🎯 XSS Testing Selected")
        test_type = "XSS"
    elif choice == '2':
        print("🎯 CSRF Testing Selected")
        test_type = "CSRF"
    elif choice == '3':
        print("🎯 SQL Injection Testing Selected")
        test_type = "SQL Injection"
    else:
        print("✖️ Invalid choice! Please select a valid test.")
        return

    # Input for domain and payload path
    domain = input("🔗 Enter the target domain (e.g., https://example.com): ")
    payload_path = input("📁 Enter the path to the payload file: ")

    # Select HTTP method (GET or POST)
    http_method = input("📜 Choose the HTTP method (GET/POST): ").upper()
    if http_method not in ["GET", "POST"]:
        print("✖️ Invalid method selected. Defaulting to GET.")
        http_method = "GET"

    # Call the respective test function based on the user's choice
    if test_type == "XSS":
        run_xss_test(domain, payload_path, http_method)
    elif test_type == "CSRF":
        run_csrf_test(domain, payload_path, http_method)
    elif test_type == "SQL Injection":
        run_sql_injection_test(domain, payload_path, http_method)

    # Save results to a text file
    result_file = f"{domain.replace('https://', '').replace('/', '')}-result.txt"
    with open(result_file, 'w') as file:
        file.write(f"Results of {test_type} testing on {domain}\n")
        file.write("========================================\n")
        # Assuming `test_results` contains the results of the selected test
        for result in test_results:
            file.write(result + "\n")
    
    print(f"✅ Results saved to {result_file}")

# Example test functions for XSS, CSRF, and SQL Injection
def run_xss_test(domain, payload_path, http_method):
    print(f"🔍 Starting XSS Tests on {domain} using {http_method} method...")
    # Simulate the test and result
    test_results = ["🎯 Vulnerability found: https://example.com with payload <script>alert(1)</script>"]
    print("\n".join(test_results))

def run_csrf_test(domain, payload_path, http_method):
    print(f"🔍 Starting CSRF Tests on {domain} using {http_method} method...")
    test_results = ["✖️ No CSRF vulnerability found; URL is safe: https://example.com"]
    print("\n".join(test_results))

def run_sql_injection_test(domain, payload_path, http_method):
    print(f"🔍 Starting SQL Injection Tests on {domain} using {http_method} method...")
    test_results = ["🎯 Possible SQL Injection vulnerability found: https://example.com with payload ' OR '1'='1"]
    print("\n".join(test_results))

# Run the main function
if __name__ == "__main__":
    main()
