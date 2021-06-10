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

jolanta_results = {},
bahnhofs_results = {}
max_item_count = 0
fetched_item_count = 0

workbook = xlsxwriter.Workbook('results.xlsx')
taken   = workbook.add_format({
    'bg_color': "#4BA8FF",
    'text_wrap': True,
    'valign': 'center',
    'border_color': "#000000",
    'border': 1
})
available = workbook.add_format({
    'bg_color': "#FFBFC3",
    'text_wrap': True,
    'valign': 'center',
    'border_color': "#000000",
    'border': 1
})
weekday = workbook.add_format({
    'bg_color': "#caffbf",
    'border_color': "#000000",
    'border': 1
})

async def main():
    print("Date format: DD-MM-YYYY")
    start_date_input = input("Input start date:").split("-")
    end_date_input = input("Input end date:").split("-")
    start_date = datetime.datetime(int(start_date_input[2]), int(start_date_input[1]), int(start_date_input[0]))
    end_date = datetime.datetime(int(end_date_input[2]), int(end_date_input[1]), int(end_date_input[0]))
    tasks = []
    for hotel in baselinks:
        write_first_column(hotel)
        tasks.append(get_data(hotel,start_date, end_date))
    await asyncio.gather(*tasks, return_exceptions=False)

    workbook.close()

def write_first_column(hotel):
    ws = workbook.add_worksheet(hotel)
    ws.set_column(0, 0, 46)
    ws.set_column(1 , 100, 25)
    ws.set_default_row(25)
    index = 0
    for room_pair in hotel_list[hotel].values():
        for count in range(room_pair[1]):
            ws.write_string(index + 1, 0, room_pair[0])
            index += 1

def print_percentage():
    global fetched_item_count
    global max_item_count
    fetched_item_count += 1
    print(str(int(fetched_item_count / max_item_count * 100)) + "%")  

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
        await asyncio.gather(get_day_data(link, hotel_name, single_date, index+1), return_exceptions=False)
        
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
    ws = workbook.get_worksheet_by_name(hotel_name)

    if date.weekday() in range(4, 7):
        ws.write(0, column, date.strftime(LINK_DATE_FORMAT), weekday)
    else:
        ws.write(0, column, date.strftime(LINK_DATE_FORMAT))
    
    row = 1
    for room_key in results.keys():
        room = results[room_key]
        available_room_count = room[1][0]

        for count in range(comparison_map[room_key][1]):
            price_string = ""
            for price in room[1][1]:
                price_string += str(price) + "€/ "

            if available_room_count < 1:
                ws.write(row, column, "", taken)
            else:
                ws.write(row, column, price_string, available)
            
            available_room_count -= 1
            row += 1
    print_percentage()

if __name__ == "__main__": 
    asyncio.run(main())
