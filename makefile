all: battery/battery.json

build:
	python3 -m build

upload:
	twine upload dist/*

getjson2toml:
	curl https://raw.githubusercontent.com/yunruse/.config/zsh/bin/json2toml > json2toml
	chmod +x json2toml
	@echo
	@echo "move this to your ~/bin before using!"

battery/battery.json: battery/battery.toml
	json2toml battery/battery.toml battery/battery.json