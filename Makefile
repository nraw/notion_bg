run:
	python3 main.py

install:
	pip3 install -r requirements.txt

run_tlama:
	python3 main.py --games_filter=all --data_updates=['Tlama']
