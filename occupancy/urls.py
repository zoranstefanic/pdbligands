from django.conf.urls import *
from occupancy.views import *

urlpatterns = patterns("occupancy.views",
    url(r"^search/$", 'search', name="search"),
    url(r"^totals/$", 'totals', name="totals"),
    url(r"^ligand_types/$", 'ligand_types', name="ligand_types"),
    url(r"^2index/$", 'two_word_index', name="two_word_index"),
    url(r"^interesting/(?P<limit>\d\.\d+)?$", 'interesting', name="interesting"),
    url(r"^pdbs/$", PDBstructureList.as_view(), name="pdb_list"),
    url(r"^ligands/$", LigandList.as_view(), name="ligand_list"),
    url(r"^ligand_pdbs/(\w+)$", "ligand_pdbs", name="ligand_pdbs"),
    url(r"^pdbs/(?P<code>\w+)/$", PDBstructureDetail.as_view(), name="pdb_detail_view"),
    url(r"^ligands/(?P<pk>\d+)/$", LigandDetail.as_view(), name="ligand_detail_view"),
)
