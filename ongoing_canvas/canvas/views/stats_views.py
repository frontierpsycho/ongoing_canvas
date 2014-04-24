import string

from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q, Count

from ongoing_canvas.canvas.models import FeelingData, Feeling
from ongoing_canvas.canvas.form_generator.form_generator import *
from ongoing_canvas.canvas.form_generator.placement_strategy import GridPlacementStrategy

form_generator = FormGenerator("ongoing_canvas/canvas/form_data/colors.json", "ongoing_canvas/canvas/form_data/shapes.json", GridPlacementStrategy(settings.CANVAS_HEIGHT, settings.CANVAS_WIDTH, settings.SHAPE_HEIGHT, settings.SHAPE_WIDTH, depth=1))

class AJAXStatisticsView(View):
	def get_data(self):
		return '{ "girl": "dayum!" }'

	def get(self, request, *args, **kwargs):
		response = HttpResponse(content_type="application/json")
		response.write(self.get_data())

		return response

class TopMoods(AJAXStatisticsView):
	def get_data(self):
		feelingDataSize = FeelingData.objects.count()
		annotated_feelings = [(annotated_feeling, annotated_feeling.fd_count) for annotated_feeling in Feeling.objects.annotate(fd_count=Count('feelingdata')).order_by('-fd_count')[:10] if annotated_feeling.fd_count > 0]

		feeling_colours = []

		for annotated_feeling in annotated_feelings:
			tupleOrNone = form_generator.get_feeling_coordinates(annotated_feeling[0].name)
			if tupleOrNone:
				(current_group_name, subgroup_index) = tupleOrNone
				colour = FormGenerator.get_colour(form_generator.settings["Coloring schemes"][current_group_name][subgroup_index], in_hsl=True)

				feeling_colours.append(colour)

		data = {
			"feelingDataSize": feelingDataSize,
			"feelingCounts": [t[1] for t in annotated_feelings],
			"feelingLegend": [string.capitalize(t[0].name) for t in annotated_feelings],
			"feelingColours": feeling_colours
		}
		return json.dumps(data)


