# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'FeelingData'
        db.create_table('canvas_feelingdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feeling', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['canvas.Feeling'])),
            ('sentence', self.gf('django.db.models.fields.TextField')()),
            ('postdatetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('posturl', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('gender', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('born', self.gf('django.db.models.fields.SmallIntegerField')(null=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('lat', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('lon', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2)),
            ('conditions', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('canvas', ['FeelingData'])

        # Adding model 'Feeling'
        db.create_table('canvas_feeling', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('canvas', ['Feeling'])


    def backwards(self, orm):
        
        # Deleting model 'FeelingData'
        db.delete_table('canvas_feelingdata')

        # Deleting model 'Feeling'
        db.delete_table('canvas_feeling')


    models = {
        'canvas.feeling': {
            'Meta': {'object_name': 'Feeling'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'})
        },
        'canvas.feelingdata': {
            'Meta': {'object_name': 'FeelingData'},
            'born': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'conditions': ('django.db.models.fields.SmallIntegerField', [], {}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'feeling': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['canvas.Feeling']"}),
            'gender': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'lon': ('django.db.models.fields.DecimalField', [], {'max_digits': '8', 'decimal_places': '2'}),
            'postdatetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'posturl': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'sentence': ('django.db.models.fields.TextField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['canvas']
