from kivy.app import App

def prefs_col(name):
	app = App.get_running_app()
	section, key = name.split('.')
	return eval(app.config[section][key])

def pref(name):
	app = App.get_running_app()
	section, key = name.split('.')
	try:
		return float(app.config[section][key])
	except:
		return app.config[section][key]
