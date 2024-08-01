from django.db import models
from authentification.models import CustomUser
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Post(models.Model):
    content=models.TextField()
    postimage=models.ImageField(upload_to='uploads/posts_image/',null=True , blank=True)
    author=models.ForeignKey(CustomUser , related_name='posts' , on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    created_at=models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    profile_pic = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts_with_profile_pic')
    couverture_pic = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts_with_couverture_pic')
    media_type = models.CharField(max_length=10, choices=[('photo', 'Photo'), ('video', 'Video')], default='photo')
    def __str__(self):
        return f"Post by {self.author} on {self.created_at}"
    def user_has_liked(self, user):
        return self.likes.filter(user=user).exists()
class Comment(models.Model):
    content=models.TextField()
    post=models.ForeignKey(Post , related_name='comments' , on_delete=models.CASCADE)
    author=models.ForeignKey(CustomUser , related_name='comments' , on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    created_at=models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
class Like(models.Model):
    post=models.ForeignKey(Post , related_name='likes' , on_delete=models.CASCADE)
    user=models.ForeignKey(CustomUser , related_name='likes' , on_delete=models.CASCADE)
    value = models.CharField(max_length=10, choices=[('Like', 'Like'), ('Unlike', 'Unlike')], default='Like')
    created_at=models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"Like by {self.user} on {self.post}"
    
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser , related_name='following', on_delete=models.CASCADE) #lli followa
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE) #lli tfollowwa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower} follows {self.followed}"
class Notification(models.Model):
    sender = models.ForeignKey(CustomUser , related_name='sent_notifications', on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(CustomUser , related_name='notifications', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    # comment = models.ForeignKey(Comment, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    follow = models.ForeignKey(Follow, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=[
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
    ])
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient} - {self.notification_type}"
    

class ReservationSeance(models.Model):
    coach = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seances_coach')
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='seances_client')
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=[
        ('attente', 'en attente'),
        ('accepté', 'acceptee'),
        ('refusee', 'refusee'),
        ('terminee', 'terminee')
    ], default='en attente')
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Séance avec {self.coach.username} pour {self.client.username} le {self.date_debut}"

    class Meta:
        ordering = ['date_debut']
        verbose_name = "Réservation de séance"
        verbose_name_plural = "Réservations de séances"

    def clean(self):
        if self.coach.type_user != 'coach':
            raise ValidationError("L'utilisateur sélectionné comme coach n'est pas un coach.")
        if self.client.type_user == 'coach' or self.client.type_user == 'admin' or self.client.type_user == 'moderateur' :
            raise ValidationError("Un coach ne peut pas réserver une séance.")
        if self.date_debut >= self.date_fin:
            raise ValidationError("La date de début doit être antérieure à la date de fin.")
