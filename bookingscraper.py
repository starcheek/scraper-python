#!/usr/bin/env python3
from config import hotel_list, baselinks
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
start_date = datetime.datetime(2021, 6, 10)
end_date = datetime.datetime(2021, 6, 11)
workbook = xlsxwriter.Workbook('results.xlsx')



async def main():
   # print("Date format: DD-MM-YYYY")
    # start_date_input = input("Input start date:").split("-")
    # end_date_input = input("Input end date:").split("-")
    # start_date = datetime.datetime(int(start_date_input[2]), int(start_date_input[1]), int(start_date_input[0]))
    # end_date = datetime.datetime(int(end_date_input[2]), int(end_date_input[1]), int(end_date_input[0]))
    tasks = []
    for hotel in baselinks:
        write_first_column(hotel)
        tasks.append(get_data(hotel,start_date, end_date))
    await asyncio.gather(*tasks, return_exceptions=False)

    workbook.close()


def write_first_column(hotel):
    ws = workbook.add_worksheet(hotel)
    ws.set_column(0, 0, 46)
    for index, room_pair in enumerate(hotel_list[hotel].values()):
        ws.write_string(index, 0, room_pair[0])

async def get_data(hotel_name, start_date, end_date):
    daterange = pandas.date_range(start_date, end_date)
    
    for single_date in daterange:
        next_day = single_date + datetime.timedelta(days=1)
        link = baselinks[hotel_name]
        link = re.sub(r'checkin=\d\d\d\d-\d\d-\d\d', "checkin=" + single_date.strftime(LINK_DATE_FORMAT), link)
        link = re.sub(r'checkout=\d\d\d\d-\d\d-\d\d', "checkout=" + next_day.strftime(LINK_DATE_FORMAT), link)
       # print(str(single_date) + "\n")
        await asyncio.gather(get_day_data(link, hotel_list[hotel_name], next_day), return_exceptions=False)
        
async def get_day_data(link, comparison_map, date):
    page = session.get(link)
  #  print(link + "\n")
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find('table', class_="hprt-table").find('tbody')
    room_copy = {}
    for room_link in table.find_all('a', class_="hprt-roomtype-link"):
        data_room_id = int(room_link['data-room-id'])
        room_name = room_link.find('span', class_="hprt-roomtype-icon-link").get_text(strip = True)
        free_rooms = len(table.find('select', {"data-room-id":str(data_room_id)}).find_all('option')) - 1
        room_copy[data_room_id] = (room_name, comparison_map.get(data_room_id, 0)[1] - free_rooms)

    results = {}
    for key in comparison_map.keys():
        value = comparison_map[key][1]
        if key in room_copy:
            value = room_copy[key][1]
            
        results[key] = (comparison_map[key][0], comparison_map[key][1] - value )

    #print(results)
    #print("\n\n\n\n\n")
    #Results room_id: (room_name, available_rooms)

    for room in results.values:
        for available_count in room[1]:
            workbook.get_worksheet_by_name(hotel_name, )

    return results    

if __name__ == "__main__":
    asyncio.run(main())
