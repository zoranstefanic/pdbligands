from django.shortcuts import render, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from django.views.decorators.cache import cache_page
from occupancy.models import PDBstructure, Ligand, Ligand_type
from occupancy.forms import SearchForm
import itertools

import numpy as np
from django.db.models import Count
from django.db.models.query_utils import Q
from django.http import HttpResponse
from find_interesting import all_equal
from word_count import two_words

PDBS = PDBstructure.objects.select_related().exclude(oligomer='monomeric')
ligands_to_exclude = Q(ligand_types__code="MSE") | Q(ligand_types__code="GOL") | Q(ligand_types__code="CIT") | Q(ligand_types__code="MPD")

PDBS = PDBS.exclude(ligands_to_exclude)

def search(request):
    if request.GET.get('q'):
        q = request.GET['q']
        pdbs = PDBS.filter(abstract__icontains=q)
        return render(request, 'occupancy/search.html',{'query':q, 'number':len(pdbs),'object_list':pdbs})
    else:
        return redirect('pdb_list')

class PDBstructureList(ListView):
    model = PDBstructure
    paginate_by = 20
    queryset = PDBS

class LigandList(ListView):
    model = Ligand
    paginate_by = 20

class PDBstructureDetail(DetailView):
    queryset = PDBstructure.objects.all()
    context_object_name = "pdb"

class LigandDetail(DetailView):
    queryset = Ligand.objects.all()

def totals(request):
    total_pdbs = PDBstructure.objects.count()
    total_ligands = Ligand.objects.count()
    ligands = Ligand.objects.all().order_by('code')
    types = itertools.groupby(ligands, lambda a: a.code)
    total_types = 0
    kinds = []
    oligomer_kinds=set([m[0] for m in PDBstructure.objects.values_list('oligomer')])
    for k in oligomer_kinds:
         kinds.append((k, PDBstructure.objects.filter(oligomer=k).count()))
    for t in types:
        total_types += 1
    return render(request,'occupancy/totals.html', { 
                   'total_pdbs': total_pdbs,
                   'total_ligands': total_ligands,
                   'total_types': total_types,
                   'kinds': kinds,
                   })

def ligand_types(request):
    ligands = Ligand.objects.all()
    ligands = ligands.order_by('code')
    types = itertools.groupby(ligands, lambda a: a.code)
    d = {}
    for t,v in types:
        d[t] = [i for i in v]
    return render(request,'occupancy/ligand_types.html',{'types':d})

def ligand_types_new(request):
    ligtypes = Ligand_type.objects.annotate(pdb_num=Count('in_pdbs')).order_by('-pdb_num')
    return render(request,'occupancy/ligand_types_new.html',{'ligtypes':ligtypes})
    

def ligand_counts(request):
    types = set([c[0] for c in Ligand.objects.values_list('code')])
    l = []
    for t in types:
        l.append((t,PDBS.filter(ligands__code=t).count()))
	l = sorted(l,key=lambda a: a[1], reverse=True)
    return render(request,'occupancy/ligand_counts.html',{'l':l})

def ligand_pdbs(request,code):
    pdbs = PDBstructure.objects.filter(ligands__code=code)
    return render(request,'occupancy/pdbstructure_list.html',{'object_list':pdbs,'form':SearchForm})

def interesting(request,limit):
    if not limit: limit = 0.1
    limit = float(limit)
    ret = []

    pdbs = PDBS.annotate(num_ligands=Count('ligands')).exclude(num_ligands=1)
    for s in pdbs:
        for lt in s.ligand_types.all():
            chosen = s.ligands.filter(code=lt.code)
            if len(chosen) > 1:
                occs = [l.occupancy for l in chosen]
                variance =  np.std(occs)
                if not all_equal(occs) and variance > limit:
                    ret.append([s,lt,occs,variance])
    ret = sorted(ret, key=lambda a: a[-1], reverse=True)
    return render(request,'occupancy/interesting.html',{'interesting':ret})

def two_word_index(request):
    d = {}
    abstract_pdb = PDBS.objects.exclude(abstract=None)
    for pdb in abstract_pdb:
        abstract = pdb.abstract.lower()
        for i in two_words(abstract):
            d.setdefault(i,0)
            d[i] += 1
    twowords = sorted(d,key=d.get,reverse=True)
    words = []
    for k in twowords:
        if d[k] < 10:
            break
        words.append((k,d[k]))
    return render(request,'occupancy/two_word_index.html', {'words':words}) 

def mark_pdb_checked(request):
	from django.core.serializers import serialize
	if request.is_ajax():
		pdb_id = request.POST.get('pdb_id',None)
		pdb=PDBstructure.objects.get(code=pdb_id)
		pdb.checked = True
		pdb.save()
	s = serialize('json',[pdb])
	return HttpResponse(s,mimetype='application/json')
	#return redirect('pdb_list')
