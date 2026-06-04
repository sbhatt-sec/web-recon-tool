import requests
import argparse
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def main():
    # Argparse Implementation

    parser = argparse.ArgumentParser(description="Web Recon Tool")
    parser.add_argument('-u', '--url', help="Target URL", required=True)
    parser.add_argument('-o', '--output', help="Save Output to a file")
    args = parser.parse_args()

    url = args.url

    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    
    header = {'User-Agent': 'Mozilla/5.0 (WINDOWS NT 10.0; WIN64; x64)'}

    try:

        print(f"Starting Recon on {url}")
        response = requests.get(url, timeout=5, headers= header)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Status code and server detection
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Server : {response.headers.get('Server', 'Unknown')}")



        # security headers
        security_headers = {
            'CSP': 'Content-Security-Policy',
            'HSTS': 'Strict-Transport-Security',
            'X-Frame-Options': 'X-Frame-Options',
            'X-Content-Type-Options': 'X-Content-Type-Options'
        }

        print(f"\n[+] Security Headers: ")
        for short_name, full_name in security_headers.items():
            if full_name in response.headers:
                print(f" [+] {short_name} Present")
            else:
                print(f" [-]{short_name} Absent")
        

        # parse page title

        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else 'Not Specified'
        print(f"\n[+] Title: {title}")


        #Form Analysis
        forms = soup.find_all('form')
        print(f"[+] Forms Found: {len(forms)} Found")
        for i, form in enumerate(forms, 1):
            method = form.get('method','GET').upper()
            action = form.get('action', 'Unknown')
            print(f" Form #{i}")
            print(f" Method : {method}")
            print(f" Action : {action}")
            print(f"Inputs: ")
            for inp in form.find_all('input'):
                inp_name = inp.get('name')
                inp_type = inp.get('type')
                print(f" -{inp_name}  type: {inp_type}")

        
        # Hidden Inputs

        hidden_input = soup.find_all('input',{'type': 'hidden'})
        if hidden_input:
            print(f"\n[+] Found Hidden Inputs: ")
            for h in hidden_input:
                print(f" -{h.get('name')} : {h.get('value')}")


        #  email checker usig regex
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = set(re.findall(email_pattern, response.text))
        print(f"\n[+] Email Found: {len(emails)}")
        for email in emails:
            print(f" - {email}")


        # Links

        links = soup.find_all('a')
        external_link = []
        internal_link = []

        # get the domain of the target
        target_domain = urlparse(url).netloc 

        for link in links:
            href = link.get('href')
            
            if href:
                # Extract the domain for the link
                href_domain = urlparse(href).netloc
                # if link is empty string ot if it matches the domain name  then it is an internal link
                if href_domain == "" or href_domain == target_domain:
                    internal_link.append(href)
                else:
                    external_link.append(href)
        
        print(f'[+] External Link : {len(external_link)} Found')
        for href in external_link:
            print(f" - {href}")
        print(f'[+] Internal Link : {len(internal_link)} Found') 
        for href in internal_link:
            print(f"[+] - {href}")
        


        # to output the results in a file 

        if args.output:
            with open(args.output, 'w') as f:
                f.write(f"Recon Report for {url}\n")
                f.write(f"Status code : {response.status_code}\n")
                f.write(f"Server : {response.headers.get('Server', 'unknown')}\n")
                f.write(f"Title : {title}\n")
                f.write(f"Email Found : {', '.join(emails) if emails else 'None'}\n")
            print(f"\n[+] Report saved to {args.output}")



    except requests.exceptions.ConnectionError:
        print(f"[!] Could not connect to Target URL...")
    except requests.exceptions.Timeout:
        print(f"[!] Connection Timed Out...")
    except requests.exceptions.RequestException as e:
        print(f"[!] Request Failed: {e}")


if __name__ == "__main__":
    main()



    