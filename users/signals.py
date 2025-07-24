from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site
from django.urls import reverse
from events.models import Event
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

User = get_user_model()

@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    if created and not instance.groups.filter(name__in=['Admin', 'Organizer']).exists():
        group, _ = Group.objects.get_or_create(name='Participant')
        instance.groups.add(group)

@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        current_site = Site.objects.get_current()
        domain = current_site.domain
        protocol = 'https' if current_site.id != 1 else 'http'
        activation_link = f"{protocol}://{domain}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}"

        subject = "Activate Your Event Manager Account"
        context = {
            'user': instance,
            'activation_link': activation_link,
        }

        html_content = render_to_string('users/activation_email.html', context)
        text_content = (
            f"Hi {instance.first_name or instance.username},\n\n"
            "Please activate your account by visiting the link below:\n"
            f"{activation_link}\n\n"
            "If you did not register, please ignore this email."
        )

        email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [instance.email])
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_notification(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            subject = f'RSVP Confirmation for {instance.name}'
            context = {
                'user': user,
                'event': instance,
            }
            html_content = render_to_string('users/rsvp_mail.html', context)
            text_content = (
                f"Hi {user.first_name or user.username},\n\n"
                f"You have successfully RSVPed to the event \"{instance.name}\" on {instance.date}."
            )

            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=True)
