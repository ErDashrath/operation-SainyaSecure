import graphene

# TODO: Add modular Query/Mutation classes for each app
class Query(graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
