from django import template

register = template.Library()

@register.filter
def to_raphael(value, arg):
	ret = '{}.path("{}").attr({{ fill: "{}", "stroke-width" : 0 }})'.format(arg, value.path, value.colour)
	if value.transformation_matrix != "":
		tm = value.transformation_matrix
		transform_string = '.transform(Raphael.matrix({}, {}, {}, {}, {}, {}).toTransformString())'.format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5]) 
		ret += transform_string

	return ret

