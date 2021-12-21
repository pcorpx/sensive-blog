def index(request):
    most_popular_posts = (Post.objects.popular()[:5]
        .prefetch_related('author')
        .fetch_with_comments_count()
    )
    fresh_posts = (Post.objects.prefetch_related('author')
        .annotate(comments_count=Count('comments'))
        .order_by('-published_at'))
    most_fresh_posts = fresh_posts[:5]

    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        'most_popular_posts': [
            serialize_post_optimized(post) for post in most_popular_posts
        ],
        'page_posts': [
            serialize_post_optimized(post) for post in most_fresh_posts
        ],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)
