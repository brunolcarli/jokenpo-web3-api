import graphene
from django.conf import settings
from api.models import UserModel
from datetime import datetime
import graphql_jwt
from api.user_auth import access_required



class UserType(graphene.ObjectType):
    id = graphene.ID()
    score = graphene.Int()
    username = graphene.String()



class Query(graphene.ObjectType):

    version = graphene.String(
        description='Returns current API version!'
    )
    def resolve_version(self, info, **kwargs):
        return settings.VERSION

    
    test_auth = graphene.String()
    @access_required
    def resolve_test_auth(self, info, **kwargs):
        return 'You are atuthenticated'

    users = graphene.List(
        UserType,
        username__icontains=graphene.String(),
        score__gte=graphene.Int(),
        score__lter=graphene.Int()
    )
    def resolve_users(self, info, **kwargs):
        return UserModel.objects.filter(**kwargs)


class SignUp(graphene.relay.ClientIDMutation):
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        # Check if username or email already exists
        try:
            UserModel.objects.get(username=kwargs['username'])
        except UserModel.DoesNotExist:
            pass
        else:
            raise Exception('Username already in use')

        # Create user object
        user = UserModel.objects.create(username=kwargs['username'])
        user.set_password(kwargs['password'])
        user.save()

        return SignUp(user)


class SignIn(graphene.relay.ClientIDMutation):
    token = graphene.String()
    user = graphene.Field(UserType)

    class Input:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate_and_get_payload(self, info, **kwargs):
        try:
            user = UserModel.objects.get(
                username=kwargs['username']
            )
        except UserModel.DoesNotExist:
            raise Exception('User not found')

        if not user.check_password(kwargs['password']):
            raise Exception('Invalid password')

        user.last_login = datetime.now()
        user.save()

        session = graphql_jwt.ObtainJSONWebToken.mutate(
            self,
            info,
            username=user.username,
            password=kwargs['password']
        )

        return SignIn(token=session.token, user=user)


class Mutation:
    sign_up = SignUp.Field()
    sign_in = SignIn.Field()
