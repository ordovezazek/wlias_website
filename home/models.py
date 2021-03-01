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
    brandDescription = RichTextField(blank=True, verbose_name="Brand Description")
    serviceDescription = RichTextField(blank=True, verbose_name="Service Description")
    about_link = models.CharField(
        max_length=500,
        blank=True
    )

    section1 = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Section 1 (image)"
    )
    section1_mobile = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Section 1 Mobile (image)"
    )
    section2 = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Section 2 (image)"
    )

    invitation = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Invitation Message"
    )

    content_panels = Page.content_panels + [

        MultiFieldPanel(
            [
                ImageChooserPanel("section1"),
                ImageChooserPanel("section1_mobile"),
                ImageChooserPanel("section2"),
            ],
            heading="Home Page Display"
        ),
        FieldPanel('brandDescription'),
        FieldPanel('serviceDescription'),
        FieldPanel('invitation'),
        FieldPanel('about_link'),
    ]
        

        #sets slug to home
    def full_clean(self, *args, **kwargs):
        # super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('home'):
            self.slug = 'home'

    class Meta:
        # abstract = True
        verbose_name = "Home Page"
