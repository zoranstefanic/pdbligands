from django.db import models
from django.shortcuts import redirect

from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
from bs4 import BeautifulSoup
import numpy as np
import urllib2
from tempfile import NamedTemporaryFile

class PDBstructure(models.Model):
	"PDB strcture"
	code = models.CharField(max_length=4, verbose_name="PDB_code")
	abstract = models.TextField(max_length=2000, verbose_name="Pub_med_abstract",null=True,blank=True)
	reference = models.TextField(max_length=300, verbose_name="Reference",null=True,blank=True)
	doi  = models.TextField(max_length=30, verbose_name="Doi",null=True,blank=True)
	oligomer  = models.TextField(max_length=30, verbose_name="oligomer",null=True,blank=True)
	ligand_types = models.ManyToManyField('Ligand_type',related_name="in_pdbs",null=True)

	def __unicode__(self):
		return self.code

	def pdb_url(self):
		return 'http://www.rcsb.org/pdb/explore/explore.do?structureId=' + self.code

	def get_mmcif(self):
		url = "http://www.rcsb.org/pdb/files/%s.cif?headerOnly=YES" %self.code
		f = urllib2.urlopen(url)
		ciflines = f.readlines()
		outfile = open('mmcifs/' + self.code + '.mmcif','w')
		outfile.writelines(ciflines[1:-1])
		print 'Wrote: %s cif' %self.code
		outfile.close()

	def get_abstract(self):
		url = "http://www.rcsb.org/pdb/files/%s.cif?headerOnly=YES" %self.code
		f = urllib2.urlopen(url)
		ciflines = f.readlines()
		try:
			for line in ciflines:
				if line.startswith('_citation.pdbx_database_id_PubMed'):
					pubmedid = line.split()[1]
			pubmed_link = "http://www.ncbi.nlm.nih.gov/pubmed/%s?dopt=Abstract" %pubmedid
			f = urllib2.urlopen(pubmed_link)
			html = f.read()
			soup = BeautifulSoup(html)
			a = soup.find_all(class_="abstr")[0]
			self.abstract = str(a.p)
			self.save()
		except:
			pass

	def get_abstract_from_mmcif(self):
		url = "http://www.rcsb.org/pdb/files/%s.cif?headerOnly=YES" %self.code
		f = urllib2.urlopen(url).read()
		tmpf = NamedTemporaryFile()
		tmpf.write(f)
		mmcif = MMCIF2Dict(tmpf.name)
		try:
			pubmedid = mmcif.get('_citation.pdbx_database_id_PubMed')[0]
			print pubmedid
			pubmed_link = "http://www.ncbi.nlm.nih.gov/pubmed/%s?dopt=Abstract" %pubmedid
			f = urllib2.urlopen(pubmed_link)
			html = f.read()
			soup = BeautifulSoup(html)
			a = soup.find_all(class_="abstr")[0]
			self.abstract = str(a.p)
			self.save()
		except:
			print 'no abstract save for', self.code
			pass

	def get_info_from_mmcif(self,key):
		cifname = 'mmcifs/' + self.code + '.mmcif'
		try:
			mmcif = MMCIF2Dict(cifname)
			return mmcif.get(key)
		except:
			print 'no %s in %s' %(key,self.code)

	def get_oligomeric_state(self):
		state = self.get_info_from_mmcif('_pdbx_struct_assembly.oligomeric_details')
		if type(state) == type([]):
			self.oligomer = state[0]
		else:
			self.oligomer = state
		self.save()
		print 'Saved %s as %s' %(self, self.oligomer)

	def img_url(self):
		return 'http://www.rcsb.org/pdb/images/%s_bio_r_250.jpg' %self.code

class Ligand(models.Model):
	code = models.CharField(max_length=3, verbose_name="Ligand code")
	chain_id = models.CharField(max_length=1, verbose_name="Chain id")
	pdb = models.ForeignKey('PDBstructure',related_name="ligands")
	ltype = models.ForeignKey('Ligand_type',related_name="ligands_of_this_type",null=True)
	occupancy = models.FloatField(null=True)

	def __unicode__(self):
		return self.code + ' ' + self.chain_id

	def url(self):
		return '/occupancy/ligand_pdbs/' + self.code

	def img_url(self):
		return 'http://www.rcsb.org/pdb/images/%s_200.gif' %self.code

class Ligand_type(models.Model):
	code = models.CharField(max_length=3, verbose_name="Ligand type")

	def __unicode__(self):
		return self.code

	def url(self):
		return '/occupancy/ligand_type/' + self.code

	def img_url(self):
		return 'http://www.rcsb.org/pdb/images/%s_200.gif' %self.code
