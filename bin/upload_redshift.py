#!/usr/bin/env python

"""this script uploads host galaxy information (mean redshift and standard deviation, RA and DEC) to gracedb
"""
__author__ = "maya.fishbach@ligo.org"

from argparse import ArgumentParser
import json
from ligo.gracedb.rest import GraceDb, DEFAULT_SERVICE_URL
import tempfile
from gwcosmology import utils

parser = ArgumentParser(description = __doc__)
parser.add_argument("-z", "--redshift", type=float, help="mean redshift of host galaxy", required=True)
parser.add_argument("-s", "--sigma", type=float, help="standard deviation of redshift",required=True)
parser.add_argument("-r", "--RA", type=float, help="RA of the host galaxy in degrees",required=True)
parser.add_argument("-d", "--DEC", type=float, help="DEC of the host galaxy in degrees",required=True)
parser.add_argument("-g", "--graceid", type=str, help="Grace ID",required=True)
parser.add_argument("-G", "--graceurl", type=str, help= "GraceDB url. default ="+DEFAULT_SERVICE_URL, default=DEFAULT_SERVICE_URL)
args = parser.parse_args()

gracedb = GraceDb(args.graceurl)

galaxy = {'z': args.redshift, 'sigma': args.sigma, 'RA': args.RA, 'DEC': args.DEC}
with tempfile.TemporaryFile() as obj:
	obj.write(json.dumps(galaxy))
	obj.seek(0,0)
	gracedb.writeLog(args.graceid, "redshift information", filename=utils.galaxy_name(args.graceid), filecontents=obj)
