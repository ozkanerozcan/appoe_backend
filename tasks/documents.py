from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Post, List

@registry.register_document
class TaskDocument(Document):

    list = fields.ObjectField(properties={
        'title': fields.TextField(
            fields={'raw': fields.KeywordField()},
            analyzer="keyword"),
        'group': fields.ObjectField(properties={
            'title': fields.TextField(),
        })
    })


    created_by = fields.ObjectField(properties={
        'username': fields.TextField(
            fields={'raw': fields.KeywordField()},
            analyzer="keyword"
        )
    })

    
    
    class Index:
        name = "taks_posts"

    class Django:
        model = Post
        fields = ["id", "title", "body", "deadline_at", "status", "worked_on"]