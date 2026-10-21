from django.core.management.base import BaseCommand
from djangoapp.models import CarMake, CarModel
class Command(BaseCommand):
    help='Seed the educational car catalog idempotently'
    def handle(self,*args,**kwargs):
        for make,model,kind in [('Toyota','Camry','Sedan'),('Toyota','RAV4','SUV'),('Honda','Civic','Sedan'),('Ford','Escape','SUV')]:
            obj,_=CarMake.objects.get_or_create(name=make,defaults={'description':f'{make} automobiles'})
            CarModel.objects.get_or_create(car_make=obj,name=model,year=2023,defaults={'type':kind})
        self.stdout.write(self.style.SUCCESS('Car catalog ready'))
