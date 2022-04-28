import os
from dotenv import load_dotenv
from pyvis.network import Network
import networkx as nx
import requests
import csv
import json
from collections import defaultdict

load_dotenv()

COLLECTIONS_URL = 'https://api.reservoir.tools/collections/v3?sortBy=allTimeVolume&offset=%d'
HOLDERS_URL = 'https://api.reservoir.tools/owners/v1?collection=%s&offset=%d'
HEADERS = { 'x-api-key': os.environ.get('RESERVOIR_API_KEY') }

IGNORE_LIST = ['0x495f947276749ce646f68ac8c248420045cb7b5e', '0xc36cf0cfcb5d905b8b513860db0cfe63f6cf9f5c']
NAME_IGNORE_LIST = ['nfp']
HOLDER_MAX = 6000
COLLECTION_MAX = 1000
PAGE_SIZE = 20

network = Network(width='100%', height='100%', bgcolor='#000000')
overlap = defaultdict(lambda: defaultdict(int))

# Use collections and holders data already pulled
collections = csv.DictReader(open('collections.csv'))
holders = json.load(open('holders.json'))

# Allows for a set to be JSON serialized
def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

# Pulls 
def getCollections():
	global collectionsDict
	collections = []

	for i in range(COLLECTION_MAX / PAGE_SIZE):
		page = requests.get(COLLECTIONS_URL % (i * PAGE_SIZE), headers=HEADERS).json()['collections']

		for collection in page:
			if not collection['floorAskPrice']:
				collection['floorAskPrice'] = 0

			try:
				if float(collection['floorAskPrice']) < 200 and collection['id'] not in IGNORE_LIST:
					collections.append(collection)
					print(collection['slug'])
				else:
					print(collection)
			except:
				print('failed')
				pass

	return collections

def getHolders(collection, name):
	global holders
	print(collection)
	
	for i in range(HOLDER_MAX / PAGE_SIZE):
		try:
			page = requests.get(HOLDERS_URL % (collection, i * 20), headers=HEADERS).json()
			owners = page['owners']

			if not owners:
				print('done!')
				break

			print(i)

			for holder in owners:
				holders[holder['address']].add(name)
		except:
			print('missed')


# Determine collection overlap
for holder in holders:
	for collection in holders[holder]:
		for otherCollection in holders[holder]:
			if collection != otherCollection:
				overlap[collection][otherCollection] += 1


# Add nodes
for collection in collections:
	if collection['name'] not in NAME_IGNORE_LIST:
		network.add_node(
			collection['name'], 
			label=' ', 
			image=collection['imageURL'],
			shape='circularImage',
			value=float(collection['floor']),
			title=collection['name']
		)

# Add edges
for collection in overlap:
	if collection not in NAME_IGNORE_LIST:
		for neighbor in sorted(overlap[collection], key=overlap[collection].get, reverse=True)[:4]:
			network.add_edge(collection, neighbor, hidden=True)

#network.show_buttons(filter_=['physics'])
network.set_options("""
var options = {
  "physics": {
    "enabled": true,
    "forceAtlas2Based": {
      "gravitationalConstant": -3,
      "springLength": 10,
      "springConstant": 0.975
    },
    "maxVelocity": 50,
    "minVelocity": 0.75,
    "solver": "forceAtlas2Based"
  }
}
	""")
network.show('nx.html')

