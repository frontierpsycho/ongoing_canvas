from multiprocessing import Process, Manager
import datetime
from collections import OrderedDict

from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from django_socketio import broadcast_channel, NoSocket

from canvas.models import FeelingData
from canvas.form_generator.form_generator import *
from canvas.form_generator.placement_strategy import GridPlacementStrategy
from canvas.forms import PlaygroundFilterForm

def start_generator(cells_manager, grid_manager):
	form_generator = FormGenerator("canvas/form_data/colors.json", "canvas/form_data/shapes.json", GridPlacementStrategy(settings.CANVAS_HEIGHT, settings.CANVAS_WIDTH, settings.SHAPE_HEIGHT, settings.SHAPE_WIDTH, grid_manager, depth=1), cells_manager, ongoing=True)

detail_form_generator = FormGenerator("canvas/form_data/colors.json", "canvas/form_data/shapes.json", GridPlacementStrategy(settings.CANVAS_HEIGHT, settings.CANVAS_WIDTH, settings.SHAPE_HEIGHT, settings.SHAPE_WIDTH, depth=1))

manager = Manager()

cells = manager.dict()
grid = manager.list()

p = Process(target=start_generator, args=(cells, grid))
p.start()

class CanvasView(ListView):
	global cells
	global grid
	context_object_name = "shapes"
	template_name="canvas/canvas.html"

	def get_queryset(self):
		shapes = OrderedDict()
		# flatten grid
		fd_ids = [subitem for sublist in grid for item in sublist for subitem in item]
		for fd_id in fd_ids:
			shapes[fd_id] = cells[fd_id]
		return shapes
	
	def get_context_data(self, **kwargs):
		context = super(CanvasView, self).get_context_data(**kwargs)
		context["width"] = settings.CANVAS_WIDTH
		context["height"] = settings.CANVAS_HEIGHT
		context['ongoing'] = True
		return context

class SnapshotView(CanvasView):
	template_name="canvas/snapshot.html"

class PlaygroundView(CanvasView):
	context_object_name = "shapes"
	template_name = "canvas/playground.html"

	def get_queryset(self):
		filters = []
		self.feelings = []
		self.date = None
		self.intensities = []
		self.blackwhite = False

		playground_form_generator = FormGenerator("canvas/form_data/colors.json", "canvas/form_data/shapes.json", GridPlacementStrategy(settings.CANVAS_HEIGHT, settings.CANVAS_WIDTH, settings.SHAPE_HEIGHT, settings.SHAPE_WIDTH, grid=[], depth=1))

		if self.request.GET:
			self.form = PlaygroundFilterForm(self.request.GET)
			if self.form.is_valid(): # All validation rules pass
				self.date = self.form.cleaned_data['date']

				if self.date:
					# ugly filter to get data from specific date
					filters.extend([Q(postdatetime__gte=datetime.datetime.combine(self.date, datetime.time.min)), Q(postdatetime__lte=datetime.datetime.combine(self.date, datetime.time.max))])

				intensities = ["intensity%d" % i for i in range(4)]
				for index, intensity in enumerate(intensities):
					if self.form.cleaned_data[intensity]:
						self.intensities.append(index)

				self.blackwhite = self.form.cleaned_data['blackwhite']
				playground_form_generator.blackwhite = self.blackwhite

				self.feelings.extend(self.request.GET.getlist('feeling'))
				if 'specificFeeling' in self.request.GET:
					self.specificFeeling = self.request.GET['specificFeeling']
					self.feelings.append(self.specificFeeling)

				filters.append(Q(feeling__name__in=playground_form_generator.expand_feeling_list(self.feelings, intensity_list=self.intensities)))
		else:
			self.form = PlaygroundFilterForm()


		feelingdata = FeelingData.objects.filter(*filters).order_by("postdatetime")

		feelingdata = feelingdata[:playground_form_generator.placement_strategy.number_of_cells()]
		
		self.feelingtree = playground_form_generator.feeling_categories_to_json()
		self.search_list = playground_form_generator.feelings_to_json()

		shapes = []
		for fd in feelingdata:
			shape, remove_list = playground_form_generator.generate_shape(fd)
			if shape is not None: 
				shapes.append(shape)
		return shapes

	def get_context_data(self, **kwargs):
		context = super(PlaygroundView, self).get_context_data(**kwargs)
		context['ongoing'] = False
		context['form'] = self.form
		context['feelingtree'] = self.feelingtree
		context['search_list'] = self.search_list
		context['checked_nodes'] = json.dumps(self.feelings)
		context['special'] = json.dumps({'intensities': self.intensities, 'blackwhite': self.blackwhite})
		if self.date:
			context['chosen_date'] = self.date
		if self.specificFeeling:
			context['specificFeeling'] = self.specificFeeling

		return context

class FeelingDataDetailView(DetailView):
	context_object_name = "feeling"
	queryset = FeelingData.objects.all()

	def dispatch(self, request, *args, **kwargs):
		if request.is_ajax():
			self.template_name_suffix = "_detail_ajax"
		return super(FeelingDataDetailView, self).dispatch(request, *args, **kwargs)

	def get_object(self, **kwargs):
		object = super(FeelingDataDetailView, self).get_object()

		return object

	def get_context_data(self, **kwargs):
		context = super(FeelingDataDetailView, self).get_context_data(**kwargs)
		tupleOrNone = detail_form_generator.get_feeling_coordinates(self.get_object().feeling.name)
		if tupleOrNone:
			(current_group_name, subgroup_index) = tupleOrNone
			shape = Shape(detail_form_generator.shapes[current_group_name][0], self.get_object())
			shape.colour = "hsl(%d, %d, %d)" % (0, 0, 100)  # make shape white
			context['shape'] = shape
			context['category'] = current_group_name

		return context

def statistics(request):
	return "Stats!"

@csrf_exempt
def broadcast(request):
	global cells
	if len(cells) > 0:
		fd_id = request.POST["id"]
		remove_list = request.POST["remove"]

		shape = cells[int(fd_id)]
		try:
			broadcast_channel({ 'fd_id': fd_id, 'shape': shape.path, 'colour': shape.colour, 'transform': shape.transformation_matrix, "remove": remove_list } , "shapes")
		except NoSocket:
			logger.error("No subscribers on channel shapes")
	return HttpResponse()
