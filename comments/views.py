from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from comments.models import post, comment, like
from django.contrib import messages
from login.models import userProfile

from django.contrib.auth.models import User, auth


@login_required(login_url='/login/login')
def create_post(request):
    print("hello")
    images = request.FILES.get('image')
    if request.method == 'POST':
        comments = []
        user_id = request.user.id
        content = request.POST['comment']
        posts = post.objects.create(user_id=user_id, image=images, content=content, comments=comments)
        posts.save()
        messages.success(request, "Your post created successfully")
        return redirect('welcome')
    else:
        return render(request, 'comments/create_post.html')
    return render(request, 'comments/create_post.html')


@login_required(login_url='/login/login')
def Show_user_post(request):
    user_id = request.user.id
    data = post.objects.filter(user_id=user_id)
    context = {'post_data': data}
    return render(request, 'comments/Show_user_post.html', context)


@login_required(login_url='/login/login')
def user_comment(request):
    if request.method == 'POST':
        user_comment = request.POST['user_comment']
        user_id = request.user.id
        post_id = request.POST['post_id']
        likes = []
        comments_data = comment.objects.create(user_id=user_id, messages=user_comment, likes=likes)
        commentlist = []
        postOldDetails = post.objects.filter(id=post_id).all()
        for pd in postOldDetails:
            for c in pd.comments:
                commentlist.append(c)
        commentlist.append(comments_data)
        postDetails = post.objects.get(id=post_id)
        postDetails.comments = commentlist
        postDetails.save()
        data = post.objects.filter(user_id=user_id)
        context = {'post_data': data}
        return redirect('welcome')
    else:
        return redirect('Show_user_post')
        return render(request, 'comments/Show_user_post.html')


@login_required(login_url='/login/login')
def show_post_comment(request):
    post_id = request.GET.get('id')
    post_comment_detail = post.objects.get(id=post_id)
    return render(request, 'comments/show_post_comment.html',
                  {'post_comment_detail': post_comment_detail, 'post_id': post_id})


@login_required(login_url='/login/login')
def comment_like(request):
    if request.method == 'POST':
        user_id = request.user.id
        comment_id = request.POST['comment_id']
        post_id = request.POST['post_id']
        if post.objects.filter(id=post_id).exists():
            postData = post.objects.get(id=post_id)
            postComments = postData.comments
            for i in range(0, len(postComments)):
                if int(comment_id) == postComments[i].comment_id:
                    if like.objects.filter(user=user_id, comment_id=int(comment_id)).exists():
                        for comment_data in postComments:
                            if comment_data.comment_id == int(comment_id):
                                for like_data in comment_data.likes:
                                    if like_data.user.id == int(user_id):
                                        comment_data.likes.pop(comment_data.likes.index(like_data))

                        postData.save()
                        likeData = like.objects.get(user=user_id, comment_id=int(comment_id))
                        likeData.delete()

                        comment_update = comment.objects.filter(comment_id=comment_id)
                        for data in comment_update:
                            comment_id = data.comment_id
                            no_of_like = data.no_of_like
                        DEFAULT_VALUE = 0
                        if no_of_like is None:
                            no_of_like = DEFAULT_VALUE

                       	no_of_like = no_of_like - 1
                        comment.objects.filter(comment_id=comment_id).update(no_of_like=no_of_like)

                        return HttpResponse(str(no_of_like))

                    else:
                        userObj = User.objects.get(id=user_id)
                        comment_update = comment.objects.filter(comment_id=comment_id)
                        for data in comment_update:
                            comment_id = data.comment_id
                            no_of_like = data.no_of_like
                        DEFAULT_VALUE = 0
                        if no_of_like is None:
                            no_of_like = DEFAULT_VALUE
                        no_of_like = no_of_like + 1
                        comment.objects.filter(comment_id=comment_id).update(no_of_like=no_of_like)

                        lokeObj = like.objects.create(user=userObj, comment_id=comment_id)
                        likelist = []
                        postData.comments[i].likes = [lokeObj]
                        postData.save()
                        return HttpResponse(str(no_of_like))


def like_show(request):
    post_id = request.GET.get('post_id')
    like_data = like.objects.filter(post_id=post_id).order_by('-id')[:5]
    return render(request, 'comments/like_show.html', {'likes': like_data})
