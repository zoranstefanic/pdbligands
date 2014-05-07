# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PDBstructure'
        db.create_table(u'occupancy_pdbstructure', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('abstract', self.gf('django.db.models.fields.TextField')(max_length=2000, null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.TextField')(max_length=300, null=True, blank=True)),
            ('doi', self.gf('django.db.models.fields.TextField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal(u'occupancy', ['PDBstructure'])

        # Adding model 'Ligand'
        db.create_table(u'occupancy_ligand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('chain_id', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('pdb', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ligands', to=orm['occupancy.PDBstructure'])),
            ('lig_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='type_ligands', null=True, to=orm['occupancy.Ligand_type'])),
            ('occupancy', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'occupancy', ['Ligand'])

        # Adding model 'Ligand_type'
        db.create_table(u'occupancy_ligand_type', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=3)),
        ))
        db.send_create_signal(u'occupancy', ['Ligand_type'])


    def backwards(self, orm):
        # Deleting model 'PDBstructure'
        db.delete_table(u'occupancy_pdbstructure')

        # Deleting model 'Ligand'
        db.delete_table(u'occupancy_ligand')

        # Deleting model 'Ligand_type'
        db.delete_table(u'occupancy_ligand_type')


    models = {
        u'occupancy.ligand': {
            'Meta': {'object_name': 'Ligand'},
            'chain_id': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lig_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'type_ligands'", 'null': 'True', 'to': u"orm['occupancy.Ligand_type']"}),
            'occupancy': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'pdb': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ligands'", 'to': u"orm['occupancy.PDBstructure']"})
        },
        u'occupancy.ligand_type': {
            'Meta': {'object_name': 'Ligand_type'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'occupancy.pdbstructure': {
            'Meta': {'object_name': 'PDBstructure'},
            'abstract': ('django.db.models.fields.TextField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'doi': ('django.db.models.fields.TextField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.TextField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['occupancy']