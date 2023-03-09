all: battery.json

getjson2toml:
	curl https://raw.githubusercontent.com/yunruse/.config/zsh/bin/json2toml > json2toml
	chmod +x json2toml
	@echo
	@echo "move this to your ~/bin before using!"

battery.json: battery.toml
	json2toml battery.toml battery.json
