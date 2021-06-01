#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests, os, time

topGGURL = "https://top.gg/servers"
TopServersURL = "https://top.gg/servers/list/top?sort=members"

class Downloader:
    mode = ""
    url = ""
    urls = []
    emojiURLList = []
    def PrintMenu(self):
        print("Welcome in Discord Emojis Downloader 1.0")
        print("1. Download from a specific server")
        print("2. Download all emoji's from the first 300 pages")
        print("3. Generate random URL and download every emoji's from every generated URL's")
        while True:
            choice = input("Choose an option : ")
            if choice == "1":
                print("[+] Option Choosen : Specific")
                return "Specific"
            elif choice == "2":
                print("[+] Option Choosen : Randomized")
                return "Randomized"
            else:
                print("[-] Invalid Option !")
    def GetURL(self):
        #Ask for URL or Top.gg Server ID
        self.url = input("[+] Enter URL or Top.gg Server ID : ")
        #Check if url containt http or is just a number
        if not "http" in self.url:
            t = self.url
            self.url = topGGURL + '/' + t
            print(f"[+] Downloading Images From : {self.url}")
        else:
            print(f"[+] Downloading Images From : {self.url}")
    def GetURLs(self):
        print("[+] Getting all the 300 pages of the Top Servers IDs...")
        print("[+] This might take a little time please be patient")
        iterator = 1
        while iterator <= 300:
            try:
                CuRL = "https://top.gg/servers/list/top?sort=members&page=" + str(iterator)
                re = requests.get(CuRL)
                soup = BeautifulSoup(re.content, 'html.parser')
                ServerDivs = soup.find_all('div', class_='top is-flex')
                for i in ServerDivs:
                    CServerIDa = i.find_all('a', class_='btn-like btn')
                    try:
                        #ServerIDURL = CServerIDa[0]['href'].split('/')[2]
                        print(f"[+] Adding {topGGURL + '/' + CServerIDa[0]['href'].split('/')[2]}")
                        self.urls.append(topGGURL + "/" + CServerIDa[0]['href'].split('/')[2])
                    except IndexError:
                        #print("[+] Server ID not found continuing...");
                        continue
                iterator+=1
            except KeyboardInterrupt:
                print("[+] CTRL + C Detected, Stopping DiscordID Parser")
                break
    def ParseImageList(self, url):
        re = requests.get(url)
        soup = BeautifulSoup(re.content, 'html.parser')
        imgList = soup.find_all('img', class_='emote')
        for i in imgList:
            self.emojiURLList.append(i['src'])
    def ParseImages(self, url):
        print(f"[+] Parsing images from : {url}")
        #make request to url
        re = requests.get(url)
        #get all img tag
        soup = BeautifulSoup(re.content, 'html.parser')
        #print(soup.prettify())
        imgList = soup.find_all('img', class_='emote')
        for i in imgList:
            self.emojiURLList.append(i['src'])
    def DownloadImages(self, url):
        try:
            os.mkdir("./emojis")
        except FileExistsError:
           print() 
        for i in self.emojiURLList:
            re = requests.get(i)
            #print(re.content)
            with open("./emojis/" + i.split('/')[-1], "wb") as file:
                file.write(re.content)
                file.close()
            print(f"[+] New image downloaded : {i.split('/')[-1]}")

def main():
    try:
        StartDownload = Downloader()
        StartDownload.mode = StartDownload.PrintMenu()
        if StartDownload.mode == "Specific":
            #Call Get URL
            StartDownload.GetURL()
            StartDownload.ParseImages(StartDownload.url)
            StartDownload.DownloadImages(StartDownload.url)
        elif StartDownload.mode == "Randomized":
            #Call Generate RandomURLs
            StartDownload.GetURLs()
            for i in StartDownload.urls:
                print(f"[+] Parsing Images from : {i}")
                StartDownload.ParseImageList(i)
            StartDownload.DownloadImages(i)
    except KeyboardInterrupt:
        print("\n[+] CTRL + C Detected...")
        print("[!] Ending program !")
main()
