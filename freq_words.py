import requests
from bs4 import BeautifulSoup
import requests
from bs4.element import Comment
import urllib.request
import nltk
from operator import itemgetter
from urllib.request import Request, urlopen


# Sets the page to crawl
MAIN_LINK = "https://www.cornell.edu/"
MAIN_LINK_DOMAIN = "cornell."

crawled = []


#retreives visible text from the webpage
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def visible_text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def return_visible_text(link):

    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()

    return (visible_text_from_html(html))

"""Given a url, returns page's htmltext
Parameters: <link> is a valid web links
Output: String of page's html
"""
def page_html(link):
    url = requests.get(link)
    htmltext = url.text
    return htmltext

def new_links_on_main(link):
    url = link
    # Getting the webpage, creating a Response object.
    response = requests.get(url)

    # Extracting the source code of the page.
    data = response.text

    # Passing the source code to BeautifulSoup to create a BeautifulSoup object for it.
    soup = BeautifulSoup(data,  "html.parser")

    # Extracting all the <a> tags into a list.
    tags = soup.find_all('a')

    # Extracting URLs from the attribute href in the <a> tags.
    links = {}
    for tag in tags:
        link = tag.get('href')
        if link != None and len(link) > 0:
            if len(link) > 1:
                if link[0] == "/" and link[1] == "/":
                    continue
            if link[0] == "/":
                link = MAIN_LINK + link
            if link[-1] == "/":
                link = link[0:-1]
            if link not in links:
                links[link] = 1
            else:
                links[link] = links[link] + 1
    return links

#Cleans out undesirable links
def clean_links(list):
    links = {}
    not_links = {}
    for items in list:
        if items.find(".css") != -1 or items.find(".php") != -1 or items.find(".ico") != -1 or items[0] == "#" or items.find(".xml") != -1 or items.find(".png") != -1 or items.find(".js") != -1 or items.find(".jpg") != -1 or items.find(".pdf") != -1:
            not_links[items] = list[items]
        else:
            links[items] = list[items]
    return(links)

#Cleans out social media links
def org_links(list):
    nonsocial_media = {}
    social_media = {}
    for items in list:
        if items.find("http://www.twitter.com/") != -1 or items.find("http://twitter.com/") != -1:
            social_media[items] = list[items]
        if items.find("mailto:") != -1:
            social_media[items] = list[items]
        else:
            nonsocial_media[items] = list[items]
    return(nonsocial_media)

#seperates links from within the domain vs. outside
def in_domain(list):
    domain = {}
    ood = {}
    for items in list:
        if items.find(MAIN_LINK_DOMAIN) != -1 or items[0] == "/":
            domain[items] = list[items]
        else:
            ood[items] = list[items]
    return(domain)

#Finds unique words and the number of times used within a list of links
def get_tokens(links):
    word_count = {}
    for item in links:
        try:
            urlopen(item)
        except:
            pass
        html = return_visible_text(item)
        tokens = nltk.word_tokenize(html)
        for token in tokens:
            token = token.lower()
            if token not in word_count:
                word_count[token] = 1
            else:
                word_count[token] = word_count[token] + 1
    new = sorted(word_count.items(), key=itemgetter(1), reverse=True)
    print(new)

#every link on the page
master_list = new_links_on_main(MAIN_LINK)

#separated link lists
list_clean = clean_links(master_list)
list_org = org_links(list_clean)
list_indomain = in_domain(list_org)



get_tokens([MAIN_LINK])
