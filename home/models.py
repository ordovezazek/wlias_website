from django.db import models
 
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField

from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock

class HomePage(Page):
    template = 'home/landing.html'

    max_count = 1

    collection_name = models.TextField(null=True)

    section1 = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    section1_mobile = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    section2 = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    about = RichTextField()

    content_panels = Page.content_panels + [

        MultiFieldPanel(
            [
                FieldPanel("collection_name"),
                ImageChooserPanel("section1"),
                ImageChooserPanel("section1_mobile"),
                ImageChooserPanel("section2"),
                # ImageChooserPanel("img3"),
            ],
            heading="Frame 1"
        ),
        FieldPanel('about'),
    ]
        

        #sets slug to home
    def full_clean(self, *args, **kwargs):
        # super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('home'):
            self.slug = 'home'

    class Meta:
        # abstract = True
        verbose_name = "Home Page"
