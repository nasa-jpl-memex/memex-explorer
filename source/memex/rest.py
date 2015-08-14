from rest_framework import routers, serializers, viewsets, parsers

from base.models import Project
from apps.crawl_space.models import Crawl, CrawlModel


class SlugModelSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, read_only=True)


class ProjectSerializer(SlugModelSerializer):
    class Meta:
        model = Project


class CrawlSerializer(SlugModelSerializer):
    seeds_list = serializers.FileField()
    crawler = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    config = serializers.CharField(read_only=True)
    index_name = serializers.CharField(read_only=True)
    pages_crawled = serializers.IntegerField(read_only=True)
    harvest_rate = serializers.FloatField(read_only=True)
    rounds_left = serializers.IntegerField(read_only=True)

    class Meta:
        model = Crawl
        fields = (
            "id",
            "project",
            "name",
            "description",
            "project",
            "seeds_list",
            "slug",
            "crawler",
            "status",
            "config",
            "pages_crawled",
            "harvest_rate",
            "rounds_left",
            "index_name"
        )


class CrawlModelSerializer(SlugModelSerializer):
    model = serializers.FileField()
    features = serializers.FileField()

    class Meta:
        model = CrawlModel


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CrawlViewSet(viewsets.ModelViewSet):
    parser_classes = (parsers.FileUploadParser,)
    queryset = Crawl.objects.all()
    serializer_class = CrawlSerializer


class CrawlModelViewSet(viewsets.ModelViewSet):
    parser_classes = (parsers.FileUploadParser,)
    queryset = CrawlModel.objects.all()
    serializer_class = CrawlModelSerializer


router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"crawls", CrawlViewSet)
router.register(r"crawl_models", CrawlModelViewSet)
