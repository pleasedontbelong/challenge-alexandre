import re
import urlparse


from django.shortcuts import render
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import renderers
from rest_framework import pagination
from rest_framework import viewsets
from rest_framework import request
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from segmentsconfigapp.models import SegmentsConfig
from segmentsconfigapp.serializers import SegmentsConfigSerializer
from segmentsconfigapp.parser import ParserSegmentConfig

class SegmentsConfigSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000

@permission_classes((AllowAny, ))
class SegmentsConfigViewSet(viewsets.ModelViewSet):
    queryset = SegmentsConfig.objects.all()
    serializer_class=SegmentsConfigSerializer
    pagination_class=SegmentsConfigSetPagination


@permission_classes((AllowAny, ))
class RulesResultViewSet(viewsets.ViewSet):

	@detail_route(methods=['post'])
	def list_matched(self, request, segments_config_id):
		queryset = SegmentsConfig.objects.filter(name=segments_config_id)
		data = []
		first_segment = queryset.first()
		if first_segment != None:
			p = ParserSegmentConfig()
			p.parse(first_segment.rules_set)
			#We iterate through different links
			for link in request.data:
				found_associate_pattern_to_link(p, link, data)
		return Response(data)

"""
Take in parameter a string corresponding to an URL and try to compare it with every
pattern
"""
def found_associate_pattern_to_link(p, link, data):
	find = False
	if is_url_valid(link) == False:
		data.append({'url': link, 'value': 'NOT_VALID'})
	else:
		for rule in p.rule_list:
			rule_regex = rule[1]

			if str_is_matching(rule_regex, link):
				data.append({'url': link, 'value': rule[0]})
				find = True
		if find == False:
			data.append({'url': link, 'value': 'UNKNOWN'})

def str_is_matching(pattern, str):
	tab_split = pattern.strip('*').split('*')
	for segment in tab_split:
		i = str.find(segment)
		if i == -1:
			return False
		end = i + len(segment)
	return True

def is_url_valid(url):
	res = URLValidator()
	try:
		res(url)
	except ValidationError, e:
		return (False)
	return True