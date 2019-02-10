# scrape profiles for a fruit from ndb.nal.usda.gov

import bs4
import requests


def find_fiber(food_name):
    # step a: request ndb website
    food_soup = query_site(food_name)

    # step b: get alert message
    alert = get_alert(food_soup)
    if alert == -1:
        return -1

    # step c: get url with "fruit_name, raw" as a header.
    #         Pick the first url to request.
    index_list = get_url_raw(food_soup)
    if index_list == -2:
        return -2

    url_list = [food_soup.body.find_all('td')[i].
                find('a').attrs['href'] for i in index_list]

    # As stated in the instruction,
    # we only need to request the first url
    query_soup = query_raw_site(url_list[0])

    # step d: open 'fruit, raw' URL, get
    fiber_idx = get_fiber_idx(query_soup)
    if fiber_idx == -3:
        return -3
    elif fiber_idx == -4:
        return -4
    else:
        fiber_idx += 2

    fiber = report_fiber(fiber_idx, query_soup)

    return fiber


# Assist Functions
def query_site(food_name):
    url = """https://ndb.nal.usda.gov/ndb/search/
             list?&qt=&ds=Standard+Reference&qlookup="""
    site = url + food_name

    try:
        wb_data = requests.get(site)
    except requests.exceptions.RequestException as e:
        raise ValueError('page not found')

    soup = bs4.BeautifulSoup(wb_data.text, 'lxml')
    return soup


def query_raw_site(url):
    try:
        query = requests.get("https://ndb.nal.usda.gov" + url)
    except requests.exceptions.RequestException as e:
        raise ValueError('raw page not found')

    query_soup = bs4.BeautifulSoup(query.text, 'lxml')
    return query_soup


def _get_alert(tag):
    return tag.has_attr('class') and "alert" in tag['class']


def get_alert(soup):
    alert = soup.body.find(_get_alert)
    if alert == -1:
        return -1

    alert = alert.get_text(strip=True)
    if alert[0:2] == 'No':
        return -1  # food not found

    return alert


def get_url_raw(soup):
    table_content = soup.body.find_all('td')
    index_list = []

    for i, element in enumerate(table_content):
        content = element.get_text(strip=True)
        if ', raw' in content:
            index_list.append(i)

    if len(index_list) > 0:
        return index_list
    else:
        return -2  # food does not have raw form


def get_fiber_idx(soup):
    try:
        table = soup.find("table", id="nutdata")
    except Exception:
        return -3  # nuttable not found

    if table is None:
        return -3

    table_content = table.find_all('td')
    idx = -1
    for i, element in enumerate(table_content):
        content = element.get_text(strip=True)
        if 'Fiber, total dietary' in content:
            idx = i

    if idx == -1:
        return -4  # fiber not found
    else:
        return idx


def report_fiber(idx, tag):
    table_content = tag.find_all('td')
    text = table_content[idx].get_text(strip=True)

    try:
        fiber = float(text)
        return fiber
    except Exception:
        return None


if __name__ == '__main__':
    fiber = find_fiber("pears")  # 3.1
    fiber2 = find_fiber("kk")  # -1


