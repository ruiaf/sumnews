from django import template

register = template.Library()

@register.inclusion_tag('single_doc.html')
def show_doc(doc, edition):
    return {'doc': doc, 'edition': edition}

@register.inclusion_tag('single_cluster.html')
def show_cluster(cluster, edition):
    return {'cluster': cluster, 'edition': edition}