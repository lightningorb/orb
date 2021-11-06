from orb.misc.utils import *

def is_mock():
	return pref('lnd.protocol') == 'mock'

def hostname():
	app = App.get_running_app()
	return app.config['lnd']['hostname']

def grpc_port():
	app = App.get_running_app()
	return app.config['lnd']['grpc_port']

def macaroon():
	app = App.get_running_app()
	return app.config['lnd']['macaroon_admin']

def cert():
	app = App.get_running_app()
	return app.config['lnd']['tls_certificate'].encode()
