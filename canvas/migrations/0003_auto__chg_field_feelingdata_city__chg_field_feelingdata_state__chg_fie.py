# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'FeelingData.city'
        db.alter_column('canvas_feelingdata', 'city', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

        # Changing field 'FeelingData.state'
        db.alter_column('canvas_feelingdata', 'state', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Changing field 'FeelingData.country'
        db.alter_column('canvas_feelingdata', 'country', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

        # Changing field 'FeelingData.conditions'
        db.alter_column('canvas_feelingdata', 'conditions', self.gf('django.db.models.fields.SmallIntegerField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'FeelingData.city'
        db.alter_column('canvas_feelingdata', 'city', self.gf('django.db.models.fields.CharField')(default='NULL', max_length=64))

        # Changing field 'FeelingData.state'
        db.alter_column('canvas_feelingdata', 'state', self.gf('django.db.models.fields.CharField')(default='NULL', max_length=16))

        # Changing field 'FeelingData.country'
        db.alter_column('canvas_feelingdata', 'country', self.gf('django.db.models.fields.CharField')(default='NULL', max_length=64))

        # Changing field 'FeelingData.conditions'
        db.alter_column('canvas_feelingdata', 'conditions', self.gf('django.db.models.fields.SmallIntegerField')(default='NULL'))


    models = {
        'canvas.feeling': {
            'Meta': {'object_name': 'Feeling'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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
