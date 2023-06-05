from django.db import models


class Clients(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)

    class Meta:
        db_table = 'clients'
        ordering = ['id']
    
    def __str__(self):
        return f'ID клієнта: {self.id} | імʼя: {self.name} | телефон: {self.telephone}'
    
    def natural_key(self):
        return f"{self.id} | {self.name} | {self.telephone}"


class Masters(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)

    class Meta:
        db_table = 'masters'
        ordering = ['id']
    
    def __str__(self):
        return f'ID майстра: {self.id} | імʼя: {self.name} | телефон: {self.telephone}'
    
    def natural_key(self):
        return f"{self.id} | {self.name} | {self.telephone}"


class Providedservices(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)

    class Meta:
        db_table = 'providedservices'
        ordering = ['id']
    
    def __str__(self):
        return f'ID послуги: {self.id} | назва: {self.name} | категорія: {self.category}'
    
    def natural_key(self):
        return f"{self.id} | {self.name} | {self.category}"


class Repairparts(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    amount_on_station = models.IntegerField()
    amount_on_storage = models.IntegerField()

    class Meta:
        db_table = 'repairparts'
        ordering = ['id']
    
    def __str__(self):
        return f'ID запчастини: {self.id} | назва: {self.name}'
    
    def natural_key(self):
        return f"{self.id} | {self.name}"


class Responsibles(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)

    class Meta:
        db_table = 'responsibles'
        ordering = ['id']
    
    def __str__(self):
        return f'ID відповідального: {self.id} | імʼя: {self.name} | телефон: {self.telephone}'
    
    def natural_key(self):
        return f"{self.id} | {self.name} | {self.telephone}"


class Vehicles(models.Model):
    id = models.IntegerField(primary_key=True)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    manufacture_year = models.IntegerField()
    client = models.ForeignKey(Clients, on_delete=models.PROTECT, help_text="Оберіть один з варіантів")

    class Meta:
        db_table = 'vehicles'
        ordering = ['id']
    
    def __str__(self):
        return f'ID авто: {self.id} | марка: {self.brand} | модель: {self.model} | клієнт: {self.client.name}({self.client.id})'
    
    def natural_key(self):
        return f"{self.id} | {self.brand} | {self.model} | {self.client.name}({self.client.id})"
    
    natural_key.dependencies = ["website_app.client"]


class Warrantiescards(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    vehicle = models.ForeignKey(Vehicles, on_delete=models.PROTECT, help_text="Оберіть один з варіантів")
    provided_service = models.ForeignKey(Providedservices, on_delete=models.PROTECT, help_text="Оберіть один з варіантів")

    class Meta:
        db_table = 'warrantiescards'
        ordering = ['id']
    
    def __str__(self):
        return f'ID гарант талона: {self.id} | початок: {self.start_date} | '\
                f'кінець: {self.end_date} | авто: {self.vehicle.brand}({self.vehicle.id}) | '\
                f'послуга: {self.provided_service.name}({self.provided_service.id})'
    
    def natural_key(self):
        return f"{self.id} | {self.vehicle} | {self.provided_service}"


class Repairsessions(models.Model):
    id = models.IntegerField(primary_key=True)
    order_number = models.CharField(max_length=50)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    malfunctions = models.CharField(max_length=255, blank=True, null=True)
    order_comment = models.CharField(max_length=255, blank=True, null=True)
    total_sum = models.IntegerField()
    paid_sum = models.IntegerField()
    if_finished = models.BooleanField()
    vehicle = models.ForeignKey(Vehicles, on_delete=models.PROTECT, help_text="Оберіть один з варіантів")

    responsible = models.ForeignKey(Responsibles, on_delete=models.PROTECT, help_text="Оберіть один з варіантів")
    master = models.ForeignKey(Masters, on_delete=models.PROTECT, help_text="Оберіть один з варіантів")
    # repair_parts = models.ManyToManyField(Repairparts, through='RepairsessionsRepairparts', help_text="Оберіть один або більше варантів")
    provided_services = models.ManyToManyField(
        Providedservices,
        through='RepairsessionsProvidedservices',
        help_text="Оберіть один або більше варантів (Потрібно зажати Ctrl або Cmd при натисканні на обʼєкт для вибору декількох варіантів)"
    )

    class Meta:
        db_table = 'repairsessions'
        ordering = ['id']
    
    def __str__(self):
        return f'Замовлення: {self.order_number} | '\
                f'Чи виконано: {self.if_finished} | Несправності: {self.malfunctions} | '\
                f'Авто: {self.vehicle.brand}({self.vehicle.id}) | Клієнт: {self.vehicle.client.name} | '\
                f'Майстер: {self.master.name}({self.master.id})'
    
    def natural_key(self):
        return f"{self.id} | {self.order_number} | {self.if_finished}"


class RepairsessionsProvidedservices(models.Model):
    repair_session = models.OneToOneField(Repairsessions, on_delete=models.CASCADE, primary_key=True)  # The composite primary key (repair_session_id, provided_service_id) found, that is not supported. The first column is selected.
    provided_service = models.ForeignKey(Providedservices, on_delete=models.PROTECT)

    class Meta:
        db_table = 'repairsessions_providedservices'
        unique_together = (('repair_session_id', 'provided_service_id'),)


class RepairsessionsRepairparts(models.Model):
    repair_session = models.OneToOneField(Repairsessions, on_delete=models.PROTECT, primary_key=True)  # The composite primary key (repair_session_id, repair_part_id) found, that is not supported. The first column is selected.
    repair_part = models.ForeignKey(Repairparts, on_delete=models.PROTECT)
    amount = models.IntegerField()

    class Meta:
        db_table = 'repairsessions_repairparts'
        unique_together = (('repair_session_id', 'repair_part_id'),)

