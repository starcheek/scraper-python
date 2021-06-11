#!/usr/bin/env python3
available_room_color = "yellow"
taken_room_color = "blue"

baselinks = {
    "jolanta": "https://www.booking.com/hotel/lv/jolanta.lv.html?aid=397594;label=gog235jc-1FCAEoggI46AdIGlgDaIoBiAEBmAEauAEXyAEM2AEB6AEB-AECiAIBqAIDuAKirOiFBsACAdICJGFjZjA1MWE1LTdkODctNGFhMC1hNzgzLWRiMDM5MzQ5N2FlN9gCBeACAQ;sid=c46130fdae3af06545fba388f7c95691;all_sr_blocks=26630902_241064272_1_1_0;checkin=2021-06-10;checkout=2021-06-11;dest_id=-3206721;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=1;highlighted_blocks=26630902_241064272_1_1_0;hpos=1;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=26630902_241064272_1_1_0__5500;srepoch=1623094322;srpvid=2d568959a95b00aa;type=total;ucfs=1;sig=v1jOEcQgd4#hotelTmpl",
    "bahnhof": "https://www.booking.com/hotel/lv/bahnhofs.lv.html?aid=397594;label=gog235jc-1FCAEoggI46AdIGlgDaIoBiAEBmAEauAEXyAEM2AEB6AEB-AECiAIBqAIDuAKirOiFBsACAdICJGFjZjA1MWE1LTdkODctNGFhMC1hNzgzLWRiMDM5MzQ5N2FlN9gCBeACAQ;sid=c46130fdae3af06545fba388f7c95691;all_sr_blocks=494880606_232022328_1_2_0;checkin=2021-06-12;checkout=2021-06-13;dest_id=-3206721;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=1;highlighted_blocks=494880606_232022328_1_2_0;hpos=1;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=494880606_232022328_1_2_0__8500;srepoch=1622883240;srpvid=ed3d3e930b940013;type=total;ucfs=1&#hotelTmpl",
    "ierulle": "https://www.booking.com/hotel/lv/ierulle.lv.html?aid=397594;label=gog235jc-1DCAEoggI46AdIGlgDaIoBiAEBmAEauAEXyAEM2AED6AEB-AECiAIBqAIDuAKirOiFBsACAdICJGFjZjA1MWE1LTdkODctNGFhMC1hNzgzLWRiMDM5MzQ5N2FlN9gCBOACAQ;sid=c46130fdae3af06545fba388f7c95691;all_sr_blocks=46907103_205808313_1_1_0;checkin=2021-09-22;checkout=2021-09-23;dest_id=-3206721;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=4;highlighted_blocks=46907103_205808313_1_1_0;hpos=4;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=46907103_205808313_1_1_0__2499;srepoch=1623399778;srpvid=9c913af1eda0015c;type=total;ucfs=1;sig=v12yQHiR6w#_",
    "lake_studio": "https://www.booking.com/hotel/lv/lake-aluksne-studio-apartment.lv.html?aid=397594;label=gog235jc-1DCAEoggI46AdIGlgDaIoBiAEBmAEauAEXyAEM2AED6AEB-AECiAIBqAIDuAKirOiFBsACAdICJGFjZjA1MWE1LTdkODctNGFhMC1hNzgzLWRiMDM5MzQ5N2FlN9gCBOACAQ;sid=c46130fdae3af06545fba388f7c95691;all_sr_blocks=532708601_285711835_4_0_0;checkin=2021-09-22;checkout=2021-09-23;dest_id=-3206721;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=8;highlighted_blocks=532708601_285711835_4_0_0;hpos=8;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=532708601_285711835_4_0_0__6900;srepoch=1623400191;srpvid=32eb3bbfe643008e;type=total;ucfs=1;sig=v1Jebzl8Wz#hotelTmpl",
    "deco_apartment": "https://www.booking.com/hotel/lv/deco-apartments-in-city-center.lv.html?aid=397594;label=gog235jc-1DCAEoggI46AdIGlgDaIoBiAEBmAEauAEXyAEM2AED6AEB-AECiAIBqAIDuAKirOiFBsACAdICJGFjZjA1MWE1LTdkODctNGFhMC1hNzgzLWRiMDM5MzQ5N2FlN9gCBOACAQ;sid=c46130fdae3af06545fba388f7c95691;all_sr_blocks=699092301_288399541_2_0_0;checkin=2021-09-22;checkout=2021-09-23;dest_id=-3206721;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=18;highlighted_blocks=699092301_288399541_2_0_0;hpos=18;no_rooms=1;req_adults=1;req_children=0;room1=A;sb_price_type=total;sr_order=popularity;sr_pri_blocks=699092301_288399541_2_0_0__12000;srepoch=1623400314;srpvid=58043bfd35d6006a;type=total;ucfs=1;sig=v1ThI-ovW0#hotelTmpl",
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
    },
    "ierulle": {
        46907103: ('Divvietīgs numurs (2 gultas) ar koplietošanas vannas istabu', 1),
        46907101: ('Divvietīgs numurs (1 gulta)', 1),
        46907105: ('Divvietīgs numurs (2 gultas)', 1),
        46907102: ('Luksusa divvietīgs numurs (1 gulta)', 1)
    },
    "lake_studio": {
        532708601: ('Studijas tipa dzīvoklis', 1)
    },
    "deco_apartment": {
        699092301: ('Divu guļamistabu dzīvoklis', 1)
    }
}
