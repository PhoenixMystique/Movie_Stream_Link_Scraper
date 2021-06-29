import json
from timeout import timeout
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

browser = webdriver.Chrome('Drivers/chromedriver')
BaseLink = "https://mp4moviez.click"
browser.set_page_load_timeout(10)

file = open("bugs.txt", "a+")
file.close()
c = 1
PageCheck = True
Strings = ""
Reload = 1
Reload1 = 1
Reload2 = 1
Numbers = 1
Retries_Times = 0
MoviesData = {}
Gener = ""
initialdir = ["bollywood-movies.html", "hollywood-hindi-movies.html"
    , "hollywood-hindi-dubbed-tv-series.html", "hollywood-tv-shows-and-series.html",
              "south-indian-hindi-dubbed-movies.html", "hollywood-english-movies.html", "ott-platform-movies.html"]

@timeout(20)
def lastStep(linkset2, Gener, temp):
    global Reload2, Strings, Numbers
    check = True

    Name = temp.replace(" ", "-")
    try:
        browser.get(linkset2)
    except TimeoutException:
        if Reload2 < Retries_Times:
            Reload2 += 1
            return Moviefolderfetcher(Gener, linkset2)
        else:
            browser.execute_script("window.stop();")
            Reload2 = 0
    try:
        Soup = BeautifulSoup(browser.page_source, "html5lib")
        last_data = Soup.findAll("div", "mast")
        count = 0
        tempArray = []
        for data7 in last_data:
            count += 1
            if Name.lower() and (".mp4" or ".mkv" or ".avi") in str(data7.find('a')["href"]).lower():
                tempArray.append(data7.find('a')["href"])
                check = False
            if count == len(last_data) and check == False:
                saver(temp, tempArray, temp[0])

        if check:
            for data in last_data:
                if Name.lower() in str(data.find('a')["href"]).lower():
                    lastStep(BaseLink + data.find('a')["href"], Gener, temp)
                    check = True
    except Exception as e:
        print("lastStep" + str(e))


def Moviefolderfetcher(Gener, linkset):
    global Reload1, Strings, Numbers
    Name = ""
    try:
        browser.get(linkset)
    except TimeoutException:
        if Reload1 < Retries_Times:
            Reload1 += 1
            print("Retrying" + str(Reload1))
            return Moviefolderfetcher(Gener, linkset)
        else:
            browser.execute_script("window.stop();")
            Reload1 = 0
    try:
        Soup = BeautifulSoup(browser.page_source, "html5lib")
        Step2_data = Soup.findAll("a")
        for atags in Step2_data:
            if Gener not in atags["href"]:
                temp = atags.get_text().strip()
                if "20" in temp:
                    Name = temp.split("20")[0]
                elif "19" in temp:
                    Name = temp.split("19")[0]

                if ".html" in atags["href"]:
                    if "20" or "19" in atags["href"]:
                        if "http" not in atags["href"]:
                           print(atags["href"])
                           try:
                             lastStep(BaseLink + atags["href"], Gener, Name)
                           except:
                               continue
    except Exception as e:
        print("folderFetcher" + str(e))


def DataFetcher(link):
    global Reload, c, Gener

    try:
        browser.get(link)

    except Exception:
        if Reload < Retries_Times:
            return DataFetcher(link)
            Reload += 1
        else:
            browser.execute_script("window.stop();")
            Reload = 0
    Soup = BeautifulSoup(browser.page_source, "html5lib")
    c = 1
    commingdata = Soup.findAll("a")

    for atags in commingdata:
        for needtags in initialdir:
            if needtags in atags["href"]:
                if "http" in atags["href"]:
                    Gener = needtags.replace(".html", "")
                    MoviesData["Movies_Data"] = []
                    for i in range(4):
                        if i == 0:
                            continue
                        else:
                            Moviefolderfetcher(Gener, atags["href"] + "&p=" + str(i))
                    with open("Movie_Api_2/" + Gener + ".json", "a") as json_file:
                        json.dump(MoviesData, json_file)
                        print("Dumped")
                    MoviesData.clear()


def saver(Name, videos, starting_Name):
    try:
        temp_Name = Name.replace(" ", "_")

        if "(" in temp_Name:
            temp2=temp_Name[:(temp_Name.find("("))]
            temp_Name =temp2
        if temp_Name[len(temp_Name) - 1] == "_":
             temp1 = temp_Name[:(len(temp_Name) - 1)]
             temp_Name =temp1

        temp = {
            "Movie_Name": temp_Name,
            "Server": videos,
            "Start_Name": starting_Name.lower()
        }
        print(temp)
        MoviesData["Movies_Data"].append(temp)
    except Exception as e:
        print("Problem at Data Saver @" + str(e))


DataFetcher(BaseLink)
