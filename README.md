# CS 4260 Program 3
This is a python program that uses a heuristic depth-first search to generate round trip road trips based on utility values determined by a handcrafted regression tree. It also takes into account user inputs for required and forbidden locations.

## Repository Structure
```
cs4260-pa3/
├── LocThemesUtil.csv       # CSV file containing locations, themes, and utilities
├── EdgeThemesUtil.csv      # CSV file containing edges, themes, and utilities
│
├── GenerateThemes.py       # Randomly generates themes for locations and edges
│
├── Location.py             # Class representing a location
├── Edge.py                 # Class representing an edge
├── Graph.py                # Class representing a graph
│
├── LocationRegTree.py      # Builds regression tree for locations
├── EdgeRegTree.py          # Builds regression tree for edges
│
├── RoundTripRoadTrip.py    # Finds round trip road trips
│
└── results.txt             # Road trips and summary statistics are written here
```
