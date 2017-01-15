import argparse
from utilities import Utilities

parser = argparse.ArgumentParser()
parser.add_argument('action', help='The action to be performed')
args = parser.parse_args()

Utilities = Utilities()

if args.action == 'sync':

	Utilities.sync_metadata()

elif args.action == 'link':

	Utilities.associate_ids()

elif args.action == 'validate':

	Utilities.validate_metadata()
