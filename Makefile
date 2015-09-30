default:
	@echo "[+] Running analysis..."
	@cd ./examples/ & ipython notebook

update-data:
	@echo "[+] Updating data files..."
	@echo "    - This may take a while on your first run..."
	@python ./update-data.py  -y 2013 2014 2015

clean:
	@echo "[+] Cleaning data..."
	@rm -rf ./data/*
