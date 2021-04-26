from django.db import models
from django.utils import timezone
from blog.models import User, Article

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    like_count = models.IntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    # 代表该评论回复的评论的引用，如果没有回复其他评论则为空
    quote_comment = models.ForeignKey(to='self', null=True, blank=True,
                                       on_delete=models.SET_NULL, related_name='sub_comments')

    # reply_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='usercomment')
    # # 类似于并查集，但这里直接记录祖先结点
    # ancestor = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.SET_NULL, related_name='posterity')
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content[:20]