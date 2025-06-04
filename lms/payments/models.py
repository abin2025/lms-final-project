from django.db import models

from students.models import BaseModelClass

# Create your models here.

class StatusChoices(models.TextChoices) :

    PENDING = 'pending','pending'

    SUCCESS = 'success','success'

    FAILED = 'failed','failed'

class Payments(BaseModelClass):

    student = models.ForeignKey('students.Students',on_delete=models.CASCADE)

    course = models.ForeignKey('course.Course',on_delete=models.CASCADE)

    amount = models.FloatField()

    status = models.CharField(max_length=15,choices=StatusChoices.choices,default=StatusChoices.PENDING)

    paid_at = models.DateTimeField(null=True,blank=True)

    def __str__(self):

        return f'{self.student.name}-{self.course.title}'

    class Meta:

        verbose_name = 'payments'

        verbose_name_plural ='payments' 

class Transaction(BaseModelClass):

    payment =models.ForeignKey('payments',on_delete = models.CASCADE)

    rzp_order_id = models.SlugField(null=True,blank=True)

    status = models.CharField(max_length =15,choices=StatusChoices.choices,default=StatusChoices.PENDING) 

    transaction_at = models.DateTimeField(null=True,blank=True)

    # rzp_payment_id = models.SlugField(null=True,blank=True)

    # rzp_payment_signature = models.TextField(null=True,blank=True)

    def __str__(self) :

        return f'{self.payment.student.name}-{self.course.title}-Transaction'


    class Meta:

        verbose_name = 'Transaction'

        verbose_name_plural = 'Transaction'        
