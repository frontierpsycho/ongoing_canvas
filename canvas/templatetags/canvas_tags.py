from django import template

register = template.Library()

@register.filter
def to_raphael(value, arg):
	shadow = '{}.path("{}").attr({{ fill: "#444", "stroke" : "none" }})'.format(arg, value.path)
	ret = '{}.path("{}").attr({{ fill: "{}", "stroke-width" : 0 }})'.format(arg, value.path, value.colour)
	if value.transformation_matrix != "":
		tm = value.transformation_matrix
		shadow_transform_string = '.blur(2).transform(Raphael.matrix({}, {}, {}, {}, {}, {}).toTransformString())'.format(tm[0], tm[1], tm[2], tm[3], tm[4]+4, tm[5]+4) 
		transform_string = '.transform(Raphael.matrix({}, {}, {}, {}, {}, {}).toTransformString())'.format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5]) 
		ret += transform_string
		shadow += shadow_transform_string

	return shadow+"; "+ret

