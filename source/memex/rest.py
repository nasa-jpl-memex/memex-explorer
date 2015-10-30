import shutil
import json

from rest_framework import routers, serializers, viewsets, parsers, filters
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from django.core.validators import URLValidator

from base.models import Project, SeedsList
from apps.crawl_space.models import Crawl, CrawlModel

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError


class DataWakeIndexUnavailable(APIException):
    status_code = 404
    default_detail = "The server failed to find the DataWake index in elasticsearch."


class SlugModelSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False, read_only=True)


class ProjectSerializer(SlugModelSerializer):
    url = serializers.CharField(read_only=True)

    class Meta:
        model = Project


class CrawlSerializer(SlugModelSerializer):
    # Expose these fields, but only as read only.
    id = serializers.ReadOnlyField()
    seeds_list = serializers.FileField(read_only=True, use_url=False)
    status = serializers.CharField(read_only=True)
    config = serializers.CharField(read_only=True)
    index_name = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    pages_crawled = serializers.IntegerField(read_only=True)
    harvest_rate = serializers.FloatField(read_only=True)
    location = serializers.CharField(read_only=True)

    def validate_crawler(self, value):
        if value == "ache" and not self.initial_data.get("crawl_model"):
            raise serializers.ValidationError("Ache crawls require a Crawl Model.")
        return value

    class Meta:
        model = Crawl


class CrawlModelSerializer(SlugModelSerializer):
    model = serializers.FileField(use_url=False)
    features = serializers.FileField(use_url=False)
    url = serializers.CharField(read_only=True)

    def validate_model(self, value):
        if value.name != "pageclassifier.model":
            raise serializers.ValidationError("File must be named pageclassifier.model")
        return value

    def validate_features(self, value):
        if value.name != "pageclassifier.features":
            raise serializers.ValidationError("File must be named pageclassifier.features")
        return value

    class Meta:
        model = CrawlModel


class SeedsListSerializer(SlugModelSerializer):
    url = serializers.CharField(read_only=True)
    file_string = serializers.CharField(read_only=True)

    def validate_seeds(self, value):
        try:
            seeds = json.loads(value)
        except ValueError:
            raise serializers.ValidationError("Seeds must be a JSON encoded string.")
        if type(seeds) != list:
            raise serializers.ValidationError("Seeds must be an array of URLs.")
        validator = URLValidator()
        errors = []
        for index, x in enumerate(seeds):
            try:
                validator(x)
            except ValidationError:
                # Add index to make it easier for CodeMirror to select the right
                # line.
                errors.append({index: x})
        if errors:
            errors.insert(0, "The seeds list contains invalid urls.")
            errors.append({"list": "\n".join(seeds)})
            raise serializers.ValidationError(errors)
        return value

    class Meta:
        model = SeedsList


"""
Viewset Classes.

Filtering is provided by django-filter.

Backend settings are in common_settings.py under REST_FRAMEWORK. Setting is:
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)

This backend is supplied to every viewset by default. Alter query fields by adding
or removing items from filter_fields
"""
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_fields = ('id', 'slug', 'name',)


class CrawlViewSet(viewsets.ModelViewSet):
    queryset = Crawl.objects.all()
    serializer_class = CrawlSerializer
    filter_fields = ('id', 'slug', 'name', 'description', 'status', 'project',
        'crawl_model', 'crawler', 'seeds_object')


class CrawlModelViewSet(viewsets.ModelViewSet):
    queryset = CrawlModel.objects.all()
    serializer_class = CrawlModelSerializer
    filter_fields = ('id', 'slug', 'name', 'project',)

    def destroy(self, request, pk=None):
        model = CrawlModel.objects.get(pk=pk)
        crawls = Crawl.objects.all().filter(crawl_model=pk)
        if crawls:
            message = "The Crawl Model is being used by the following Crawls and cannot be deleted: "
            raise serializers.ValidationError({
                "message": message,
                "errors": [x.name for x in crawls],
            })
        else:
            shutil.rmtree(model.get_model_path())
            return super(CrawlModelViewSet, self).destroy(request)


class SeedsListViewSet(viewsets.ModelViewSet):
    queryset = SeedsList.objects.all()
    serializer_class = SeedsListSerializer
    filter_fields = ('id', 'name', 'seeds', 'slug',)

    def create(self, request):
        # If a seeds file or a textseeds exists, then use those. Otherwise, look
        # for a string in request.data["seeds"]
        seeds_list = request.FILES.get("seeds", False)
        textseeds = request.data.get("textseeds", False)
        if seeds_list:
            request.data["seeds"] = json.dumps(map(str.strip, seeds_list.readlines()))
        elif textseeds:
            if type(textseeds) == unicode:
                request.data["seeds"] = json.dumps(map(unicode.strip, textseeds.split("\n")))
            # Get rid of carriage return character.
            elif type(textseeds) == str:
                request.data["seeds"] = json.dumps(map(str.strip, textseeds.split("\n")))
        return super(SeedsListViewSet, self).create(request)

    def destroy(self, request, pk=None):
        seeds = SeedsList.objects.get(pk=pk)
        crawls = Crawl.objects.all().filter(seeds_object=pk)
        if crawls:
            message = "The Seeds List is being used by the following Crawls and cannot be deleted: "
            raise serializers.ValidationError({
                "message": message,
                "errors": [x.name for x in crawls],
            })
        else:
            return super(SeedsListViewSet, self).destroy(request)


class DataWakeView(APIView):
    index = "datawake"
    es = Elasticsearch()

    def create_trails(self, trail_ids):
        trails = []
        for x in trail_ids:
            url_search = self.es.search(index=self.index, q="trail_id:%d" % x,
                fields="url", size=1000)["hits"]["hits"]
            new_trail = {"trail_id": x, "urls": [], "domain_name":url_search[0]["_type"]}
            for y in url_search:
                new_trail["urls"].append(y["fields"]["url"][0])
            new_trail.update({"urls_string": "\n".join(new_trail["urls"])})
            trails.append(new_trail)
        return trails

    def get(self, request, format=None):
        # TODO: catch all exception. At the very least, deal with 404 not found and
        # connection refused exceptions.
        # Temporarily remove exceptions for debugging.
        try:
            trail_ids = [x["key"] for x in self.es.search(index=self.index, body={
                "aggs" : {
                    "trail_id" : {
                        "terms" : { "field" : "trail_id" }
                    }
                }
            })["aggregations"]["trail_id"]["buckets"]]
            response = self.create_trails(trail_ids)
        except ConnectionError as e:
            raise OSError("Failed to connect to local elasticsearch instance.")
        except NotFoundError:
            raise DataWakeIndexUnavailable
        return Response(response)


router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"crawls", CrawlViewSet)
router.register(r"crawl_models", CrawlModelViewSet)
router.register(r"seeds_list", SeedsListViewSet)
