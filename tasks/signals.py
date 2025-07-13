from django.db.models.signals import m2m_changed,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.core.mail import EmailMessage, get_connection
from tasks.models import Task


@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        from django.core.mail import EmailMessage, get_connection

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_task_creation(sender, instance, action, **kwargs):
    if action == 'post_add':
        assigned_emails = [emp.email for emp in instance.assigned_to.all()]

        try:
            connection = get_connection(timeout=10)  # ⏱️ 10 সেকেন্ড টাইমআউট

            email = EmailMessage(
                subject='New Task Added',
                body=f"You have been assigned to the task: {instance.title}",
                from_email='asifraihan821@gmail.com',
                to=assigned_emails,
                connection=connection
            )

            email.send(fail_silently=False)

        except Exception as e:
            print(f"Email sending failed: {e}")


@receiver(post_delete, sender=Task)
def delete_associate_details(sender, instance, **kwargs):
     if instance.details:
          print(isinstance)
          instance.details.delete()

          print('deleted successfully')

