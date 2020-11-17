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

# from artists.models import 
 

class ShopPage(Page):
    template = 'shop/shop.html'

    max_count = 1

    collection = models.CharField(max_length=1000)

    content_panels = Page.content_panels + [

                
        MultiFieldPanel(
                [
                    FieldPanel("collection"),
                ],
                heading="Collection Heading",
        ),
        MultiFieldPanel(
                [
                    InlinePanel("designs", label="Products", min_num=1, max_num=100),
                ],
                heading="Shop Products",
        ),
    ]

    #sets slug
    def full_clean(self, *args, **kwargs):
        # super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('shop'):
            self.slug = 'shop'

    # def get_context(self, request):
    #     context = super(ShopPage, self).get_context(request)
    #     context['products'] = self.designs.all()

    #     return context

class ShopPageOrderable(Orderable):
    
    page = ParentalKey("shop.ShopPage", related_name="designs")
    product = models.ForeignKey(
        "artists.Design",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    panels = [
        SnippetChooserPanel("product"),
    ]
