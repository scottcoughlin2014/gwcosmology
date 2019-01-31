#!/usr/bin/env python

"""this script uploads mean redshift and standard deviation to gracedb
"""
__author__ = "maya.fishbach@ligo.org"

from argparse import ArgumentParser
import json
from ligo.gracedb.rest import GraceDb, DEFAULT_SERVICE_URL
import tempfile

parser = ArgumentParser(description = __doc__)
parser.add_argument("-z", "--redshift", type=float, help="mean redshift of host galaxy")
parser.add_argument("-s", "--sigma", type=float, help="standard deviation of redshift")
parser.add_argument("-g", "--graceid", type=str, help="Grace ID")
parser.add_argument("-G", "--graceurl", type=str, help= "GraceDB url", default=DEFAULT_SERVICE_URL)
args = parser.parse_args()
gracedb = GraceDb(args.graceurl)
galaxy = {'z': args.redshift, 'sigma': args.sigma}
with tempfile.TempFile() as obj:
	obj.write(json.dumps(galaxy))
	obj.seek(0,0)
	gracedb.writeLog(args.graceid, "redshift information", filename = "hostgalaxy-%s.json"%args.graceid, filecontents = obj)

