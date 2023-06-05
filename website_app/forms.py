from django import forms
from website_app.models import *
from bootstrap_datepicker_plus.widgets import DateTimePickerInput

class ClientsForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = "__all__"
        exclude = ('id',)
    
    def __init__(self, *args, **kwargs):
        super(ClientsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['telephone'].widget.attrs['class'] = 'form-control'
    
    def custom_save(self, commit=True):
        instance = super(ClientsForm, self).save(commit=False)
        instance.id = Clients.objects.latest('id').id + 1
        if commit:
            instance.save()
        return instance


class MastersForm(forms.ModelForm):
    class Meta:
        model = Masters
        fields = "__all__"
        exclude = ('id',)
    
    def __init__(self, *args, **kwargs):
        super(MastersForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['telephone'].widget.attrs['class'] = 'form-control'
    
    def custom_save(self, commit=True):
        instance = super(MastersForm, self).save(commit=False)
        instance.id = Masters.objects.latest('id').id + 1
        if commit:
            instance.save()
        return instance


class VehiclesForm(forms.ModelForm):
    class Meta:
        model = Vehicles
        fields = "__all__"
        exclude = ('id',)
    
    def __init__(self, *args, **kwargs):
        super(VehiclesForm, self).__init__(*args, **kwargs)
        self.fields['brand'].widget.attrs['class'] = 'form-control'
        self.fields['model'].widget.attrs['class'] = 'form-control'
        self.fields['manufacture_year'].widget.attrs['class'] = 'form-control'
        self.fields['client'].widget.attrs['class'] = 'form-control form-select'
    
    def custom_save(self, commit=True):
        instance = super(VehiclesForm, self).save(commit=False)
        instance.id = Vehicles.objects.latest('id').id + 1
        if commit:
            instance.save()
        return instance


class ResponsiblesForm(forms.ModelForm):
    class Meta:
        model = Responsibles
        fields = "__all__"
        exclude = ('id',)
    
    def __init__(self, *args, **kwargs):
        super(ResponsiblesForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['telephone'].widget.attrs['class'] = 'form-control'
    
    def custom_save(self, commit=True):
        instance = super(ResponsiblesForm, self).save(commit=False)
        instance.id = Responsibles.objects.latest('id').id + 1
        if commit:
            instance.save()
        return instance


class WarrantiescardsForm(forms.ModelForm):
    class Meta:
        model = Warrantiescards
        fields = "__all__"
        exclude = ('id',)
        widgets = {
            'start_date': DateTimePickerInput(attrs={'placeholder': 'DateTime Start'}),
            'end_date': DateTimePickerInput(attrs={'placeholder': 'DateTime End'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(WarrantiescardsForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget.attrs['class'] = 'form-control'
        self.fields['end_date'].widget.attrs['class'] = 'form-control'
        self.fields['vehicle'].widget.attrs['class'] = 'form-control form-select'
        self.fields['provided_service'].widget.attrs['class'] = 'form-control form-select'
    
    def custom_save(self, commit=True):
        instance = super(WarrantiescardsForm, self).save(commit=False)
        instance.id = Warrantiescards.objects.latest('id').id + 1
        if commit:
            instance.save()
        return instance


class RepairpartsForm(forms.ModelForm):
    class Meta:
        model = Repairparts
        fields = "__all__"
        exclude = ('id',)
    
    def __init__(self, *args, **kwargs):
        super(RepairpartsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['amount_on_station'].widget.attrs['class'] = 'form-control'
        self.fields['amount_on_storage'].widget.attrs['class'] = 'form-control'
    
    def custom_save(self, commit=True):
        instance = super(RepairpartsForm, self).save(commit=False)
        instance.id = Repairparts.objects.latest('id').id + 1
        if commit:
            instance.save()
        return instance


class ProvidedservicesForm(forms.ModelForm):
    class Meta:
        model = Providedservices
        fields = "__all__"
        exclude = ('id',)
    
    def __init__(self, *args, **kwargs):
        super(ProvidedservicesForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['difficulty'].widget.attrs['class'] = 'form-control'
    
    def custom_save(self, commit=True):
        instance = super(ProvidedservicesForm, self).save(commit=False)
        instance.id = Providedservices.objects.latest('id').id + 1
        if commit:
            instance.save()
        return instance


class RepairsessionsForm(forms.ModelForm):
    class Meta:
        model = Repairsessions
        fields = "__all__"
        exclude = ('id', 'order_number')
        widgets = {
            'date_start': DateTimePickerInput(attrs={'placeholder': 'DateTime Start'}),
            'date_end': DateTimePickerInput(attrs={'placeholder': 'DateTime End'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(RepairsessionsForm, self).__init__(*args, **kwargs)
        # self.fields['order_number'].widget.attrs['class'] = 'form-control'
        self.fields['malfunctions'].widget.attrs['class'] = 'form-control'
        self.fields['order_comment'].widget.attrs['class'] = 'form-control'
        self.fields['total_sum'].widget.attrs['class'] = 'form-control'
        self.fields['paid_sum'].widget.attrs['class'] = 'form-control'
        self.fields['if_finished'].widget.attrs['class'] = 'form-check-input'
        self.fields['vehicle'].widget.attrs['class'] = 'form-control form-select'
        self.fields['responsible'].widget.attrs['class'] = 'form-control form-select'
        self.fields['master'].widget.attrs['class'] = 'form-control form-select'
        # self.fields['repair_parts'].widget.attrs['class'] = 'form-control'
        self.fields['provided_services'].widget.attrs['class'] = 'form-control'
    
    def custom_save(self, commit=True):
        instance = super(RepairsessionsForm, self).save(commit=False)
        print(instance.__dict__)
        instance.id = Repairsessions.objects.latest('id').id + 1
        instance.order_number = f"00{instance.id}"
        if commit:
            instance.save()
        return instance



class RepairsessionsRepairpartsForm(forms.ModelForm):
    class Meta:
        model = RepairsessionsRepairparts
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(RepairsessionsRepairpartsForm, self).__init__(*args, **kwargs)
        self.fields['repair_session'].widget.attrs['class'] = 'form-control form-select'
        self.fields['repair_part'].widget.attrs['class'] = 'form-control form-select'
        self.fields['amount'].widget.attrs['class'] = 'form-control'
