from selenium import webdriver


# funkcja zwraca sterownik przegladarki
def get_firefox_driver():
    return webdriver.Firefox(firefox_binary="C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe")


def get_skin_name(full_link):
    """
    Funkcja wycina z linku to, co jest po jego ostatnim ukosniku:
    np: full_link = "http://abc.pl/tekst3" da w rezultacie tekst3
    :param full_link: param
    """
    rev = full_link[::-1]  # odwracamy string  abc -> cba
    for i in range(len(rev)):  # szukamy pozycji ukosnika, ktory teraz bedzie z przodu
        if rev[i] == '/':
            return rev[0:i][::-1]  # wycinamy tekst od poczatku do ukosnika, odwracamy str


def save_download_links(driver, page):
    """
    Funkcja pomocnicza:  z danej podstrony zbiera wszystkie linki, ktore sluza do sciagania
    skorek.
    :param driver: WebDriver
    :param page: strona do przeczesania
    :return:
    """
    # driver = get_firefox_driver()
    driver.get(page)  # wchodzi na podstrone
    links = driver.find_elements_by_xpath("//a")  # wszystkie linki zwraca w liscie

    for next_link in links:  # dla kazdego WebElementu w liscie
        try:
            href = next_link.get_attribute('href')  # wyciagnij wartosc atrybutu href="..."

            if href[-3:] not in ['tml', 'php']:  # jesli w href nie ma html, php - gitara
                if href != 'http://www.allwinampskins.com/':  # jesli nie jest to bazowy link
                    f = open('links.txt', 'a+')  # do pliku z linkami zapisuje plik
                    f.write(href + '\n')  # jeden link - jedna linia, zapewnia to \n
                    f.close()  # zamknij plik
                    # download_links.append()
                    print(href)
        except Exception as e:
            # print(type(e).__name__)  # sprawdzalem typ wyjatku zeby wywalic bledy, niech sobie bedzie w komencie
            continue  # w razie bledu kontynuuj petle


"""
Wlasciwy kod skryptu. Kod TYLKO zapisuje linki do pliku
"""


def all_skin_links_to_disk():
    root_page = 'http://www.allwinampskins.com/winamp_skins.'  # strona bazowa, do niej bedziemy dodawac literke i .html

    driver = get_firefox_driver()  # pobranie sterownika przegladarki

    for next_letter in range(26):  # a,b,c... x,y,z

        """
        Mala literka 'a' ma kod ascii 97. Liter w alfabecie jest 26. Aby otrzymac 'e' do 97 nalezy dodac 4
        alt+101 na numerycznej, daje literke e - sprawdz
        """

        # root_page + mala literka + '.html' daje linka do strony na dana literke
        save_download_links(driver, root_page + chr(97 + next_letter) + '.html')  # linki do skorek do pliku

        tags = driver.find_elements_by_xpath("//a")  # pobierz wszytskie linki

        for next_tag in tags:  # dla kazdego linku w WebElemen
            if 'Next page' in next_tag.text:  # jesli link prowadzi do nastepnej podstrony (1,2,3,4...)
                print('NEXT PAGE AT ' + next_tag.get_attribute('href'))
                save_download_links(root_page + chr(97 + next_letter) + '.html')  # to wejdz do niego i zapisz linki
                break  # po zapisie

# all_skin_links_to_disk()

def download_skins():
    """
    Otwiera plik z linkami do odczytu. Wczytuje wszystkie linki do listy
    Zapisywalem jeden link w jednej linii, wiec sprawa bedzie prosta:
    """

    import urllib.request, os

    links = open('links.txt', 'r').readlines()  # caly plik siedzi w liscie

    print('Len before '+str(len(links)))

    links = list(set(links))  # usuwam powtorzenia

    print('Len after '+str(len(links)))
    input('Enter...')

    if not os.path.isdir('skins'):
        os.mkdir('skins')

    for link in links:  # dla kazdego linku
        link = link.replace('\n', '')
        print('Downloading '+link)
        # print(link)
        urllib.request.urlretrieve(link, 'skins\\' + get_skin_name(link))

        '''response = urllib.request.urlopen(link)
        data = response.read()
        open()'''
download_skins()