from django.db import models


class Payment(models.Model):
    payment_id = models.PositiveBigIntegerField(unique=True)
    order_id = models.PositiveBigIntegerField(unique=True)
    user_id = models.PositiveBigIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=50)
    payment_gateway = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(
            f"Payment {self.transaction_id} - "
            "{self.amount} {self.currency} ({self.status})"
        )


class Refund(models.Model):
    payment = models.ForeignKey(Payment, related_name="refunds", on_delete=models.CASCADE)
    refund_id = models.CharField(max_length=255, unique=True)
    refund_status = models.CharField(max_length=10)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_refund_at = models.DateTimeField(null=True, blank=True)
    is_refunded = models.BooleanField(default=False)

    def __str__(self):
        return f"Refund {self.refund_id} - {self.refund_amount} {self.payment.currency}"
