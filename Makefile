default: menu

menu:
	@node ./scripts/menu.js

update-data:
	@python ./update-data.py  -y 2013 2014 2015

update-games:
	@echo "[+] Updating data files..."
	@echo "    - This may take a while on your first run..."
	@python ./update-game-data.py  -y 2013 2014 2015

clean:
	@echo "[+] Cleaning data..."
	@rm -rf ./data
	@mkdir ./data
	@mkdir ./data/pickle
	@mkdir ./data/csv

install:
	@npm install
	@pip install -r requirements.txt
	@mkdir -p ./data/pickle
	@mkdir -p ./data/csv
