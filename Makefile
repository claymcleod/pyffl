default: menu

menu:
	@node ./scripts/menu.js

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
