#!/usr/bin/env python3


baselinks = {
    "jolanta": "https://www.booking.com/hotel/lv/jolanta.lv.html?aid=397594;label=gog235jc-1FCAEoggI46AdIGlgDaIoBiAEBmAEauAEXyAEM2AEB6AEB-AECiAIBqAIDuAKirOiFBsACAdICJGFjZjA1MWE1LTdkODctNGFhMC1hNzgzLWRiMDM5MzQ5N2FlN9gCBeACAQ;sid=c46130fdae3af06545fba388f7c95691;all_sr_blocks=26630902_241064272_1_1_0;checkin=2021-06-10;checkout=2021-06-11;dest_id=-3206721;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=1;highlighted_blocks=26630902_241064272_1_1_0;hpos=1;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=26630902_241064272_1_1_0__5500;srepoch=1623094322;srpvid=2d568959a95b00aa;type=total;ucfs=1;sig=v1jOEcQgd4#hotelTmpl",
    "bahnhof": "https://www.booking.com/hotel/lv/bahnhofs.lv.html?aid=397594;label=gog235jc-1FCAEoggI46AdIGlgDaIoBiAEBmAEauAEXyAEM2AEB6AEB-AECiAIBqAIDuAKirOiFBsACAdICJGFjZjA1MWE1LTdkODctNGFhMC1hNzgzLWRiMDM5MzQ5N2FlN9gCBeACAQ;sid=c46130fdae3af06545fba388f7c95691;all_sr_blocks=494880606_232022328_1_2_0;checkin=2021-06-12;checkout=2021-06-13;dest_id=-3206721;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=1;highlighted_blocks=494880606_232022328_1_2_0;hpos=1;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=494880606_232022328_1_2_0__8500;srepoch=1622883240;srpvid=ed3d3e930b940013;type=total;ucfs=1&#hotelTmpl",
}
    
hotel_list = {
    "jolanta": {
    26630902: ('Standarta divvietīgs numurs (1 gulta)', 2),
    26630905: ('Standarta divvietīgs numurs (2 gultas)', 1),
    26630901: ('\"Junior suite\" numurs', 1),
    26630903: ('\"Suite\" numurs', 1)
    },
    "bahnhof": {
    494880604: ('Standarta divvietīgs numurs (1 gulta)', 1),
    494880605: ('Standarta divvietīgs numurs (1 gulta)', 1),
    494880606: ('Standarta divvietīgs numurs (2 gultas)', 1),
    494880607: ('Standarta divvietīgs numurs (2 gultas)', 1),
    494880601: ('"Superior" klases numurs ar "king" izmēra gultu', 1),
    494880602: ('"Superior" klases numurs ar "king" izmēra gultu', 1),
    494880603: ('"Superior" klases numurs ar "king" izmēra gultu', 1),
    494880609: ('"Superior" klases numurs ar "king" izmēra gultu', 1),
    494880608: ('"Suite" numurs ar "king" izmēra gultu un balkonu', 1),
    }
}
