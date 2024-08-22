from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Post, List, Group 
from users.models import CustomUser
from django.conf import settings

@registry.register_document
class TaskPostDocument(Document):

    list = fields.ObjectField(properties={
        'title': fields.TextField(),
        'group': fields.ObjectField(properties={
            'title': fields.TextField(),
        })
    })

    created_by = fields.ObjectField(properties={
        'username': fields.TextField(),
        'full_name': fields.TextField()
    })

        
    class Index:
        name = "taks_posts"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Post
        fields = ["title", "body"]
        related_models = [List, Group, CustomUser]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(TaskPostDocument, self).get_queryset().select_related(
            'list',
            'list__group',
            'created_by'
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """

        if isinstance(related_instance, List):
            return Post.objects.filter(list=related_instance)
        elif isinstance(related_instance, Group):
            return Post.objects.filter(list__group=related_instance)
        elif isinstance(related_instance, CustomUser):
            return Post.objects.filter(created_by=related_instance)

    '''
    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Genre):
            return related_instance.genres.all()
        elif isinstance(related_instance, Country):
            return related_instance.countries.all()
        elif isinstance(related_instance, Author):
            return related_instance.authors.all()
        else:
            return []
    '''
