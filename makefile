all: battery.json

battery.json: battery.toml
	# https://github.com/yunruse/.config/blob/zsh/bin/json2toml
	json2toml battery.toml battery.json
