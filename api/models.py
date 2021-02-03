from django.db import models

RATES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)


class Car(models.Model):
    make = models.CharField("Car make", max_length=100)
    model = models.CharField("Car model", max_length=100)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        ordering = ['make']
        unique_together = ('make', 'model',)


class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="rate_set")
    rate = models.PositiveIntegerField("Rate", choices=RATES)

    def __str__(self):
        return f"{self.car} {self.rate}"
