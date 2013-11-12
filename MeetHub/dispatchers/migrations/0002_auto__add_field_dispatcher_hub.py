# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Dispatcher.hub'
        db.add_column(u'dispatchers_dispatcher', 'hub',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hubs.Hub'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Dispatcher.hub'
        db.delete_column(u'dispatchers_dispatcher', 'hub_id')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dispatchers.debugdispatcher': {
            'Meta': {'object_name': 'DebugDispatcher', '_ormbases': [u'dispatchers.Dispatcher']},
            u'dispatcher_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['dispatchers.Dispatcher']", 'unique': 'True', 'primary_key': 'True'}),
            'tag': ('django.db.models.fields.TextField', [], {'max_length': '60'})
        },
        u'dispatchers.dispatcher': {
            'Meta': {'object_name': 'Dispatcher'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '250'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.Event']", 'through': u"orm['dispatchers.EventDispatched']", 'symmetrical': 'False'}),
            'hub': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hubs.Hub']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '60'}),
            'real_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"})
        },
        u'dispatchers.eventdispatched': {
            'Meta': {'object_name': 'EventDispatched'},
            'dispatcher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dispatchers.Dispatcher']"}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'when': ('django.db.models.fields.DateField', [], {})
        },
        u'dispatchers.testdispatcher': {
            'Meta': {'object_name': 'TestDispatcher', '_ormbases': [u'dispatchers.Dispatcher']},
            u'dispatcher_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['dispatchers.Dispatcher']", 'unique': 'True', 'primary_key': 'True'}),
            'test': ('django.db.models.fields.TextField', [], {'max_length': '25'})
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
        }
    }

    complete_apps = ['dispatchers']