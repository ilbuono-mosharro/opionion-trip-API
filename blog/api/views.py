from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly, IsSafeMethod, IsOwner
from .serializers import PostSerializer, CommentSerializer
from ..models import Post, Comment


class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], url_path='comments', url_name='get_comments_by_post',
            permission_classes=[IsSafeMethod])
    def get_comments_by_post(self, request, *args, **kwargs):
        post = self.get_object()
        queryset = post.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='create-comment', url_name='create_comment',
            permission_classes=[permissions.IsAuthenticated])
    def create_comment(self, request, pk=None, *args, **kwargs):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path="author-posts", url_name="author_posts",
            permission_classes=[permissions.IsAuthenticated, IsOwner])
    def author_posts(self, request, *args, **kwargs):
        user = request.user
        posts = Post.objects.filter(author=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    allowed_methods = ['get', 'put', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(author=user)
