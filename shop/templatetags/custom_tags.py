from django import template
# from ..models import Post
# from django.db.models import Count
# from django.utils.safestring import mark_safe
# import markdown


register = template.Library()

@register.filter
def ru_plural(value, variants):
    # фильтр для склонения в ед и множ числе
    variants = variants.split(',')
    value = abs(int(value))
    
    if value % 10 == 1 and value % 100 != 11:
        variant = 0
    elif value % 10 >= 2 and value % 10 <= 4 and (value % 100 < 10 or value % 100 >= 20):
        variant = 1
    else:
        variant = 2

    return variants[variant]


# @register.simple_tag
# def total_posts():
#     # количество постов
#     return Post.published.count()


# @register.inclusion_tag('blog/post/latest_post.html')
# def show_latest_posts(count=5):
#     # последние посты
#     latest_posts = Post.published.order_by('-publish')[:count]
#     return {'latest_posts': latest_posts}


# @register.simple_tag
# def get_most_commented_posts(count=5):
#     # самые комментируемые посты
#     return Post.published.annotate(
#         total_comments=Count('comments')
#     ).order_by('-total_comments')[:count]


# @register.filter(name='markdown')
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))