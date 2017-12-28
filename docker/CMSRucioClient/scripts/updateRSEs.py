#! /bin/env python
# Script for managing (creating/updating/deleting) the RSEs and their attributes 
# Initially will use PhEDEx nodes information as input,
# should be easily transformed/extended for using other sources. 

import argparse

from rucio.client.accountclient import AccountClient
from rucio.client.rseclient import RSEClient
from rucio.common.exception import Duplicate, RSEProtocolPriorityError, \
	RSEProtocolNotSupported, RSENotFound, InvalidObject

def whoami ( account = 'natasha', auth_type='x509_proxy'):
	"""Runs whoami command for a given account via client tool, requires a valid proxy
	"""
	account_client = AccountClient(account=account, auth_type='x509_proxy')
	print("Connected to rucio as %s" % account_client.whoami()['account'])

def list_rses(client):
	"""Prints names of existing RSEs"""
	for rse in rse_client.list_rses():
		print (rse['rse'])

def add_rse(client, name):
	"""Adds an rse """
	rse_client.add_rse(name)
	if args.verbosity:
		print "Added RSE "+name
		info=rse_client.get_rse(name)
		for q,v in info.iteritems():
			print q+" :  ",v

if __name__ == '__main__':
	parser=argparse.ArgumentParser(
    	description='''
    	creates or updates the RSEs and their attributes based on TMDB information 
     	''',
    	epilog="""This is a test version use with care!""")
	parser.add_argument('--test-auth', action='store_true', \
		help='executes AccountClient.whoami (use --account option to change identity')
	parser.add_argument('--account', default='natasha', help=' use account ')
	parser.add_argument('-v', '--verbose', action='store_true', \
		help='increase output verbosity')
	parser.add_argument('--add-rse', help='add RSE')
	args = parser.parse_args()
	if args.verbose:
		print (args) 
	if args.test_auth:
		whoami(account=args.account)
	# create re-usable RSE client connection: 
	rse_client = RSEClient(account=args.account, auth_type='x509_proxy')
	print "===== Initial list of RSEs:"
	list_rses(rse_client)
	try:
		if args.add_rse:
			print "===== Adding RSE "+args.add_rse
			add_rse(rse_client, args.add_rse)
	except InvalidObject:
		print "InvalidObject exception: "
		print str(InvalidObject)
	print "===== Current list of RSEs:"
	list_rses(rse_client)
