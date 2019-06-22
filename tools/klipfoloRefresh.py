import os, json, argparse
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

profile = dict()  

# This was adapted from an earlier crawling project
# some remnants still need to be cleaned up

class KlipfolioCrawler(object):
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless")
        self.driver = webdriver.Firefox(executable_path='/home/ubuntu/geckodriver', 
                                        firefox_options=options)
        self.baseURL = "https://app.klipfolio.com"
        self.authURL = self.baseURL + '/login/'

    def login(self, authentication):
        driver = self.driver
        with open(authentication,"r") as f:
            data = f.read()
            auth_dict = json.loads(data)
            if(auth_dict['username'] == "" or auth_dict['password'] == ""):
                print("Please enter your Klipfolio credentials in 'auth.json' file")
            else:
                my_username =  auth_dict['username']
                my_password = auth_dict['password']

        driver.get(self.authURL)
        sleep(5)

        inp_username = driver.find_element(By.NAME, "username")
        inp_password = driver.find_element(By.NAME, "password")

        inp_username.send_keys(my_username)
        inp_password.send_keys(my_password)

        driver.find_element(By.NAME, "LOGIN").click()
        sleep(5)

    def get_post_urls(self, query, post_count):
        post_urls = list()
        driver = self.driver
        scroll_downs = int(int(post_count)/12+1)
        
        for i in range(scroll_downs):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(5)
            eles = driver.find_elements(By.CSS_SELECTOR, '.v1Nh3 a')
            for ele in eles:
                post = ele.get_attribute('href')
                if post not in post_urls:
                    post_urls.append(post)

        return post_urls                    
            
    def load_data(self, directory):
        data = json.dumps(profile)
        with open(os.path.join(directory, "profile.json"), "w") as f:
            f.write(data)

    def crawl(self, authentication, query, crawl_type, number, profile_status, directory):
        driver = self.driver
        self.login(authentication)
        print('Logged in successfully...')
        profile_url = self.baseURL + "/" + query
        driver.get(profile_url)
        print('Viewed page... refreshing data source.')
        ds_name = 'e-ds_refresh'
        driver.find_element(By.NAME, ds_name).click()
        print('Refreshed! Exiting now.')

def main():
    parser = argparse.ArgumentParser(description='Klipfolio Refresh')
    # Refresh Dashboard
    parser.add_argument('-q', '--query', type=str,
            default='datasources/view/<datasource_ID_number>',help="Page to visit")
    parser.add_argument('-a', '--authentication', type=str, default='./auth.json', help='Path to authentication json file')
    parser.add_argument('-l', '--headless', action='store_true', help='If set, script will be run headless')
    args = parser.parse_args()
    
    crawler = KlipfolioCrawler(headless=args.headless)
    
    crawler.crawl(authentication=args.authentication, 
                      query=args.query,
                      crawl_type=args.crawl_type,
                      number=args.number,
                      profile_status=args.profile_status,
                      directory=args.directory)

if __name__ == "__main__":
    main()
