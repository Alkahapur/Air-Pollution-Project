import os # path handling
import time
import shutil # to move/copy files

# selenium imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from configs import * # import everything from config file


def file_exists(state:str, city:str, station_name:str) -> bool:
    '''
    check if the required file exists in the system return Boolena value
    '''
    dir_ = os.path.join(os.getcwd(), 'media', state, city, station_name)
    file = f'{start_date}_{end_date}.xlsx'
    dir_ = os.path.join(dir_, file)
    if os.path.exists(dir_):
        print(f"File Already Exists! {dir_} - Skipping.")
        return True
    else:
        return False


def dir_handling(state:str, city:str, station_name:str) -> str:
    # creates tree: media/state/city/station_name/file
    dir_ = os.path.join(os.getcwd(), 'media', state, city, station_name)
    if not os.path.exists(dir_):
        os.makedirs(dir_)
    return dir_


def file_handling(state:str, city:str, station_name:str) -> None:

    '''
    check the downloads folder for the downloaded file and moves to the current tree
    '''

    orig_file = []
    while len(orig_file) == 0:
        # cpcbccr follows a naming convention that every file it downloads starts with site_
        orig_file = [x for x in os.listdir(downloads_folder) if x.startswith('site_')]
        if len(orig_file) == 0:
            print('waiting for file to download.')
            # wait for five seconds if the file has not been downloaded yet
            time.sleep(5)

    old_dir = os.path.join(downloads_folder + orig_file[0])

    # creates tree State, cities, stations, downloaded files
    dir_ = dir_handling(state, city, station_name)

    # new_file name
    new_dir = os.path.join(dir_, f'{start_date}_{end_date}.xlsx')

    print(old_dir, new_dir)

    # move file to the media folder
    shutil.move(old_dir, new_dir)


def func(caching=True):
    '''
    set caching to True if don't want to re-download the file
    '''

    for i, item in enumerate(STATIONS_LIST):
        # enumerate over stations list
        if STATE == '':
            pass
        elif item['state'] != STATE:
            continue

        start_time = time.time()

        # Download those stations that were available in the db
        state, city, station, station_name = item['state'], item['city'], item['site'], item['site_name']
        station_name = station_name.split(', ')[0].replace(' ', '_').replace('-', '_')
        
        if caching and file_exists(state, city, station_name):
            # if caching set is set to True and the file does exists skip this iteration
            continue
        
        # https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/data
        # this url was used to extract data. either we can fill the form using selenium or create a dynamic url string to pass our own params
        string = f"%2522%257B%255C%2522parameter_list%255C%2522%253A%255B%257B%255C%2522id%255C%2522%253A0%252C%255C%2522itemName%255C%2522%253A%255C%2522{PARAMS['name'][0]}%255C%2522%252C%255C%2522itemValue%255C%2522%253A%255C%2522{PARAMS['value'][0]}%255C%2522%257D%252C%257B%255C%2522id%255C%2522%253A1%252C%255C%2522itemName%255C%2522%253A%255C%2522{PARAMS['name'][1]}%255C%2522%252C%255C%2522itemValue%255C%2522%253A%255C%2522{PARAMS['value'][1]}%255C%2522%257D%252C%257B%255C%2522id%255C%2522%253A2%252C%255C%2522itemName%255C%2522%253A%255C%2522{PARAMS['name'][2]}%255C%2522%252C%255C%2522itemValue%255C%2522%253A%255C%2522{PARAMS['value'][2]}%255C%2522%257D%252C%257B%255C%2522id%255C%2522%253A3%252C%255C%2522itemName%255C%2522%253A%255C%2522{PARAMS['name'][3]}%255C%2522%252C%255C%2522itemValue%255C%2522%253A%255C%2522{PARAMS['value'][3]}%255C%2522%257D%252C%257B%255C%2522id%255C%2522%253A4%252C%255C%2522itemName%255C%2522%253A%255C%2522{PARAMS['name'][4]}%255C%2522%252C%255C%2522itemValue%255C%2522%253A%255C%2522{PARAMS['value'][4]}%255C%2522%257D%252C%257B%255C%2522id%255C%2522%253A5%252C%255C%2522itemName%255C%2522%253A%255C%2522{PARAMS['name'][5]}%255C%2522%252C%255C%2522itemValue%255C%2522%253A%255C%2522{PARAMS['value'][5]}%255C%2522%257D%255D%252C%255C%2522criteria%255C%2522%253A%255C%2522{criteria}%2520Hours%255C%2522%252C%255C%2522reportFormat%255C%2522%253A%255C%2522Tabular%255C%2522%252C%255C%2522fromDate%255C%2522%253A%255C%2522{start_date}%2520T00%253A00%253A00Z%255C%2522%252C%255C%2522toDate%255C%2522%253A%255C%2522{end_date}%2520T09%253A46%253A59Z%255C%2522%252C%255C%2522state%255C%2522%253A%255C%2522{state.strip().replace(' ', '%2520')}%255C%2522%252C%255C%2522city%255C%2522%253A%255C%2522{city.strip().replace(' ', '%2520')}%255C%2522%252C%255C%2522station%255C%2522%253A%255C%2522{station}%255C%2522%252C%255C%2522parameter%255C%2522%253A%255B%255C%2522{PARAMS['value'][0]}%255C%2522%252C%255C%2522{PARAMS['value'][1]}%255C%2522%252C%255C%2522{PARAMS['value'][2]}%255C%2522%252C%255C%2522{PARAMS['value'][3]}%255C%2522%252C%255C%2522{PARAMS['value'][4]}%255C%2522%252C%255C%2522{PARAMS['value'][5]}%255C%2522%255D%252C%255C%2522parameterNames%255C%2522%253A%255B%255C%2522{PARAMS['name'][0]}%255C%2522%252C%255C%2522{PARAMS['name'][1]}%255C%2522%252C%255C%2522{PARAMS['name'][2]}%255C%2522%252C%255C%2522{PARAMS['name'][3]}%255C%2522%252C%255C%2522{PARAMS['name'][4]}%255C%2522%252C%255C%2522{PARAMS['name'][5]}%255C%2522%255D%257D%2522"
        query = HEADER + string

        print(f'Downloading Data for - {state}, {city}, {station}, {station_name} from-{start_date}, to-{end_date}')
        print(f'{i} out of {len(STATIONS_LIST)}')
        
        # Download using selenium
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.maximize_window()
        driver.get(query)

        # checking https certification of the website
        # uncomment if the website's certificate is not renewed
        # try:
        #     # click the chrome advanced button
        #     ele = driver.find_element(by=By.ID, value='details-button')
        #     ele.click()
        #     # click the proceed to unsafe website link
        #     ele = driver.find_element(by=By.ID, value='proceed-link')
        #     ele.click()
        # except NoSuchElementException:
        #     pass

        # find the Excel button and download the image
        # wait until the page is fully loaded
        # webdriver wait time can be increased if it takes more time to load
        try:
            WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, XPATH)))
        except TimeoutException:
            print('Website took too much time to respond, Please try again later.')
            return
        except NoSuchElementException:
            print('Desired element not found!')
            return

        driver.find_element(by=By.XPATH, value=XPATH).click()

        # move the downloaded file from Downloads folder and paste in the current directory's tree
        file_handling(state, city, station_name)
        end_time = time.time()
        print(f'Took {end_time - start_time} seconds to download the file \n')
        driver.quit()


if __name__ == '__main__':
    func(True)
