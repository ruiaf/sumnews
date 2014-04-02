from django import template

register = template.Library()

@register.inclusion_tag('single_doc.html')
def show_doc(doc):
    return {'doc': doc}

@register.inclusion_tag('single_cluster.html')
def show_cluster(cluster):
    return {'cluster': cluster}