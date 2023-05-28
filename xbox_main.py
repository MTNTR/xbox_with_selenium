from bs4 import BeautifulSoup
import os
import requests
import json


rows = []
here = os.path.dirname(os.path.abspath(__file__))


def get_langs_desc(url):
    langs_dict = {'ru': 'ru-ru', 'de': 'de-de', 'pl': 'pl-pl'}
    descs = {}
    for lang in langs_dict.keys():
        lang_name = f'desc_{lang}'
        parse_link = url.replace('en-us', langs_dict[lang])
        resp = requests.get(parse_link)
        parse = BeautifulSoup(str(resp.text), 'html.parser')
        descrip = parse.find('p', {'class': 'Description-module__description___1ddri typography-module__xdsBody2___1XDyq ExpandableText-module__container___21-cS'}).text
        fin_desc = str(descrip).replace('</p>', '')
        descs[lang_name] = fin_desc

    return descs


def get_game_info(url_en):

    tags = []
    imgs_en = []

    resp_en = requests.get(url_en)
    parse_en = BeautifulSoup(str(resp_en.text), 'html.parser')
    descrip_en = parse_en.find('p', {'class': 'Description-module__description___1ddri typography-module__xdsBody2___1XDyq ExpandableText-module__container___21-cS'}).text
    desc_en = str(descrip_en).replace('</p>', '')
    
    icon_url = parse_en.find('img', {'class': 'ProductDetailsHeader-module__productImage___tT14m'}).attrs['src']
    title = parse_en.find('h1').text

    youtube_id = ''
    imgs_parse_en = parse_en.find_all('div', {'class': 'ItemsSlider-module__itemMargin___11wwp'})
    for div_block in imgs_parse_en[0:4]:
        img = '' 
        try:
            img = div_block.find('img').attrs['src']
        except AttributeError:
            pass
        imgs_en.append(img)
    
    tags_blocks = parse_en.find_all('div', {'class': 'commonStyles-module__basicContainer___ZmTki FeaturesList-module__item___19NYe typography-module__xdsTag3___dtX8u'})
    for tag_block in tags_blocks:
        tag = tag_block.text
        tags.append(tag)
        
    price = parse_en.find('span', {'class': 'Price-module__boldText___34T2w Price-module__moreText___1FNlT'}).text
    year = parse_en.find_all('div', {'class': 'typography-module__xdsBody2___1XDyq'})[-1].text[-4:]
    
    langs_desc = get_langs_desc(url_en)

    game_info = {'price': price, 'icon_url': icon_url, 'youtube_id': youtube_id, 'imgs_en': imgs_en, 'title': title, 'tags': tags,
                 'desc_en': desc_en, 'year': year, 'url': url_en}

    game_info.update(langs_desc)
    return game_info


def get_games_links(url):
    games = []
    resp_en = requests.get(url)                            
    parse_en = BeautifulSoup(str(resp_en.text), 'html.parser')
    games_list = parse_en.find_all('div', {'class': 'm-channel-placement-item'})
    for game in games_list:
        game_short_link = game.find('a').attrs['href'].replace('p/', '').replace('en-us/', '')
        game_full_link = f'https://www.xbox.com/en-us/games/store{game_short_link}'
        games.append(game_full_link)
    return games


def get_all_games_links():
    for i in range(12):
        counter = i*90
        url = f'https://www.microsoft.com/en-us/store/best-rated/games/xbox?s=store&skipitems={counter}'
        games = get_games_links(url)
        with open(os.path.join(here, 'games_links.txt'), 'a') as f:
            for game in games: 
                f.write(str(f'{game}\n'))

    return 


def read_last_id():
    return int(open(os.path.join(here, 'counter.txt')).read().strip())


def main_theme():
    last_id = read_last_id()
    with open(os.path.join(here, 'games_links.txt'), 'r') as f:
        games_links = f.readlines()
    url = games_links[last_id]
    game_info = get_game_info(url)
    last_id += 1
    with open(os.path.join(here, 'counter.txt'), 'w') as count:
        count.write(str(last_id))
    return game_info     


def main_parser():
    last_id = read_last_id()
    n_pages_to_skip = last_id//90
    n_games_to_skip = n_pages_to_skip*90
    urls_block = f'https://www.microsoft.com/en-us/store/best-rated/games/xbox?s=store&skipitems={n_games_to_skip}'
    games_list = get_games_links(urls_block)
    game_id = last_id - n_games_to_skip
    game_link = games_list[game_id]
    game_info = get_game_info(game_link)
    rows.append(game_info)
    game_info_json = str(json.dumps(rows, ensure_ascii=False))
    
    new_id = last_id +1
    with open(os.path.join(here, 'counter.txt'), 'w') as f:                                  
        f.write(str(f'{new_id}'))
    return game_info_json


if __name__ == '__main__':
    print(main_parser())
