from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new super user"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
        ("parent", "Parent"),
        ("administrator", "Administrator"),
    ]
    role = models.CharField(max_length=13, choices=ROLE_CHOICES, default="student")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=10)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email


# Teacher Model
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subject = models.CharField(max_length=50)
    office_number = models.CharField(max_length=10)

    def __str__(self):
        return self.user.email


# Parent Model
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    children = models.ManyToManyField(Student, related_name="parents")

    def __str__(self):
        return self.user.email


# Administrator Model
class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email


# Payment Model
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[("paid", "Paid"), ("unpaid", "Unpaid"), ("late", "Late")],
    )

    def __str__(self):
        return f"{self.student.user.email} - {self.amount}"


# Installment Model
class Installment(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="installments"
    )
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    installment_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[("paid", "Paid"), ("unpaid", "Unpaid"), ("late", "Late")],
    )

    def __str__(self):
        return (
            f"{self.payment.student.user.email} - Installment {self.installment_amount}"
        )
