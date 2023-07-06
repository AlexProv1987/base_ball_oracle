import requests
from parsel import Selector
class WebScraper(): 
    '''
    Class Purpose:
    Generic web scraper

    properties:
    base_url - the base url having the request made to it
    link_url_base - handles appending the baseurl to redirect properly using url?
    time_out - how long to wait for the reply
    params - dictionary of url parameters to append to the base url
    node_dict - dictionary of the name(key) and xpath (values) to loop over to get information required
                the product dict that is returned will use the name(key) of the node_dict as its key 
                for the value found via the xpath
    
    Methods:

    scrape_first_item -> grab the first node values for the node_dict specified
    scrape_by_keyword -> grab the first node values that matches the keyword specified
    scrape_all -> return all items for nodes specified, optional keyword to filter volume returned
    
    '''
    def __init__(self, base_url:str, link_url_base:str, timeout:int, params:dict, node_dict:dict) -> None:
        self.headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        self.nodes = node_dict  
        self.params = params
        self.base_url = base_url
        self.link_base = link_url_base
        self.timeout = timeout
        self.product_dict = {}
    def send_request(self):
        html = requests.get(
            self.base_url, params=self.params, headers=self.headers, timeout=self.timeout
        )
        return html.text
    
    '''Grab the first item and return the requested node values'''
    def scrape_first_item(self) -> dict:
        response = Selector(self.send_request())
        for node,xpath in self.nodes.items():
            if '@href' in xpath:
                if self.base_url is None:
                    self.product_dict[node] = response.xpath(xpath).get()
                else:
                    self.product_dict[node] = f'{self.link_base}{response.xpath(xpath).get()}'
            else:
                self.product_dict[node] = response.xpath(xpath).get()
        return self.product_dict

    '''Loop over the nodes until we find one satisfying the keyword arg'''
    def scrape_by_keyword(self,keyword):
        pass

    '''return a full dictionary foreach item, accepts keyword to further filter'''
    def scrape_all(self, keyword):
        if keyword is None:
            pass
        else:
            pass