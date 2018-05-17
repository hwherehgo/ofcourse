
from django.core.cache import cache
from .models import Post
from common import rds



def page_cache(time1):
    def inner1(func):
        def inner2(request):
            key='View_{}_{}'.format(request.get_full_path(),request.session.session_key)
            response = cache.get(key)
            if response is None:
                response = func(request)
                cache.set(key,response,time1)
            return response

        return inner2
    return inner1


def read_count(func):
    def inner(request):

        response=func(request)
        if response.status_code<=300:
            post_id = request.GET.get('post_id')
            rds.zincrby('readcount',post_id)
    return inner



def get_top_n(n):

    ##进制类型转换程int
    ori_data = rds.revzrange('readcount',0,n-1,withscores=True)
    # [(b'21',39)]
    rank_data = [[int(m),int(n)] for m,n in ori_data]
    # [[21,39]] 这个是正确的顺序
    post_id_list = [mm for mm,_ in rank_data]

    #这个是不正确的顺序  需要排序
    postsobj = Post.objects.get(id__in=post_id_list)

    postsobj = sorted(postsobj,key = lambda item:post_id_list.index(item.id))

    for mmm,nnn in zip(rank_data,postsobj):
        mmm[0] = nnn

    return rank_data







