from django.conf.urls import *
from occupancy.views import *

urlpatterns = patterns("occupancy.views",
    url(r"^search/$", 'search', name="search"),
    url(r"^totals/$", 'totals', name="totals"),
    url(r"^2index/$", 'two_word_index', name="two_word_index"),
    url(r"^pdbs/$", PDBstructureList.as_view(), name="pdb_list"),
    url(r"^pdbs/(?P<pk>\d+)/$", PDBstructureDetail.as_view(), name="pdbstructure_detail"),
    url(r"^ligands/$", LigandList.as_view(), name="ligand_list"),
    url(r"^ligand_pdbs/(\w+)$", "ligand_pdbs", name="ligand_pdbs"),
    url(r"^ligand_types/$", 'ligand_types', name="ligand_types"),
    url(r"^ligand_types_new/$", 'ligand_types_new', name="ligand_types_new"),
    url(r"^ligands/(?P<pk>\d+)/$", LigandDetail.as_view(), name="ligand_detail"),
    url(r"^ligand_counts/$", 'ligand_counts', name="ligand_counts"),
    url(r"^interesting/(?P<limit>\d\.\d+)?$", 'interesting', name="interesting"),
    url(r"^mark_pdb_checked/$", 'mark_pdb_checked', name="mark_pdb_checked"),
)
