from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sys
import csv
import json
import urllib.parse

def extract_links(driver):
    links = []
    for elem in driver.find_elements(By.XPATH, '//div[span[a[contains(@href, "articleNumber")]]]'):
        link = elem.find_elements(By.XPATH, './/span/a')[0].get_attribute('href')
        title = elem.find_elements(By.XPATH, './/span/a/h2')[0].text
        description = elem.find_elements(By.XPATH, './../../div/span')[0].text
        updated = elem.find_elements(By.XPATH, './../../div/div/div/div[4]/div/span')[1].text
        links.append(
            {
                "articleid": link.split("=")[1],
                "link": link,
                "title": title,
                "description": description,
                "updated": updated
            }
        )
    return links

def get_results_count(driver):
    results_str = driver.find_elements(By.XPATH, '//span[contains(text(),"Showing")]')[0].text
    m = re.match(r'.* (\d+) results.*', results_str)
    if m:
        return int(m.group(1))
    return 0

def get_url(driver, url, page_no, start_page):
    url2 = "{0}&pageNo={1}&from={2}".format(url, page_no, start_page)
    print(url2)
    driver.get(url2)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "a"))
    )

def scrape_dynamic_links(url):
    driver = webdriver.Chrome()
    links = []

    page_no = 1
    offset = 0
    
    get_url(driver, url, page_no, offset)
    links += extract_links(driver)
    
    results_count = get_results_count(driver) - 50
    while results_count > 0:
        page_no += 1
        offset += 50
        get_url(driver, url, page_no, offset)
        links += extract_links(driver)
        results_count -= 50

    return links

if len(sys.argv) != 2:
    print("usage: {0} <output file path>".format(sys.argv[0]))
    exit(0)
output_file = sys.argv[1]


pagesize = 50
post_time = "Past Week"  # or "Past Month"
base = "https://support.broadcom.com/web/ecx/search?"
aggregations = [
    {
        "type":"_type",
        "filter":[
            "knowledge_articles_doc"
        ]
    },
    {
        "type":"productname",
        "filter":[
            "VMware NSX",
            "VMware vDefend Firewall",
            "VMware NSX-T Data Center",
            "VMware NSX Networking",
            "VMware NSX Firewall"
        ]
    },
    {
        "type":"post_time",
        "filter":[ post_time ]
    }
]
params = {
    "activeType": "knowledge_articles_doc",
    "language": "en",
    "resultsPerPage": pagesize,
    "pageSize": pagesize,
    "aggregations": json.dumps(aggregations)
}
url = base + urllib.parse.urlencode(params)
links = scrape_dynamic_links(url)

exclution_keywords = [
    "for vSphere",
    "NSX-v",
    "BGP",
    "OSPF",
    "Federation",
    "federated",
    " GM ",
    "Global Manager",
    "Global-Manager",
    "LDAP",
    "VPN",
    "IPSec",
    "Policy API",
    "NAPP",
    "NSX Application Platform",
    "NSX Intelligence",
    "Security Only",
    "NSXe",
    "V2T",
    "Migrate Coordinator",
    "Malware",
    "IDFW",
    "TAS",
    "TKG",
    "Docker",
    "Container",
    "NCP",
    "SDDC-Managed",
    "SDDC-Manager",
    "SDDC Manager",
    "VMware By Broadcom",
    "The purpose of this KB is to provide",
    "vLCM"
]

with open(output_file, 'w', encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(["Article ID", "Link", "Title", "Last Updated", "Judge", "Description"])
    for link in links:
        description = link["description"]
        title = link["title"]

        found = False
        for keyword in exclution_keywords:
            if description.lower().find(keyword.lower()) != -1:
                found = True
                break
        judge = ""
        if found:
            judge = "exclude"

        writer.writerow([link["articleid"], link["link"], title, link["updated"], judge, description])

"""
<div class="su__w-100 su__overflow-hide su__media-body su__word-break custom-overflow-initial">
    <div class="customdata-view">
        <span class="su__viewed-results su__noclicked-title su__text-truncate1 su__text_align">
            <a tabindex="-1" class="su__text-decoration su__text-black su__font-14 su__font-bold" href="https://broadcomcms-software.wolkenservicedesk.com/external/article?articleNumber=311844" target="_blank" rel="noopener">
                <h2 tabindex="0" class="su__text-truncate1 su__my-0 su__font-14 su__line-height-n">NSX NAPP Infra is Degraded</h2>
            </a>
        </span>
        <span title="Knowledge Articles" class="su__ribbon-title su__bg-blue su__font-12 su__font-bold su__px-2 su__rtlmr-1 su__ml-1 su__rtlml-0 su__d-inline-block su__radius-3"> Knowledge Articles</span>
            <div class="su_preview-startblock su__ml-1">
                <div class="su__results-preview">
                    <div class="su__position-relative" data-testid="tooltip">
                        <div data-testid="tooltip-placeholder" class="su__d-flex">
                            <div class="su__preview-block-content su__d-inline-block su__cursor">
                                <div aria-label="Preview" role="button" tabindex="0" class="su__flex-vcenter su__justify-content-end">
                                    <svg width="13.697" height="9.132" viewBox="0 0 13.697 9.132" fill="#00000091">
                                        <path class="a" d="M13.615,8.719A7.627,7.627,0,0,0,6.849,4.5,7.628,7.628,0,0,0,.083,8.719a.769.769,0,0,0,0,.694,7.627,7.627,0,0,0,6.766,4.219,7.628,7.628,0,0,0,6.766-4.219A.769.769,0,0,0,13.615,8.719ZM6.849,12.49a3.424,3.424,0,1,1,3.424-3.424A3.424,3.424,0,0,1,6.849,12.49Zm0-5.707a2.266,2.266,0,0,0-.6.09A1.138,1.138,0,0,1,4.656,8.464,2.278,2.278,0,1,0,6.849,6.783Z" transform="translate(0 -4.5)">
                                        </path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="su__flex-vcenter">
            <div class="su__href-txt su__text-decoration su__color-lgray su__font-12 su__font-italic">
                https://broadcomcms-software.wolkenservicedesk.com/external/article?articleNumber=311844</div>
            </div>
            <span class="su__list-item-desc su__w-100 su__my-1 su__font-regular su__font-12 su__loading-view">
                NSX NAPP Infra is Degraded in the NSX UI,Workaround: Login to the nsx-manager as root and run the below command. Enter password when prompted. 
                curl https://localhost/napp/api/v1/platform/monitor/feature/health -k -u admin Review the output and it will indicate which Pods are down and it may....
            </span>
            <div>
                <div class="su__d-flex su__flex-wrap su__align-content-around su__mt-2 font-12 custom-metadata custom-metadata-width">
                    <div class="su__meta-date su__meta-data su__word-break"><div class="su__d-flex su__flex-wrap custom-metadata">
                        <span class="metaDataKey su__font-bold su__color-blue su__mr-2 su__rtlmr-0 su__rtlml-2 su__font-12"> Article ID <span>:</span></span>
                        <span class="su__color-black su__tags  su__mb-1 su__radius-3 su__mr-1 su__rtlmr-0 su__rtlml-2 su__line-height-n su__font-10">311844</span>
                    </div>
                </div>
                <div class="su__meta-date su__meta-data su__word-break">
                    <div class="su__d-flex su__flex-wrap custom-metadata">
                        <span class="metaDataKey su__font-bold su__color-blue su__mr-2 su__rtlmr-0 su__rtlml-2 su__font-12"> Product <span>:</span></span>
                        <span class="su__color-black su__tags  su__mb-1 su__radius-3 su__mr-1 su__rtlmr-0 su__rtlml-2 su__line-height-n su__font-12 su__color-lgray">VMware vDefend Firewall</span>
                    </div>
                </div>
                <div class="su__meta-date su__meta-data su__word-break">
                    <div class="su__d-flex su__flex-wrap custom-metadata"><span class="metaDataKey su__font-bold su__color-blue su__mr-2 su__rtlmr-0 su__rtlml-2 su__font-12"> Source <span>:</span></span>
                    <span class="su__color-black su__tags  su__mb-1 su__radius-3 su__mr-1 su__rtlmr-0 su__rtlml-2 su__line-height-n su__font-10">Knowledge Base Articles</span>
                </div>
            </div>
            <div class="su__meta-date su__meta-data su__word-break">
                <div class="su__d-flex su__flex-wrap custom-metadata">
                    <span class="metaDataKey su__font-bold su__color-blue su__mr-2 su__rtlmr-0 su__rtlml-2 su__font-12"> Updated Date <span>:</span></span>
                    <span class="su__color-black su__tags  su__mb-1 su__radius-3 su__mr-1 su__rtlmr-0 su__rtlml-2 su__line-height-n su__font-10">11/5/2024 5:01 PM</span>
                </div>
            </div>
        </div>
        <div class="custom-metadata-dropdowns"></div>
    </div>
</div>
"""


