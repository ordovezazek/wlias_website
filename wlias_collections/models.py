from __future__ import unicode_literals
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.search import index

from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core.models import Page, Orderable, Collection
from wagtail.core.fields import RichTextField, StreamField

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
 
from wagtail.core import blocks
from django_extensions.db.fields import AutoSlugField

from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    PageChooserPanel,
    MultiFieldPanel,
    StreamFieldPanel,
)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from wagtail.search.models import Query


class CollectionsPage(Page):

    template = "collections/collections.html"

    subpage_types = ['wlias_collections.CollectionPageSpecific']

    max_count = 1

    content_panels = Page.content_panels + [

    ]

    def child_pages(self):
        return CollectionPageSpecific.objects.live().child_of(self)

    def children(self):
        return self.get_children().specific().live()

    def get_collections(self):
        return CollectionPageSpecific.objects.live().descendant_of(self) 

    def paginate(self, request, *args):
        page = request.GET.get('page')
        collections = args[0]
        search_query = args[1]
        if search_query:
            collections = collections.search(search_query)

            # Log the query so Wagtail can suggest promoted results
            Query.get(search_query).add_hit()

        paginator = Paginator(collections, 4)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages


    def get_context(self, request):
        search_query = request.GET.get('search', None)
        context = super(CollectionsPage, self).get_context(request)
        context['collections'] = self.paginate(request, self.get_collections(), search_query)

        return context


    #sets slug
    def full_clean(self, *args, **kwargs):
        # super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('collections'):
            self.slug = 'collections'

    class Meta:
        # abstract = True
        verbose_name = "Collections Page"


# class CollectionAreaOrderable(Orderable):
    
#     page = ParentalKey("wlias_collections.CollectionPageSpecific", related_name="collections")
#     collection = models.ForeignKey(
#         "wlias_collections.Collection",
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True
#     )

#     panels = [
#         SnippetChooserPanel("collection"),
#     ]

class CollectionPageSpecific(Page):
    template = "collections/collections_specific.html"

    # collection_color = models.CharField(max_length=100, blank=True)
    

    collection = models.ForeignKey(
        "wlias_collections.Collection",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Collection"
    )

    content_panels = Page.content_panels + [
        
        # FieldPanel("collection_color"),

        MultiFieldPanel(
                [
                    SnippetChooserPanel("collection")
                ],
                heading="Assign Collection",
        ),

    ]

class Collection(ClusterableModel):
    collection_name = models.CharField(max_length=100, blank=True)
    collection_color = models.CharField(max_length=100, blank=True)
    description = RichTextField(blank=True,)
    designs_section_title = models.CharField(max_length=100, blank=True, verbose_name="Design Section Title")

    display = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Page Display"
    )

    mobile_display = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Mobile Page Display"
    )

    thumbnail = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    panels = [
 
        
        MultiFieldPanel(
                    [
                        FieldPanel("collection_name"),
                        FieldPanel("collection_color"),
                        FieldPanel("description"),
                        FieldPanel("designs_section_title"),
                    ],
                    heading="Collection Details",
            ),

        MultiFieldPanel(
                    [
                        ImageChooserPanel('display'),
                        ImageChooserPanel('mobile_display'),
                        ImageChooserPanel("thumbnail"),
                    ],
                    heading="Collection Visuals",
            ),

        MultiFieldPanel(
                    [
                        InlinePanel("artists", label="Artist", min_num=1, max_num=100)
                    ],
                    heading="Artists",
            ),

    ]

    @property
    def link(self):
        if self.order_link:
            return self.order_link
        return '#'

    def __str__(self):
        return self.collection_name
    class Meta:
        # abstract = True
        verbose_name = "Collection"
        verbose_name_plural = "Collections"

register_snippet(Collection)

class CollectionPageOrderable(Orderable):
    
    page = ParentalKey("wlias_collections.Collection", related_name="artists")
    artist = models.ForeignKey(
        "artists.Artist",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    panels = [
        SnippetChooserPanel("artist"),
    ]

# class CollectionPageOrderable(Orderable):
    
#     page = ParentalKey("wlias_collections.Collection", related_name="designs")
#     product = models.ForeignKey(
#         "artists.Design",
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True
#     )

#     panels = [
#         SnippetChooserPanel("product"),
#     ]