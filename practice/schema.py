import graphene
from graphene_django import DjangoObjectType
from .models import Books

class BookType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ('id', 'name')

class Query(graphene.ObjectType):
    all_books = graphene.List(BookType)

    def resolve_all_books(root, info):
        return Books.objects.filter(pk=1)

schema = graphene.Schema(query=Query)