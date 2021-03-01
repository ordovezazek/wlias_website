from django.db import models
 
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.search import index

from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from wagtail.core.models import Page, Orderable, Collection
from wagtail.core.fields import RichTextField, StreamField

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
 
from wagtail.core import blocks
from django_extensions.db.fields import AutoSlugField
from django.shortcuts import render

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

from artists.models import Design
 
class ShopPageOrderable(Orderable):
    
    page = ParentalKey("shop.ShopPage", related_name="collections")
    collection = models.ForeignKey(
        "wlias_collections.Collection",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    panels = [
        SnippetChooserPanel("collection"),
    ]

class ShopPage(Page):
    template = 'shop/shop.html'

    max_count = 1

    content_panels = Page.content_panels + [

        
        MultiFieldPanel(
                [
                    InlinePanel("collections", label="Collections", min_num=1, max_num=100)
                ],
                heading="Shop Collections",
        ),
    ]

    def child_pages(self):
        return ProductPageSpecific.objects.live().child_of(self)

    def children(self):
        return self.get_children().specific().live()

  
    #sets slug
    def full_clean(self, *args, **kwargs):
        # super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('shop'):
            self.slug = 'shop'


class ProductPageSpecific(Page):
    template = "artists/product_specific.html"

    product = models.ForeignKey(
        "artists.Design",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name= "Design"
    )

    # title = models.CharField(max_length=100, blank=True)
    # description = RichTextField(blank=True,)
    # thumbnail = models.ForeignKey(
    #     "wagtailimages.Image",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="+",
    # )

    content_panels = Page.content_panels + [
        
        # FieldPanel("title"),
        # FieldPanel("description"),
        # ImageChooserPanel("thumbnail"),

        MultiFieldPanel(
                [
                    SnippetChooserPanel("product")
                ],
                heading="Assign Design",
        ),

    ]


    #sets slug
    def full_clean(self, *args, **kwargs):
        # super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith(self.product.design_name):
            self.slug = self.product.design_name

