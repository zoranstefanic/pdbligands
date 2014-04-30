from django.shortcuts import render, redirect
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from occupancy.models import PDBstructure, Ligand
from occupancy.forms import SearchForm
import itertools


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
