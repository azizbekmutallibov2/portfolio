from rest_framework import serializers

from apps.contact.validators import validate_contact


class ProjectOutputSerializer(serializers.Serializer):
    slug = serializers.CharField()
    title = serializers.CharField()
    tag = serializers.CharField()
    tag_label = serializers.CharField(source="get_tag_display")
    problem = serializers.CharField()
    solution = serializers.CharField()
    role = serializers.CharField()
    stack = serializers.ListField(child=serializers.CharField(), source="stack_items")
    repo_url = serializers.CharField()
    demo_url = serializers.CharField()


class ContactCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, min_length=2)
    contact = serializers.CharField(max_length=150, validators=[validate_contact])
    message = serializers.CharField(max_length=2000, min_length=10)
