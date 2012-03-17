# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Feeling.color'
        db.delete_column('canvas_feeling', 'color')


    def backwards(self, orm):
        
        # Adding field 'Feeling.color'
        db.add_column('canvas_feeling', 'color', self.gf('django.db.models.fields.CharField')(default='#5c5c5c', max_length=64), keep_default=False)


    models = {
        'canvas.feeling': {
            'Meta': {'object_name': 'Feeling'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'})
        },
        'canvas.feelingdata': {
            'Meta': {'object_name': 'FeelingData'},
            'born': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'conditions': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'feeling': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['canvas.Feeling']"}),
            'gender': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2'}),
            'postdatetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'posturl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'sentence': ('django.db.models.fields.TextField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        }
    }

    complete_apps = ['canvas']
