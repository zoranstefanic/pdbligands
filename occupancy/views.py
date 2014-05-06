from django.shortcuts import render, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from occupancy.models import PDBstructure, Ligand
from occupancy.forms import SearchForm
import itertools

import numpy as np
from django.db.models import Count
from find_interesting import all_equal
from word_count import two_words

def search(request):
	if request.GET.get('q'):
		q = request.GET['q']
		pdbs = PDBstructure.objects.filter(abstract__icontains=q)
		return render(request, 'occupancy/search.html',{'query':q, 'number':len(pdbs),'object_list':pdbs})
	else:
		return redirect('pdb_list')

class PDBstructureList(ListView):
    model = PDBstructure
    paginate_by = 20

class LigandList(ListView):
    model = Ligand
    paginate_by = 20

class PDBstructureDetail(DetailView):
    queryset = PDBstructure.objects.all()

class LigandDetail(DetailView):
    queryset = Ligand.objects.all()

def totals(request):
	total_pdbs = PDBstructure.objects.count()
	total_ligands = Ligand.objects.count()
	ligands = Ligand.objects.all().order_by('code')
	types = itertools.groupby(ligands, lambda a: a.code)
	total_types = 0
	for t in types:
		total_types += 1
	return render(request,'occupancy/totals.html', { 
                   'total_pdbs': total_pdbs,
                   'total_ligands': total_ligands,
                   'total_types': total_types,
                   })

def ligand_types(request):
	ligands = Ligand.objects.all()
	ligands = ligands.order_by('code')
	types = itertools.groupby(ligands, lambda a: a.code)
	d = {}
	for t,v in types:
		d[t] = [i for i in v]
	return render(request,'occupancy/ligand_types.html',{'types':d})

def ligand_pdbs(request,code):
	pdbs = PDBstructure.objects.filter(ligands__code=code)
	return render(request,'occupancy/pdbstructure_list.html',{'object_list':pdbs,'form':SearchForm})

def interesting(request,limit=0.1):
	pdb_ligands = PDBstructure.objects.annotate(num_ligands=Count('ligands'))
	two_or_more_ligands = pdb_ligands.exclude(num_ligands=1)
	limit = float(limit)	
	ret = []
	for s in two_or_more_ligands:
		ligands = s.ligands.all()
		ligand_codes = [l.code for l in s.ligands.all()]
		ligand_types = set(ligand_codes)
		for lt in ligand_types:
			chosen = ligands.filter(code=lt)
			if len(chosen) > 1:
				occs = [l.occupancy for l in chosen]
				variance =  np.std(occs)
				if not all_equal(occs) and variance > limit:
					ret.append([s,lt,occs,variance])
	return render(request,'occupancy/interesting.html',{'interesting':ret})

def two_word_index(request):
	d = {}
	abstract_pdb = PDBstructure.objects.exclude(abstract=None)
	for pdb in abstract_pdb:
		abstract = pdb.abstract.lower()
		for i in two_words(abstract):
			d.setdefault(i,0)
			d[i] += 1
	twowords = sorted(d,key=d.get,reverse=True)
	words = []
	for k in twowords:
		if d[k] < 100:
			break
		words.append((k,d[k]))
	return render(request,'occupancy/two_word_index.html', {'words':words}) 



