from django import template


register = template.Library()


@register.filter(name='liked')
def liked(post, user_id):
    liked = post.liked(user_id)
    return liked


@register.filter(name='follows')
def follows(user, profile):
    follows = user.follows(profile)
    return follows

