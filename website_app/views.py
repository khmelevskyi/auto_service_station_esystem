from django.shortcuts import render, redirect
from website_app.models import *
from website_app.forms import *
from django.db.models.deletion import ProtectedError
from django.contrib import messages
from rest_framework import serializers as rest_serializers
from django.http import JsonResponse, Http404


models_dict = {
    "clients": Clients,
    "masters": Masters,
    "responsibles": Responsibles,
    "vehicles": Vehicles,
    "warrantiescards": Warrantiescards,
    "repairparts": Repairparts,
    "providedservices": Providedservices,
    "repairsessions": Repairsessions,
    "repairsessionsrepairparts": RepairsessionsRepairparts
}

forms_dict = {
    "clients": ClientsForm,
    "masters": MastersForm,
    "responsibles": ResponsiblesForm,
    "vehicles": VehiclesForm,
    "warrantiescards": WarrantiescardsForm,
    "repairparts": RepairpartsForm,
    "providedservices": ProvidedservicesForm,
    "repairsessions": RepairsessionsForm,
    "repairsessionsrepairparts": RepairsessionsRepairpartsForm
}


def main(request):
    return render(request, "index.html")


class DynamicModelSerializer(rest_serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop("model", None)
        super().__init__(*args, **kwargs)
        if model:
            self.Meta.model = model
    class Meta:
        model = None
        fields = "__all__"
        depth = 1



def show(request, table_name_arg):
    model_obj_name: models.Model = models_dict[table_name_arg]
    objs = model_obj_name.objects.all()

    serializer = DynamicModelSerializer(objs, many=True, model=model_obj_name)
    data = serializer.data  # Serialize the queryset
    print(data)
    return render(request, "show_objs.html", context={'data': data, 'table_name': table_name_arg})


def create(request, table_name_arg):
    if request.method == 'POST':
        obj_form_name = forms_dict[table_name_arg]
        obj_form: forms.ModelForm = obj_form_name(request.POST)
        if obj_form.is_valid():
            obj_form.custom_save()
            obj_form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "Обʼєкт додано успішно.")
            return redirect(f"/show/{table_name_arg}")
    else:
        obj_form_name = forms_dict[table_name_arg]
        obj_form: forms.ModelForm = obj_form_name()
    return render(request, 'create_edit.html', {'form': obj_form})


def edit(request, table_name_arg, id):
    model_obj_name = models_dict[table_name_arg]
    if table_name_arg == "repairsessionsrepairparts":
        repair_session_id, repair_part_id = id.split("+")
        obj: models.Model = model_obj_name.objects.filter(repair_session=repair_session_id, repair_part=repair_part_id).first()
    else:
        obj: models.Model = model_obj_name.objects.get(id=id)
    if request.method == 'POST':
        obj_form_name = forms_dict[table_name_arg]
        obj_form: forms.ModelForm = obj_form_name(request.POST, instance = obj)
        if obj_form.is_valid():
            if table_name_arg == "repairsessionsrepairparts":
                obj_form.custom_save()
            else:
                obj_form.save()
            messages.add_message(request, messages.SUCCESS, "Обʼєкт змінено успішно.")
            return redirect(f"/show/{table_name_arg}")
    else:
        obj_form_name = forms_dict[table_name_arg]
        obj_form: forms.ModelForm = obj_form_name(instance = obj)
    return render(request, 'create_edit.html', context={'form': obj_form})


def destroy(request, table_name_arg, id):
    model_obj_name = models_dict[table_name_arg]
    if table_name_arg == "repairsessionsrepairparts":
        repair_session_id, repair_part_id = id.split("+")
        obj: models.Model = model_obj_name.objects.filter(repair_session=repair_session_id, repair_part=repair_part_id).first()
    else:
        obj: models.Model = model_obj_name.objects.get(id=id)
    
    try:
        obj.delete()
        messages.add_message(request, messages.SUCCESS, "Обʼєкт видалено успішно.")
    except ProtectedError as err:
        messages.add_message(request, messages.ERROR, f"Не вдалося видалити обʼєкт. Причина: {str(err)}")
    
    return redirect(f"/show/{table_name_arg}")


def show_api(request, table_name_arg, id=None):
    # Retrieve the model based on `table_name_arg`
    model_obj_name = models_dict.get(table_name_arg)
    if model_obj_name is None:
        raise Http404("Model not found")

    # Check if an ID is provided
    if id is None:
        # No ID provided: serialize all objects
        objs = model_obj_name.objects.all()
        serializer = DynamicModelSerializer(objs, many=True, model=model_obj_name)
        data = serializer.data  # Serialize the queryset
    else:
        # ID provided: serialize a single object
        try:
            obj = model_obj_name.objects.get(id=id)
        except model_obj_name.DoesNotExist:
            raise Http404("Object not found")
        
        serializer = DynamicModelSerializer(obj, model=model_obj_name)
        data = serializer.data  # Serialize the queryset

    # Return JSON response
    return JsonResponse(data, safe=False)