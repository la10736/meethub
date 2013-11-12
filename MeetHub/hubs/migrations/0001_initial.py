# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Hub'
        db.create_table(u'hubs_hub', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'hubs', ['Hub'])


    def backwards(self, orm):
        # Deleting model 'Hub'
        db.delete_table(u'hubs_hub')


    models = {
        u'hubs.hub': {
            'Meta': {'object_name': 'Hub'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        }
    }

    complete_apps = ['hubs']