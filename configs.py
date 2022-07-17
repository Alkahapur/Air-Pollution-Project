import dataset

# should not be changed as of now as it will only extract 0 and 1 index values only
# need to change the string in scraper, if want to add more parameters
PARAMS = {
    'name': ['PM2.5', 'PM10'],
    'value': ['parameter_193', 'parameter_215']
}

# website address
HEADER = 'https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-view-data-report/'
# change this xpath with pdf or word xpath to get pdf or word file instead of xlsx
XPATH = '/html/body/app-root/app-caaqm-dashboard/div[1]/div/main/section/app-caaqm-view-data-report/div[2]/div[1]/div[2]/div/div/a[2]/i'

# get the table from db
DB = dataset.connect('sqlite:///data.sqlite3')

# start and end date  = format(Day, Month, Year)
start_date = '01-01-2015'
end_date = '13-07-2022'

# criteria or interval
# requires changes in string in scraper if wanted to change criteria from hours to minutes or annual average
criteria = 24  # available criteria [1, 4, 8, 24 hours]

# Downloads folder path - changes to your own path
downloads_folder = '/home/laterknight/Downloads/'

STATE = 'Delhi'