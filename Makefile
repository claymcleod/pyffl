default: menu

menu:
	@node ./scripts/menu.js

clean:
	@mkdir -p ./data

install: clean
	@npm install
	@pip install -r requirements.txt
