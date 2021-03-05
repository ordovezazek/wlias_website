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
 

class ArtistCatalogue(Page):

    template = "artists/artists.html"

    max_count = 1

    content_panels = Page.content_panels + [

        MultiFieldPanel(
                [
                    InlinePanel("artists", label="Artist", min_num=1, max_num=100),
                ],
                heading="Artist Details",
        ),
    ]

    #sets slug
    def full_clean(self, *args, **kwargs):
        # super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('artists'):
            self.slug = 'artists'

    def get_context(self, request):
        context = super(ArtistCatalogue, self).get_context(request)
        context['artists'] = self.artists.all()

        return context

    class Meta:
        # abstract = True
        verbose_name = "Artists Page"

class ArtistAreaOrderable(Orderable):
    
    page = ParentalKey("artists.ArtistCatalogue", related_name="artists")
    artistDeets = models.ForeignKey(
        "artists.Artist",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel("artistDeets"),
    ]

class Artist(ClusterableModel):
    artist_name = models.CharField(max_length=100, blank=True,)
    social_link = models.CharField(max_length=1000, blank=True,)

    caption = models.CharField(max_length=1000, blank=True,)
    works = models.CharField(max_length=1000, blank=True,)
    boxcap = models.CharField(max_length=1000, blank=True,)

    profile = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name="Profile Picture (Sun)"
    )

    moon = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        related_name="+",
        verbose_name="Moon Picture"
    )
    mars = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Rising Picture"
    )
    jupiter = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Venus Picture"
    )

    panels = [

        MultiFieldPanel(
            [
                FieldPanel('artist_name'),
                FieldPanel('social_link'),


                FieldPanel('caption'),
                FieldPanel('works'),
                FieldPanel('boxcap'),
            ],
            heading="Artist Details",
        ),

        MultiFieldPanel(
            [
                ImageChooserPanel("profile"),
                ImageChooserPanel("moon"),
                ImageChooserPanel("mars"),
                ImageChooserPanel("jupiter"),
            ],
            heading="Artist Visuals",
        ),

        MultiFieldPanel(
            [
                InlinePanel("designs", label="Design", min_num=1, max_num=100),
            ],
            heading="Artist Designs",
        ),
    ]

    def __str__(self):
        return self.artist_name
    class Meta:
        # abstract = True
        verbose_name = "Artist"
        verbose_name_plural = "Artists"

register_snippet(Artist)

class StoreAreaOrderable(Orderable):
    
    page = ParentalKey("artists.Artist", related_name="designs")
    designDeets = models.ForeignKey(
        "artists.Design",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
 
    panels = [
        SnippetChooserPanel("designDeets"),
    ]

class Design(models.Model):
    design_name = models.CharField(max_length=100, blank=True, verbose_name="Design Title")
    creator = models.CharField(max_length=100, blank=True, verbose_name="Creator")
    story = RichTextField(blank=True,)
    description = RichTextField(blank=True,)
    price = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=100, blank=True,)
    order_status = models.CharField(max_length=1000, blank=True, verbose_name="Order Button Text")
    order_link = models.CharField(max_length=500, blank=True)
    form_embed_link = models.CharField(max_length=500, blank=True)
    form_height = models.CharField(max_length=500, blank=True)

    display = StreamField([
        ('image', ImageChooserBlock())
    ],
    blank=True,
    null=True,
    verbose_name="Display Images"
    )

    product = StreamField([
        ('image', ImageChooserBlock())
    ],
    blank=True,
    null=True,
    verbose_name="Product Images"
    )

    # product = models.ForeignKey(
    #     "wagtailimages.Image",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="+",
    #     verbose_name="Product Image"
    # )

    panels = [

        

        MultiFieldPanel(
                [
                    FieldPanel("design_name"),
                    FieldPanel("creator"),
                    FieldPanel("description"),
                    FieldPanel("story"),
                    
                ],
                heading="Design Details",
        ),

        MultiFieldPanel(
                [
                    StreamFieldPanel("display"),
                    StreamFieldPanel("product"),
                    
                ],
                heading="Design Visuals",
        ),
        

        MultiFieldPanel(
                [
                    FieldPanel('price'),
                    FieldPanel('currency'),
                    FieldPanel('order_status'),
                    FieldPanel('order_link'),
                    FieldPanel('form_embed_link'),
                    FieldPanel('form_height'),
                ],
                heading="Ordering Details",
        ),
        
        
        
    ]

    @property
    def link(self):
        if self.order_link:
            return self.order_link
        return '#'

    def __str__(self):
        return self.design_name
    class Meta:
        # abstract = True
        verbose_name = "Design"
        verbose_name_plural = "Designs"

register_snippet(Design)

