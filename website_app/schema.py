import graphene
from graphene_django import DjangoObjectType
from .models import (
    Clients, Masters, Providedservices, Repairparts, Responsibles,
    Vehicles, Warrantiescards, Repairsessions, RepairsessionsProvidedservices,
    RepairsessionsRepairparts
)

# Object Types
class ClientsType(DjangoObjectType):
    class Meta:
        model = Clients
        fields = ("id", "name", "telephone")


class MastersType(DjangoObjectType):
    class Meta:
        model = Masters
        fields = ("id", "name", "telephone")


class ProvidedservicesType(DjangoObjectType):
    class Meta:
        model = Providedservices
        fields = ("id", "name", "category", "difficulty")


class RepairpartsType(DjangoObjectType):
    class Meta:
        model = Repairparts
        fields = ("id", "name", "amount_on_station", "amount_on_storage")


class ResponsiblesType(DjangoObjectType):
    class Meta:
        model = Responsibles
        fields = ("id", "name", "telephone")


class VehiclesType(DjangoObjectType):
    class Meta:
        model = Vehicles
        fields = ("id", "brand", "model", "manufacture_year", "client")


class WarrantiescardsType(DjangoObjectType):
    class Meta:
        model = Warrantiescards
        fields = ("id", "start_date", "end_date", "vehicle", "provided_service")


class RepairsessionsType(DjangoObjectType):
    class Meta:
        model = Repairsessions
        fields = (
            "id", "order_number", "date_start", "date_end", "malfunctions",
            "order_comment", "total_sum", "paid_sum", "if_finished",
            "vehicle", "responsible", "master", "repair_parts", "provided_services"
        )


class RepairsessionsProvidedservicesType(DjangoObjectType):
    class Meta:
        model = RepairsessionsProvidedservices
        fields = ("repair_session", "provided_service")


class RepairsessionsRepairpartsType(DjangoObjectType):
    class Meta:
        model = RepairsessionsRepairparts
        fields = ("repair_session", "repair_part", "amount")


# Mutations
class CreateClient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        telephone = graphene.String(required=True)

    client = graphene.Field(ClientsType)

    def mutate(self, info, name, telephone):
        id = Clients.objects.latest('id').id + 1
        client = Clients(id=id, name=name, telephone=telephone)
        client.save()
        return CreateClient(client=client)


class UpdateClient(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        telephone = graphene.String()

    client = graphene.Field(ClientsType)

    def mutate(self, info, id, name=None, telephone=None):
        try:
            client = Clients.objects.get(pk=id)
        except Clients.DoesNotExist:
            raise Exception("Client not found")

        if name is not None:
            client.name = name
        if telephone is not None:
            client.telephone = telephone

        client.save()
        return UpdateClient(client=client)


class DeleteClient(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            client = Clients.objects.get(pk=id)
            client.delete()
            return DeleteClient(success=True)
        except Clients.DoesNotExist:
            raise Exception("Client not found")


# Queries
class Query(graphene.ObjectType):
    all_clients = graphene.List(ClientsType)
    all_repair_sessions = graphene.List(RepairsessionsType)
    
    repair_session_by_order_number = graphene.Field(RepairsessionsType, order_number=graphene.String(required=True))
    clients_by_name = graphene.List(ClientsType, name=graphene.String(required=True))

    def resolve_all_clients(root, info):
        return Clients.objects.all()

    def resolve_all_repair_sessions(root, info):
        return Repairsessions.objects.all()

    def resolve_repair_session_by_order_number(root, info, order_number):
        try:
            return Repairsessions.objects.get(order_number=order_number)
        except Repairsessions.DoesNotExist:
            return None

    def resolve_clients_by_name(root, info, name):
        return Clients.objects.filter(name__iregex=rf"{name}")


# Schema
class Mutation(graphene.ObjectType):
    create_client = CreateClient.Field()
    update_client = UpdateClient.Field()
    delete_client = DeleteClient.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
