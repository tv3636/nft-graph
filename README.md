# nft-graph

Visualizing NFT collections based on shared ownership

https://nft-graph.vercel.app/

## Overview

This repo contains an already-generated list of the top ~1,000 NFT collections by all-time volume (`collections.csv`), up to 6,000 holders of each top collection (`holders.json`), and an html page with an interactive visualization of those collections based on shared ownership (`index.html`).

It also contains a python script to pull updated lists of collections and holders - note that to pull 6,000 holders from ~1,000 top collections took about 12 hours.

### Setup

To run the python script, first run:

`pip install -r requirements.txt`

followed by

`python data.py`


As-is, this will simply generate a new html file based on the existing `collections.csv` and `holders.json`. You can optionally remove `network.set_options` and un-comment `network.show_buttons` to interactively modify the graph settings. 

Use the `getHolders()` or `getCollections()` functions as needed to pull updated data from [Reservoir](https://reservoirprotocol.github.io/).
