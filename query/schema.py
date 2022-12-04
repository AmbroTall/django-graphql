import graphene
from graphene_django import DjangoObjectType
from .models import Quizzes, Category, Question, Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id","name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id","title","category","quiz")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title","quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question","answer_text")

# ------------------------------Get/Find Methods-------------------------------------
class Query(graphene.ObjectType):
    all_cat = graphene.Field(CategoryType, id=graphene.Int())
    all_ans = graphene.List(AnswerType, id = graphene.Int())
    ques = graphene.Field(QuestionType, id = graphene.Int())

    def resolve_all_cat(root, info, id):
        return Category.objects.get(id=id)
    def resolve_ques(root, info, id):
        return Question.objects.get(id=id)
    def resolve_all_ans(root,info, id):
        return Answer.objects.filter(question=id)




# ---------------------------------Create New Object Into Category The DataBase---------------------------------
class CategoryCreateMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,name):
        category = Category(name=name)
        category.save()
        return CategoryCreateMutation(category=category)

# ---------------------------------Update Existing Object Into Category The DataBase---------------------------------
class CategoryUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info, name, id):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return CategoryUpdateMutation(category=category)

# ---------------------------------Update Existing Object Into Category The DataBase---------------------------------
class CategoryDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return

class Mutations(graphene.ObjectType):
    create_category = CategoryCreateMutation.Field()
    update_category = CategoryUpdateMutation.Field()
    del_categroy = CategoryDeleteMutation.Field()



schema = graphene.Schema(query=Query, mutation=Mutations)