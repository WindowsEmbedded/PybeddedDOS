import argparse
from src import system
parser = argparse.ArgumentParser(description="Pybedded OS")
parser.add_argument('-P','--path-name',required=False,help="Path file name")
parser.add_argument('--type','-T',choices=['json','dir'],help="Path type")
parser.add_argument('-v','--version',action='version',version=system.getfullver(),help='Display version and exit')
parser.parse_args()
system.start()