# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table(u'sources_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('real_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=250)),
            ('hub', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hubs.Hub'], null=True)),
        ))
        db.send_create_signal(u'sources', ['Source'])

        # Adding model 'EventGenerator'
        db.create_table(u'sources_eventgenerator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['events.Event'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sources.Source'])),
            ('when', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'sources', ['EventGenerator'])

        # Adding model 'DebugSource'
        db.create_table(u'sources_debugsource', (
            (u'source_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sources.Source'], unique=True, primary_key=True)),
            ('tag', self.gf('django.db.models.fields.TextField')(max_length=60)),
        ))
        db.send_create_signal(u'sources', ['DebugSource'])

        # Adding model 'TestSource'
        db.create_table(u'sources_testsource', (
            (u'source_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sources.Source'], unique=True, primary_key=True)),
            ('test', self.gf('django.db.models.fields.TextField')(max_length=25)),
        ))
        db.send_create_signal(u'sources', ['TestSource'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table(u'sources_source')

        # Deleting model 'EventGenerator'
        db.delete_table(u'sources_eventgenerator')

        # Deleting model 'DebugSource'
        db.delete_table(u'sources_debugsource')

        # Deleting model 'TestSource'
        db.delete_table(u'sources_testsource')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'events.event': {
            'Meta': {'object_name': 'Event'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'change_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'place': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'hubs.hub': {
            'Meta': {'object_name': 'Hub'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'sources.debugsource': {
            'Meta': {'object_name': 'DebugSource', '_ormbases': [u'sources.Source']},
            u'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.Source']", 'unique': 'True', 'primary_key': 'True'}),
            'tag': ('django.db.models.fields.TextField', [], {'max_length': '60'})
        },
        u'sources.eventgenerator': {
            'Meta': {'object_name': 'EventGenerator'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sources.Source']"}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        u'sources.source': {
            'Meta': {'object_name': 'Source'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Event']", 'through': u"orm['sources.EventGenerator']", 'symmetrical': 'False'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hubs.Hub']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '60'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"})
        },
        u'sources.testsource': {
            'Meta': {'object_name': 'TestSource', '_ormbases': [u'sources.Source']},
            u'source_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sources.Source']", 'unique': 'True', 'primary_key': 'True'}),
            'test': ('django.db.models.fields.TextField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['sources']