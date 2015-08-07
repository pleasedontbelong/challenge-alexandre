from segmentsconfigapp.models import SegmentsConfig

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from segmentsconfigapp.parser import ParserSegmentConfig

#Use the parser
def parse_rules_validator(value):
	p = ParserSegmentConfig()
	res = p.parse(value)
	p.debug_print()
	if res == False:
		raise serializers.ValidationError("Parser Error : " + p.last_error)
	return value

def alphanumerical_validator(value):
	if value.isalnum() == False:
		raise serializers.ValidationError("The attribute name must be alphanumerical")
	return value

class SegmentsConfigSerializer(serializers.HyperlinkedModelSerializer):
	rules_set = serializers.CharField(validators=[parse_rules_validator])
	name = serializers.CharField(validators=[alphanumerical_validator, 
		UniqueValidator(queryset=SegmentsConfig.objects.all())])

	class Meta:
		model = SegmentsConfig
		fields = ('name', 'rules_set', 'date_creation')

