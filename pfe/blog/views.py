
from django.shortcuts import render, get_object_or_404 , redirect 
from django.contrib.auth.decorators import login_required , user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Exists, OuterRef , Q , Prefetch
from .models import Post, Like, Comment , Follow , Notification , ReservationSeance
from authentification.models import CustomUser
from django.contrib import messages
from django.urls import reverse
import json
import mimetypes
from functools import wraps
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
import logging
from django.db import IntegrityError



logger = logging.getLogger(__name__)


def is_coach(user):
    return user.type_user == 'coach'

def membre_coach_admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.type_user in ['membre', 'coach', 'admin','moderateur']:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
            return redirect('homeglobal')  
    return _wrapped_view





def admin_check(user):
    return user.is_superuser


# links:
def is_active(request, path):
    return request.path.startswith(path)

@login_required
@membre_coach_admin_required
def home(request):
    authenticated_user = request.user
    followed_users = Follow.objects.filter(follower=authenticated_user).values_list('followed', flat=True)
    posts = Post.objects.filter(author__in=followed_users).annotate(
        user_has_liked=Exists(
            Like.objects.filter(post=OuterRef('pk'), user=authenticated_user)
        )
    ).prefetch_related(
        Prefetch('comments', queryset=Comment.objects.order_by('-created_at'), to_attr='all_comments')
    ).order_by('-created_at')

    for post in posts:
        post.latest_comments = post.all_comments[:2]

    return render(request, 'blog/home.html', {'posts': posts, 'authenticated_user': authenticated_user})


@membre_coach_admin_required
@login_required
def redirect_to_profile(request):
    if request.user.is_authenticated:
        return redirect('profile', userid=request.user.id)
    else:
        return redirect('login')


@membre_coach_admin_required
@login_required
def redirect_to_profile_status(request):
    if request.user.is_authenticated:
        return redirect('profile_status', userid=request.user.id)
    else:
        return redirect('login')


@membre_coach_admin_required
@login_required
def redirect_to_profile_media(request):
    if request.user.is_authenticated:
        return redirect('profile_media', userid=request.user.id)
    else:
        return redirect('login')


@membre_coach_admin_required
@login_required
def profile(request,userid):
    user = get_object_or_404(CustomUser, id=userid)
    authenticated_user = request.user
    followers=Follow.objects.filter(followed_id=userid).count()
    user.is_followed = Follow.objects.filter(follower=authenticated_user.id, followed=user.id).exists()
    posts = Post.objects.filter(author=user).annotate(
        user_has_liked=Exists(
            Like.objects.filter(post=OuterRef('pk'), user=authenticated_user)
        )
    ).order_by('-created_at') 
    for post in posts:
        post.latest_comments = post.comments.order_by('-created_at')[:2]

    profile_pic_post_id = user.get_profile_pic_post_id()
    couverture_pic_post_id = user.get_couverture_pic_post_id()    
    return render(request, 'blog/profile.html', {'user': user, 'posts': posts , 'authenticated_user':authenticated_user,'followers':followers,'profile_pic_post_id': profile_pic_post_id ,'couverture_pic_post_id': couverture_pic_post_id  # Ajoutez cette ligne
})

@membre_coach_admin_required
@login_required
def profile_status(request,userid):
    user = get_object_or_404(CustomUser, id=userid) #hada howa l user lli dakhel 3ndo , momkin nkon mshi ana amma dk l autenticated howa ana
    authenticated_user = request.user
    user.is_followed = Follow.objects.filter(follower=authenticated_user.id, followed=user.id).exists()
    
    posts = Post.objects.filter(
        author=user
    ).filter(
        Q(postimage__isnull=True) | Q(postimage='')
    ).annotate(
        user_has_liked=Exists(
            Like.objects.filter(post=OuterRef('pk'), user=authenticated_user)
        )
    ).order_by('-created_at')
    profile_pic_post_id = user.get_profile_pic_post_id()
    couverture_pic_post_id = user.get_couverture_pic_post_id()
    return render(request, 'blog/profile.html', {'user': user, 'posts': posts, 'authenticated_user':authenticated_user ,'couverture_pic_post_id': couverture_pic_post_id,
    'profile_pic_post_id': profile_pic_post_id ,'is_status_active': is_active(request, reverse('profile_status', args=[userid])),
})


@membre_coach_admin_required
@login_required
def profile_media(request,userid):
    user = get_object_or_404(CustomUser, id=userid)
    authenticated_user = request.user
    user.is_followed = Follow.objects.filter(follower=authenticated_user.id, followed=user.id).exists()

    posts = Post.objects.filter(
        author=user
    ).filter(
        ~Q(postimage__isnull=True) & ~Q(postimage='')
    ).annotate(
        user_has_liked=Exists(
            Like.objects.filter(post=OuterRef('pk'), user=user)
        )
    ).order_by('-created_at') 

    profile_pic_post_id = user.get_profile_pic_post_id()
    couverture_pic_post_id = user.get_couverture_pic_post_id()


    return render(request, 'blog/profile.html', {'user': user, 'posts': posts,'profile_pic_post_id': profile_pic_post_id  ,'authenticated_user':authenticated_user ,'couverture_pic_post_id': couverture_pic_post_id  ,       'is_media_active': is_active(request, reverse('profile_media', args=[userid])),
})



@membre_coach_admin_required
@login_required
@require_POST
def like_unlike_post(request,postuserid):
    user = request.user
    post_id = request.POST.get('post_id')
    post_obj = get_object_or_404(Post, id=post_id)
    user_post = get_object_or_404(CustomUser, id=postuserid)


    existing_like = Like.objects.filter(post=post_obj, user=user).first()

    if existing_like:
        existing_like.delete()
        liked = False
    else:
        Like.objects.create(post=post_obj, user=user)
        liked = True

        # if user.id != postuserid:
        if request.user.id != postuserid:
            Notification.objects.create(
                sender=request.user,
                recipient=user_post,
                notification_type='like',
                post=post_obj
            )

    data = {
        'liked': liked,
        'likes': post_obj.likes.count()
    }
    return JsonResponse(data)

@membre_coach_admin_required
@login_required
def add_post(request):
    if request.method == "POST":
        contente = request.POST.get('content')
        user = request.user.id
        postimagee = request.FILES.get('postimage')
       
        if not contente and not postimagee:
            messages.error(request, "You must include content or an image to create a post.")
            return redirect('profile', userid=user)
       
        if postimagee:
            mime_type, _ = mimetypes.guess_type(postimagee.name)
            if mime_type and mime_type.startswith('image'):
                media_type = 'photo'
            elif mime_type and mime_type.startswith('video'):
                media_type = 'video'
            else:
                messages.error(request, "The uploaded file must be an image or a video.")
                return redirect('profile', userid=user)
            
            file_path = postimagee.name
            if file_path.startswith('uploads/posts_image/'):
                file_path = file_path[len('uploads/posts_image/'):]
            postimagee.name = file_path
        else:
            media_type = 'photo' 
            file_path = None

        Post.objects.create(content=contente, author_id=user, postimage=postimagee, media_type=media_type)
        return redirect('profile', userid=user)
    else:
        return redirect('profile', userid=user)

    
@membre_coach_admin_required
@login_required
def delete_post(request, postid):
    post = get_object_or_404(Post, id=postid)
    user = request.user
    if request.method == 'POST':
        # nverifie wsh lpost contient image
        if post.postimage and post.postimage == user.photo_profil:
            other_posts = Post.objects.filter(postimage=user.photo_profil).exclude(id=postid)
            if not other_posts.exists():
                user.photo_profil = "uploads/photo_profil/photo_profil_default.jpg"
                user.save()

        if post.postimage and post.postimage == user.photo_couverture:
            other_posts = Post.objects.filter(postimage=user.photo_couverture).exclude(id=postid)
            if not other_posts.exists():
                user.photo_couverture = "uploads/photo_couverture/couv2.jpg"
                user.save()

        post.delete()
        messages.success(request, "Le post a été supprimé avec succès.")
    return redirect('profile', userid=user.id)


@membre_coach_admin_required
@login_required
def edit_post(request,postid):
    user=request.user.id
    post=get_object_or_404(Post,id=postid,author_id=user)
    if request.method == 'POST':
        contente=request.POST.get('content_edit')
        postimagee = request.FILES.get('postimagee')
        if not contente and not postimagee:
            messages.error(request, "You must include content or an image to create a post.")
            return redirect('profile',userid=user)
        
        if contente:
            post.content=contente
        if postimagee:
            post.postimage=postimagee
        post.save()
        messages.success(request, "Post updated successfully.")
        return redirect('profile',userid=user)
    
    return redirect('profile',userid=user)


@login_required
@require_POST
@membre_coach_admin_required
def add_comment(request, postuserid):
    post_id = request.POST.get('post_id')
    content = request.POST.get('content')
    user = get_object_or_404(CustomUser, id=postuserid)

    if not post_id or not content:
        return JsonResponse({'error': 'Post ID and content are required.'}, status=400)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post does not exist.'}, status=404)

    comment = Comment.objects.create(post=post, author=request.user, content=content)
    comments_count = post.comments.count() 
    if request.user.id != postuserid:
        Notification.objects.create(
            sender=request.user,
            recipient=user,
            notification_type='comment',
            post=post  
            )


    data = {
        'success': True,
        'comment_id': comment.id,
        'content': comment.content,
        'author': comment.author.username,
        'profilpic': comment.author.photo_profil.url,
        'created_at': comment.created_at.strftime("%B %d, %Y, %I:%M %p"),
        'comments_count': comments_count

    }
    return JsonResponse(data)

@login_required
@membre_coach_admin_required
def update_photo_prfl(request, postid):
    user = request.user

    if request.method == "POST":
        if 'profilimage' in request.FILES:
            user.photo_profil = request.FILES['profilimage']
            user.save()

            if postid != 0:  # verifi wsh deja 3do post
                post = get_object_or_404(Post, id=postid)
                post.delete()

            Post.objects.create(
                author=user,
                postimage=user.photo_profil
            )
            
            messages.success(request, "Votre photo de profil a été mise à jour et un nouveau post a été créé.")
        else:
            messages.error(request, "Veuillez sélectionner une image à télécharger.")
        
        return redirect('profile', userid=user.id)
    return redirect('profile', userid=user.id)


@login_required
@membre_coach_admin_required
def update_photo_couverture(request, postid):
    user = request.user

    if request.method == "POST":
        if 'couvertureimage' in request.FILES:
            user.photo_couverture = request.FILES['couvertureimage']
            user.save()

            if postid != 0:  #wsh deja 3do post
                post = get_object_or_404(Post, id=postid)
                post.delete()

            Post.objects.create(
                author=user,
                postimage=user.photo_couverture
            )
            
            messages.success(request, "Votre photo de couverture a été mise à jour et un nouveau post a été créé.")
        else:
            messages.error(request, "Veuillez sélectionner une image à télécharger.")
        
        return redirect('profile', userid=user.id)
    return redirect('profile', userid=user.id)

@membre_coach_admin_required
@login_required
def search_users(request):
    query = request.GET.get('q')
    authenticated_user = request.user
    results = CustomUser.objects.filter(username__icontains=query) if query else []
    
    for user in results:
        user.is_followed = Follow.objects.filter(follower=authenticated_user, followed=user).exists()
    
    return render(request, 'blog/search_results.html', {
        'results': results, 
        'query': query, 
        'authenticated_user': authenticated_user
    })



@login_required
@membre_coach_admin_required
def send_friend_request(request, username):
    authenticated_user = request.user
    user = get_object_or_404(CustomUser, username=username) #hada howa lfollowed howa lli l9ito blusername lli sifetto men search_results
    if Follow.objects.filter(follower=request.user, followed=user).exists():
        # wra aslan gha tla3 ya follow ya followed  , hadi z3ma kan khasni nderha ila ana deja mfollowih wtl3o lya follow 3wtani wkha rmymknsh y3wdo ytl3oha
        messages.info(request, "You are already followed him")
    else:
        Follow.objects.create(follower=request.user, followed=user)
        Notification.objects.create(
            sender=request.user,
            recipient=user,
            follow=Follow.objects.get(follower=request.user, followed=user),
            notification_type='follow'
        )
    
    redirect_tst = request.POST.get('salam')
    
    if redirect_tst is not None and redirect_tst != '':
        return redirect("profile", userid=redirect_tst)
    else:
        query = request.POST.get('query')
        return redirect(f"{reverse('search_users')}?q={query}")


@login_required
@membre_coach_admin_required
def cancel_friend_request(request , username):
    authenticated_user = request.user
    user = get_object_or_404(CustomUser, username=username) #hada howa lfollowed howa lli l9ito blusername lli sifetto men search_results
    follow=Follow.objects.filter(follower=authenticated_user,followed=user).first()
    
    if follow:
        follow.delete()
        # messages.info(request, "Request canceled successffully")
    else:
        # messages.info(request, "No friend request to cancel.")
        pass


    redirect_tst = request.POST.get('salam')
    
    if redirect_tst is not None and redirect_tst != '':
        return redirect("profile", userid=redirect_tst)
    else:
        query = request.POST.get('query')
        return redirect(f"{reverse('search_users')}?q={query}")
    # return redirect('search_users')

@login_required
@membre_coach_admin_required
def show_all_notifications(request):
    authenticated_user = request.user
    notifications=Notification.objects.filter(recipient_id=request.user.id).select_related('sender')
    # .values('id', 'notification_type', 'sender__username', 'post__id', 'created_at')
    return render(request,"blog/showallnotifications.html",{"notifications":notifications,"authenticated_user":authenticated_user})

    # nzid lblan dyal read




@login_required
@membre_coach_admin_required
def ajax_search_users(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter(Q(username__icontains=query))[:5]
    results = [
        {
            'id': user.id,
            'username': user.username,
            'photo_profil': user.photo_profil.url,
        }
        for user in users
    ]
    return JsonResponse({'results': results})




@membre_coach_admin_required
@login_required
def ajax_get_notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('sender', 'post').order_by('-created_at')[:5]

    unread_count = Notification.objects.filter(
        recipient=request.user, read=False
    ).count()

    notifications_data = []
    for notif in notifications:
        data = {
            'id': notif.id,
            'sender_id': notif.sender.id,
            'sender_username': notif.sender.username,
            'sender_photo': notif.sender.photo_profil.url,
            'created_at': notif.created_at.strftime("%B %d, %Y, %I:%M %p"),
            'read': notif.read,
            'notification_type': notif.notification_type,
        }

        if notif.notification_type == 'follow':
            data['message'] = 'followed you'
        elif notif.notification_type == 'like':
            data['message'] = 'liked your post'
            if notif.post:
                data['post_id'] = notif.post.id
            else:
                data['message'] = 'liked a post that no longer exists'
        elif notif.notification_type == 'comment':
            data['message'] = 'commented on your post'
            if notif.post:
                data['post_id'] = notif.post.id
            else:
                data['message'] = 'commented on a post that no longer exists'
        else:
            data['message'] = 'interacted with you'
        
        notifications_data.append(data)
    
    return JsonResponse({'notifications': notifications_data, 'unread_count': unread_count})



@membre_coach_admin_required
@login_required
@require_POST
def mark_notification_as_read(request):
    data = json.loads(request.body)
    notification_id = data.get('notification_id')
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)






@login_required
@membre_coach_admin_required
@require_POST
def mark_all_notifications_as_read(request):
    Notification.objects.filter(recipient=request.user, read=False).update(read=True)
    return JsonResponse({'success': True})






@membre_coach_admin_required
def view_post(request,postid):
    authenticated_user = request.user
    post = get_object_or_404(Post.objects.annotate(
        user_has_liked=Exists(
            Like.objects.filter(post=OuterRef('pk'), user=authenticated_user)
        )
    ), id=postid)

    # bsh nnakhod les derniers commentaires
    post.latest_comments = post.comments.order_by('-created_at')[:2]

    profile_pic = post.profile_pic.photo_profil if post.profile_pic else post.author.photo_profil


    
    return render(request, 'blog/post.html', {
        'post': post, 
        'authenticated_user': authenticated_user,
        'profile_pic': profile_pic,
          })



@login_required
def disponibilites_coach(request, coach_id):
    coach = get_object_or_404(CustomUser, id=coach_id, type_user='coach')
    authenticated_user = request.user
    aujourd_hui = timezone.now().date()
    fin_semaine = aujourd_hui + timedelta(days=7)

    if request.method == 'POST':
        date_str = request.POST.get('date')
        heure_str = request.POST.get('heure')
        commentaire = request.POST.get('commentaire', '')
        
        if date_str and heure_str and date_str.strip() and heure_str.strip():
            try:
                if ':' not in heure_str:
                    heure_str += ':00'
                
                date_debut = timezone.make_aware(datetime.strptime(f"{date_str} {heure_str}", "%Y-%m-%d %H:%M"))
                date_fin = date_debut + timedelta(hours=1)

                if ReservationSeance.objects.filter(coach=coach, date_debut=date_debut).exists():
                    messages.error(request, "Ce créneau n'est plus disponible.")
                else:
                    reservation = ReservationSeance(
                        coach=coach,
                        client=authenticated_user,
                        date_debut=date_debut,
                        date_fin=date_fin,
                        commentaire=commentaire,
                        statut='en attente'
                    )
                    try:
                        reservation.save()
                        messages.success(request, "Réservation effectuée avec succès.")
                        return redirect('profile', userid=coach.id)
                    except ValidationError as e:
                        messages.error(request, "Erreur lors de la réservation. Veuillez réessayer.")
                        return redirect('profile',  userid=request.user.id) #ici le prob
            except ValueError:
                messages.error(request, "Format de date ou d'heure invalide.")
        

    reservations = ReservationSeance.objects.filter(
        coach=coach,
        date_debut__gte=aujourd_hui,
        date_fin__lt=fin_semaine + timedelta(days=1)
    )

    disponibilites = {}
    for i in range(7):
        jour = aujourd_hui + timedelta(days=i)
        disponibilites[jour] = [
            heure for heure in range(8, 20)
            if not reservations.filter(
                date_debut__lte=timezone.make_aware(datetime.combine(jour, datetime.min.time()) + timedelta(hours=heure)),
                date_fin__gt=timezone.make_aware(datetime.combine(jour, datetime.min.time()) + timedelta(hours=heure))
            ).exists()
        ]

    heures = list(range(8, 20))

    return render(request, 'blog/dispo_coach.html', {
        'coach': coach,
        'disponibilites': disponibilites,
        'authenticated_user': authenticated_user,
        'heures': heures,
    })



@login_required
@user_passes_test(is_coach)
def coach_reservations(request):
    now = timezone.now()
    start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)

    reservations = ReservationSeance.objects.filter(coach=request.user ,date_debut__gte=start_of_today).order_by('date_debut')
    authenticated_user=request.user


    
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        action = request.POST.get('action')
        
        reservation = get_object_or_404(ReservationSeance, id=reservation_id, coach=request.user)
        
        if action == 'accept':
            reservation.statut = 'acceptee'
            messages.success(request, "Réservation acceptée avec succès.")
        elif action == 'refuse':
            reservation.statut = 'refusee'
            messages.success(request, "Réservation refusée avec succès.")
        
        reservation.save()
        return redirect('coach_reservations')

    return render(request, 'blog/coach_reservations.html', {'reservations': reservations , 'authenticated_user':authenticated_user})


@user_passes_test(lambda u: u.is_superuser)
def usersmanager(request):
    #nnakhod les useradminwlmod
    admin_mod_users = CustomUser.objects.filter(Q(is_superuser=True) | Q(groups__name='Moderateur')).distinct().order_by('-is_superuser', '-date_joined')
    authenticated_user=request.user

    regular_users = CustomUser.objects.filter(is_superuser=False).exclude(groups__name='Moderateur').order_by('-date_joined')
    
    users = list(admin_mod_users) + list(regular_users)
    
    return render(request, 'users_manager.html', {'users': users , 'authenticated_user':authenticated_user})


@user_passes_test(lambda u: u.is_superuser)
def ban_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f"User {user.username} has been banned.")
    return redirect('usersmanager')


@user_passes_test(lambda u: u.is_superuser)
def unban_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"User {user.username} has been unbanned.")
    return redirect('usersmanager')



def delete_user(request, user_id):
    try:
        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        messages.success(request, "L'utilisateur a été supprimé avec succès.")
    except IntegrityError as e:
        logger.error(f"Erreur d'intégrité lors de la suppression de l'utilisateur {user_id}: {str(e)}")
        messages.error(request, "Erreur lors de la suppression de l'utilisateur. Il pourrait être référencé ailleurs.")
    except Exception as e:
        logger.error(f"Erreur inattendue lors de la suppression de l'utilisateur {user_id}: {str(e)}")
        messages.error(request, "Une erreur inattendue s'est produite lors de la suppression de l'utilisateur.")
    
    return redirect('usersmanager')

