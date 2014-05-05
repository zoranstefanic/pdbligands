# coding: utf-8
from search import *
import numpy as np
from django.db.models import Count

pdb_ligands = PDBstructure.objects.annotate(num_ligands=Count('ligands'))
two_or_more_ligands = pdb_ligands.exclude(num_ligands=1)

def two_same_ligands(s):
    ligs = [l.code for l in s.ligands.all()]
    return len(set(ligs)) != len(ligs)


def all_equal(l):
	return len(set(l)) <= 1

def same_ligand_different_occupancy(s):
	ligands = s.ligands.all()
	ligand_codes = [l.code for l in s.ligands.all()]
	ligand_types = set(ligand_codes)
	s = ''
	for lt in ligand_types:
		chosen = ligands.filter(code=lt)
		if len(chosen) > 1:
			occs = [l.occupancy for l in chosen]
			variance = np.std(occs)
			if not all_equal(occs) and variance > 0.05:
				s += '%5.2f %s' %(variance,lt) 
				for lig in chosen:
					s += ' %3.2f' % lig.occupancy
			else:
				pass
		s += '     '
	return s

pdbs_with_two_same_ligands = filter(two_same_ligands,two_or_more_ligands)

def get_ligand_occupancies(s):
    return [l.occupancy for l in s.ligands.all()]

def get_variance(s):
    return np.std([l.occupancy for l in s.ligands.all()])

def write_variances():
	f = open('variances','w')
	for pdb in pdbs_with_two_same_ligands:
		f.write('%6.5f %s %s' %(get_variance(pdb),pdb,same_ligand_different_occupancy(pdb)) +'\n')
	f.close()

