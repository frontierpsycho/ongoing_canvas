import xml.etree.ElementTree as ET
import copy

from django.views.generic import ListView

from canvas.models import FeelingData

class CanvasView(ListView):
	context_object_name = "feelingdata"
	template_name="canvas/canvas.html"
	
	def get_queryset(self):
		queryset = FeelingData.objects.order_by("postdatetime")[:10]
		
		self.strokes = []
		
		for fd in queryset:
			svg = '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"><svg xmlns="http://www.w3.org/2000/svg" version="1.1"><circle cx="100" cy="50" r="40" stroke="black" stroke-width="2" fill="%s" /></svg>' % fd.feeling.color
			self.strokes.append(svg)
		
		return queryset
		
	def get_context_data(self, **kwargs):
		context = super(CanvasView, self).get_context_data(**kwargs)
		context["strokes"] = self.strokes
		return context
