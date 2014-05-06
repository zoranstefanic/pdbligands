# coding: utf-8
from search import *
import codecs

exclude = set('the in the with the for the and the the that the at the in a the is a'.split())

def two_words(s):
    l = s.split()
    for i in range(len(l)-1):
        yield '%s %s' % (l[i], l[i+1])
        
abstract_pdb = PDBstructure.objects.exclude(abstract=None)

def build_two_word_index():
	f = codecs.open('two_word_index.txt','w',encoding="utf-8")
	d = {}
	for pdb in abstract_pdb:
		abstract = pdb.abstract.lower()
		#for word in exclude:
		#	abstract = abstract.replace(word, '')
		for i in two_words(abstract):
			d.setdefault(i,0)
			d[i] += 1
	twowords = sorted(d,key=d.get,reverse=True)
	for k in twowords:
		if d[k] < 100:
			break
		f.write('%-50s %10s\n' %(k,d[k]))
	f.close()

