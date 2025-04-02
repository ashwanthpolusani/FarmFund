from django.db import models
# Create your models here.

class Farm(models.Model):
    crop_name = models.CharField(max_length=100)
    farm_name = models.CharField(max_length=100)
    crop_description = models.TextField()
    crop_budget = models.IntegerField()
    
    def __str__(self):
        return self.crop_name
    
class Income(models.Model):
    farm= models.ForeignKey(Farm, on_delete=models.CASCADE)
    amount = models.IntegerField()
    details = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.date.strftime('%d-%m-%Y')
        return f"{formatted_date}  {self.details}, Rs.{self.amount}/-"
    
class Expenditure(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    amount = models.IntegerField()
    details = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        formatted_date = self.date.strftime('%d-%m-%Y')
        return f"{formatted_date}  {self.details}, Rs.{self.amount}/-"
