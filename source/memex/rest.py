from rest_framework import routers, serializers, viewsets, parsers

from base.models import Project
from apps.crawl_space.models import Crawl, CrawlModel


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ("name", "description")


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CrawlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crawl
        fields = (
            "name",
            "description",
            "crawler",
            "seeds_list",
            "project",
            "crawl_model",
            "rounds_left"
        )


class CrawlViewSet(viewsets.ModelViewSet):
    parser_classes = (parsers.FileUploadParser,)
    queryset = Crawl.objects.all()
    serializer_class = CrawlSerializer


class CrawlModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CrawlModel
        fields = (
            "name",
            "model",
            "features",
            "project"
        )


class CrawlModelViewSet(viewsets.ModelViewSet):
    parser_classes = (parsers.FileUploadParser,)
    queryset = CrawlModel.objects.all()
    serializer_class = CrawlModelSerializer


router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"crawls", CrawlViewSet)
router.register(r"crawl_models", CrawlModelViewSet)
