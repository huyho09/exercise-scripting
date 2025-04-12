import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
import concurrent.futures
import os
from get_last_char import csv_list
import time  # Import the time module

max_workers = os.cpu_count() * 4

class URLFetcher:
    @staticmethod
    def fetch_global_id_content(url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            element = soup.find('meta', {'name': 'Global-ID'})
            return element['content'] if element and 'content' in element.attrs else 'None'
        except Exception as e:
            print(e)
            return 'None'

    @staticmethod
    def fetch_blog_links(url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return [a['href'] for a in soup.find_all('a', class_='component-blog-teaser') if 'href' in a.attrs]
        except Exception as e:
            print(f"Error fetching blog links from {url}: {e}")
            return [url]

class APIClient:
    @staticmethod
    def call_api(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def extract_urls(data):
        urls = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == 'url':
                    urls.append(value)
                elif isinstance(value, (dict, list)):
                    urls.extend(APIClient.extract_urls(value))
        elif isinstance(data, list):
            for item in data:
                urls.extend(APIClient.extract_urls(item))
        return urls

class CSVExtractor:
    @staticmethod
    def extract_lang():
        return [re.search(r'^(\w+)/', item).group(1) for item in csv_list if re.search(r'^(\w+)/', item)]

    @staticmethod
    def extract_country():
        return [re.search(r'/(\w+)/', item).group(1) for item in csv_list if re.search(r'/(\w+)/', item)]

class URLListCreator:
    @staticmethod
    def create_list_url():
        lang_list = CSVExtractor.extract_lang()
        country_list = CSVExtractor.extract_country()
        return [f'https://dc-mkt-prod.cloud.bosch.tech/v1/dc-ncj-prod/{country}/{lang}/navigations?maxAdditionLevels=3'
                for lang, country in zip(lang_list, country_list)]

    @staticmethod
    def create_list_url_blog():
        lang_list = CSVExtractor.extract_lang()
        country_list = CSVExtractor.extract_country()
        return [f'https://www.boschrexroth.com/{lang}/{country}/blog/'
                for lang, country in zip(lang_list, country_list)]

class GlobalIDFinder:
    def __init__(self, url_list):
        self.url_list = url_list

    def find_all_global_ids(self):
        """
        This method finds the Global-IDs for all URLs generated from the navigation API.
        It uses multithreading to speed up the process of fetching data from multiple URLs concurrently.
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            """
            ThreadPoolExecutor is used here to manage a pool of threads.
            It allows us to execute multiple API calls concurrently, which can significantly reduce the overall execution time,
            especially when dealing with a large number of URLs. The 'with' statement ensures that all threads in the pool
            are properly shut down after the tasks are completed.
            """
            json_futures = {executor.submit(APIClient.call_api, url) for url in self.url_list}
            json_results = [future.result() for future in concurrent.futures.as_completed(json_futures)]

        url_in_json = [APIClient.extract_urls(json_result) for json_result in json_results]

        time_start = time.time()  # Record start time
        with open('Output.CSV', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Global-ID'])
            """
            Another ThreadPoolExecutor is used here to fetch the Global-ID content from the URLs extracted from the API responses.
            This again leverages multithreading to fetch content from multiple web pages simultaneously.
            'max_workers' determines the maximum number of threads that can be created.
            """
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures_to_url = {executor.submit(URLFetcher.fetch_global_id_content, url): url for sublist in url_in_json for url in sublist}
                for future in concurrent.futures.as_completed(futures_to_url):
                    url = str(futures_to_url[future])
                    try:
                        result = future.result()
                        writer.writerow([url, result])
                        print(f'the URL is : {url} - the global-id is : {result}')
                    except Exception as e:
                        writer.writerow([url, 'None'])
                        print(f'the URL is : {url} - the global-id is : None')

        time_end = time.time()  # Record end time
        execution_time = time_end - time_start
        execution_time_minutes = execution_time / 60
        print(f"Execution time for find_all_global_ids: {execution_time_minutes:.2f} minutes")

class BlogGlobalIDFinder:
    def __init__(self, url_list):
        self.url_list = url_list

    def find_blog_global_ids(self):
        """
        This method finds the Global-IDs for all blog URLs.
        It also utilizes multithreading to efficiently fetch data.
        """
        link_list = [URLFetcher.fetch_blog_links(url) for url in self.url_list]

        time_start = time.time()  # Record start time
        with open('Output_blog.CSV', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Global-ID'])
            """
            A ThreadPoolExecutor is employed here to fetch the Global-ID content from the extracted blog links.
            This allows for concurrent fetching of Global-IDs from multiple blog pages, improving performance.
            """
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures_to_url = {executor.submit(URLFetcher.fetch_global_id_content, url): url for sublist in link_list for url in sublist}
                for future in concurrent.futures.as_completed(futures_to_url):
                    url = str(futures_to_url[future])
                    try:
                        result = future.result()
                        writer.writerow([url, result])
                        print(f'the URL is : {url} - the global-id is : {result}')
                    except Exception as e:
                        writer.writerow([url, 'None'])
                        print(f'the URL is : {url} - the global-id is : None')

        time_end = time.time()  # Record end time
        execution_time = time_end - time_start
        execution_time_minutes = execution_time / 60
        print(f"Execution time for find_blog_global_ids: {execution_time_minutes:.2f} minutes")

def main():
    start_time = time.time() # Record the start time of the entire script

    url_list = URLListCreator.create_list_url()
    global_id_finder = GlobalIDFinder(url_list)
    global_id_finder.find_all_global_ids()

    url_list_blog = URLListCreator.create_list_url_blog()
    blog_global_id_finder = BlogGlobalIDFinder(url_list_blog)
    blog_global_id_finder.find_blog_global_ids()

    end_time = time.time() # Record the end time of the entire script
    total_execution_time = end_time - start_time
    total_execution_time_minutes = total_execution_time / 60
    print(f"Total execution time for the script: {total_execution_time_minutes:.2f} minutes")

if __name__ == '__main__':
    main()