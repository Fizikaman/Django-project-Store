from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.urls import reverse
from urllib.parse import quote
from django.utils.timezone import now
from django.db import transaction

from store.settings import DEFAULT_FROM_EMAIL, DOMAIN_NAME



class User(AbstractUser):
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self) -> str:
        return f"Email Verification for {self.user.email}"
    
    def send_verification_email(self):
        link = reverse('user:email_verification', kwargs={'email':quote(self.user.email), 'code':self.code})
        verification_link = f"{DOMAIN_NAME}{link}"
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = "Для подтверждения учетной записи для {} перейдите по ссылке: {}".format(
            self.user.email,
            verification_link,
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return True if now() <= self.expiration else False