run:
	python3 main.py

install:
	pip3 install -r requirements.txt

run_tlama:
	python3 main.py --games_filter=all --data_updates="['Tlama','Tlama Price','Tlama Availability']"

run_tabletop:
	python3 main.py --games_filter=all --data_updates=['Tabletop Finder']

essen_site:
	python3 make_site.py

essen_site_2024:
	python3 make_site.py --year 2024

essen_site_2025:
	python3 make_site.py --year 2025

essen_site_multi:
	python3 make_site.py --user_names "nraw,user2,user3"
