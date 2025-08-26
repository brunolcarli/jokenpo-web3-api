import graphene
import api.schema
import graphql_jwt


class Query(api.schema.Query, graphene.ObjectType):
    pass

class Mutation(graphene.ObjectType, api.schema.Mutation):
    validate_user_token = graphql_jwt.Verify.Field()
    refresh_user_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)