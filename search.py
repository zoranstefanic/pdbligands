#!/bin/env python
import urllib2
import gzip
import os
import random
from Bio.PDB.PDBParser import PDBParser
from bs4 import BeautifulSoup
import numpy as np

from occupancy.models import *

LOCAL_PDB_DIR='/PDB'

def parse_pdb_local(code):
	code = code.lower()
	path = '%s/%s/pdb%s.ent.gz' %(LOCAL_PDB_DIR,code[1:3],code)
	f = gzip.open(path, 'rb')
	p = PDBParser()
	structure = p.get_structure(code,f)
	return structure


def make_django_model(s):
	header = s.header
	ref= header['journal_reference']
	try:
		doi = "http://dx.doi.org/" + ref.split()[-1]
	except:
		doi = ''
	ligands = []
	for c in s.get_chains():      
		for res in c.get_residues():
			if res.get_id()[0][0] == 'H' and len(res.get_list()) > 5:
				if all([a.get_occupancy() < 1.0 for a in res.get_list()]):
					ligands.append(res)
	if ligands and any('ec' in v for v in header['compound'].values()):
		pdb = PDBstructure.objects.create(code=s.id, reference=ref,doi=doi)
		pdb.get_abstract()
		pdb.save()
		for l in ligands:
			lig = Ligand.objects.create(code=l.resname,chain_id=l.get_parent().id, pdb = pdb)
			lig.occupancy = '%3.2f' % np.mean([a.occupancy for a in l.get_list()])
			lig.save()

def run_local():
	pdb_dirs=[os.path.join(LOCAL_PDB_DIR,d) for d in os.listdir(LOCAL_PDB_DIR) if os.path.isdir(os.path.join(LOCAL_PDB_DIR,d))]
	#pdb_dirs = [random.choice(pdb_dirs) for i in range(10)]
	for d in pdb_dirs:
		try:
			pdbs = os.listdir(d)
			print d, len(pdbs)
			for pdb in pdbs:
				code=pdb[3:7]
				f = gzip.open(os.path.join(d,pdb), 'rb')
				p = PDBParser()
				structure = p.get_structure(code,f)
				make_django_model(structure)
		except:
			print 'Problem in dir %s' %d

if __name__ == '__main__':
	import time
	start = time.time()
	run_local()
	end = time.time()
	print 'Total time: %d seconds' %(end - start)
