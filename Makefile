default: update-data clean
	@echo "[+] Running analysis..."
	@python ./main.py

update-data: clean
	@echo "[+] Updating data files..."
	@python ./update-data.py  -y 2013 2014 2015

clean:
	@echo "[+] Cleaning data..."
	@rm -rf ./data/*