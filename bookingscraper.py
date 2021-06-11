#!/usr/bin/env python3
from config import *
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import os
import config
import asyncio
import datetime
import re
import pandas
import xlsxwriter

session = HTMLSession()

LINK_DATE_FORMAT = "%Y-%m-%d"
EXCEL_DATE_FORMAT = "%d/%m"
WORKSHEET_NAME = "RESULTS"
INITAL_DATA_CELL_INDEX = 1 # Offset for date and data. I did not change indexes when putting data, so this offset is needed

jolanta_results = {},
bahnhofs_results = {}
max_item_count = 0 # Days * hotels
fetched_item_count = 0
initial_row_indexes = {} # Indicates for each hotel where to start putting data
colored_day_range = range(5, 7)

time = datetime.datetime.now().strftime("_on_%d-%m_at_%H-%M")
workbook = xlsxwriter.Workbook('results' + str(time) + '.xlsx')
ws = workbook.add_worksheet(WORKSHEET_NAME)

TAKEN_STYLE   = workbook.add_format({
'bg_color': "#4BA8FF",
'text_wrap': True,
'valign': 'center',
'border_color': "#000000",
'border': 1
})

AVAILABLE_STYLE = workbook.add_format({
    'bg_color': "#FFBFC3",
    'text_wrap': True,
    'valign': 'center',
    'border_color': "#000000",
    'border': 1
})

WEEKDAY_STYLE = workbook.add_format({
    'bg_color': "#caffbf",
    'border_color': "#000000",
    'border': 1
})

MERGE_FORMAT_STYLE = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': 'yellow',
    'rotation': 90,
    })

MERGE_FORMAT_STYLE_HORIZONTAL = workbook.add_format({
'bold': 1,
'border': 1,
'align': 'center',
'valign': 'vcenter',
'fg_color': 'yellow',
})

HOTEL_NAMES_STYLE = workbook.add_format({
    'border': 1,
    'align': 'left'
    })

def setup_workbook():
    ws.set_column(0,0,4)
    ws.write(0, 0, "Hotel")
    ws.set_column(1, 1, 20)
    ws.write(0, 1, "Name")
    ws.set_column(2 , 100, 5)
    ws.set_default_row(16)

def write_first_column():
    index = 1
    for hotel_values in hotel_list.values():
        for room in hotel_values.values():
            for count in range(room[1]):
                ws.write_string(index, 1, room[0], HOTEL_NAMES_STYLE)
                index += 1

def print_percentage():
    global fetched_item_count
    global max_item_count
    fetched_item_count += 1
    print(str(int(fetched_item_count / max_item_count * 100)) + "%")

def get_initial_row_indexes():
    key_before = ""
    for hotel in hotel_list:
        if key_before == "":
            initial_row_indexes[hotel] = 1
            count = 0
            for pair in hotel_list[hotel].values():
                count += pair[1]
            first_cell = 2
            second_cell = count+1
            ws.merge_range('A2:A'+str(count+1), hotel, MERGE_FORMAT_STYLE)
        else:
            count = 0
            for pair in hotel_list[key_before].values():
                count += pair[1]
            inital_index = initial_row_indexes[key_before] + count  # +1 at the end because Merge takes index from 1
            initial_row_indexes[hotel] = inital_index

            count = 0
            for pair in hotel_list[hotel].values():
                count += pair[1]
            
            first_cell = initial_row_indexes[hotel] + 1
            second_cell = count + inital_index
            
            if first_cell != second_cell:
                ws.merge_range('A' + str(initial_row_indexes[hotel] + 1)+':A'+str(count + inital_index), hotel, MERGE_FORMAT_STYLE)
            else: 
                ws.write(first_cell - 1, 0, hotel, MERGE_FORMAT_STYLE_HORIZONTAL )


        key_before = hotel    


async def main():
    print("Date format: DD-MM-YY")
    start_date_input = input("Input start date:").split("-")
    end_date_input = input("Input end date:").split("-")
    setup_workbook()
    get_initial_row_indexes()

    # start_date_input = "11-06-21".split("-")
    # end_date_input = "15-06-21".split("-")
    start_date = datetime.datetime(int(start_date_input[2]) + 2000, int(start_date_input[1]), int(start_date_input[0]))
    end_date = datetime.datetime(int(end_date_input[2]) + 2000, int(end_date_input[1]), int(end_date_input[0]))
    tasks = []
    
    write_first_column()

    for hotel in baselinks:
        tasks.append(get_data(hotel, start_date, end_date))
    await asyncio.gather(*tasks, return_exceptions=False)

    workbook.close()

async def get_data(hotel_name, start_date, end_date):
    daterange = pandas.date_range(start_date, end_date)
    global max_item_count
    max_item_count = len(daterange) * len(baselinks)

    #Iterate over date range and get data from current day.
    for index, single_date in enumerate(daterange):
        next_day = single_date + datetime.timedelta(days=1)
        link = baselinks[hotel_name]
        link = re.sub(r'checkin=\d\d\d\d-\d\d-\d\d', "checkin=" + single_date.strftime(LINK_DATE_FORMAT), link)
        link = re.sub(r'checkout=\d\d\d\d-\d\d-\d\d', "checkout=" + next_day.strftime(LINK_DATE_FORMAT), link) # Replace date in link

        column = index + 1
        if single_date.weekday() in colored_day_range:
            ws.write(0, column + INITAL_DATA_CELL_INDEX, single_date.strftime(EXCEL_DATE_FORMAT), WEEKDAY_STYLE)
        else:
            ws.write(0, column + INITAL_DATA_CELL_INDEX, single_date.strftime(EXCEL_DATE_FORMAT))

        await asyncio.gather(get_day_data(link, hotel_name, single_date, column), return_exceptions=False)
        
async def get_day_data(link, hotel_name, date, column):
    page = session.get(link)
    comparison_map = hotel_list[hotel_name]
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_="hprt-table")

    #If Cannt find table - all rooms are booked
    results = {}
    if table is not None:
        tbody = table.find('tbody')
        room_copy = {}
        comparison_room_id = -1
        comparison_room_name = "" # Used to mark previous items to group rooms

        #Go trough all rows of table. 
        for tr in table.find_all('tr', class_="js-rt-block-row"):
            room_id = int(tr.find('select')["data-room-id"])
            price = re.search(r'[0-9]{1,4}', tr.find('span', class_="prco-valign-middle-helper").get_text()).group()
            if room_id != comparison_room_id:
                free_rooms = len(tr.find('select', {"data-room-id":str(room_id)}).find_all('option')) - 1
                comparison_room_name = tr.find('a', class_="hprt-roomtype-link").find('span', class_="hprt-roomtype-icon-link").get_text(strip = True)
                room_copy[room_id] = (comparison_room_name, [ comparison_map.get(room_id, 0)[1] - free_rooms, [price] ])
                comparison_room_id = room_id
            else:
                room_copy[comparison_room_id][1][1].append(price)

        #Create a map which shows how many rooms are not booked from all rooms
        for key in comparison_map.keys():
            if key in room_copy:
                results[key] = (comparison_map[key][0], [comparison_map[key][1] - room_copy[key][1][0], room_copy[key][1][1]])
            else:
                results[key] = (comparison_map[key][0], [0, []])
    else:
        # If table is empty  - mark all rooms booked
        for key in comparison_map.keys():
            results[key] = (comparison_map[key][0], [0, []])

# ('Standarta divvietīgs numurs (1 gulta)', [2, ['55', '85']])
    
    row = initial_row_indexes[hotel_name]
    for room_key in results.keys():
        room = results[room_key]
        available_room_count = room[1][0]

        for count in range(comparison_map[room_key][1]):
            if available_room_count < 1:
                ws.write(row, column + INITAL_DATA_CELL_INDEX, " ", TAKEN_STYLE)
            else:
                ws.write(row, column + INITAL_DATA_CELL_INDEX, str(max(room[1][1])), AVAILABLE_STYLE)
            
            available_room_count -= 1
            row += 1
    print_percentage()

if __name__ == "__main__": 
    asyncio.run(main())
