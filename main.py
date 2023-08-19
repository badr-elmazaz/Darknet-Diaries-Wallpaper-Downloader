import requests
from bs4 import BeautifulSoup
import sys
from lxml import etree
from pathlib import Path
import os


URL = "https://darknetdiaries.com"
SAVE_PATH = "wallpapers"



def save_image(url: str, file_name: str):
    path = os.path.join(SAVE_PATH, file_name)
    Path(path).resolve().parent.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
    except Exception as e:
        print(e)
        print("Error: " + str(sys.exc_info()[0]))
        sys.exit(1)


def extract_wallpaper_link(html: str):
    soup = BeautifulSoup(html, "html.parser")
    wallpaper_link = soup.find("meta", property="og:image").get("content")
    return wallpaper_link

def get_html(url: str):
    try:
        r = requests.get(url)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print("Error: " + str(sys.exc_info()[0]))
        sys.exit(1)

def get_latest_episode_number() -> int:
    html = get_html(URL+"/episode")
    dom = etree.HTML (html)
    latest_episode = dom.xpath('/html/body/div[3]/div/section[2]/div/article[1]/div[2]/div/h2/a')[0].get('href').split('/')[2]
    return int(latest_episode)

def get_latest_episode_wallpaper_downloaded() -> int:
    episodes = os.listdir(SAVE_PATH)
    episodes = [int(episode.split('.')[0]) for episode in episodes]
    return max(episodes)


def main():
    latest_episode_number = get_latest_episode_number()
    latest_episode_wallpaper_downloaded = get_latest_episode_wallpaper_downloaded()
    for episode_number in range(latest_episode_wallpaper_downloaded + 1, latest_episode_number + 1):
        print(f"Downloaded wallpaper for episode {episode_number}...", end="\r")
        url = URL + f"/episode/{episode_number}/"
        html = get_html(url)
        wallpaper_link = extract_wallpaper_link(html)
        wallpaper_extension = wallpaper_link.split('.')[-1]
        save_image(wallpaper_link, f"{episode_number}.{wallpaper_extension}")
        print(f"Wallpaper downloaded for episode {episode_number}", end="\r")
        
    
    

if __name__ == "__main__":
    main()
    print()
    print("Done!")