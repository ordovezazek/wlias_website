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

    max_count = 1

    #sets slug
    def full_clean(self, *args, **kwargs):
        # super(HomePage, self).full_clean(*args, **kwargs)

        if not self.slug.startswith('collections'):
            self.slug = 'collections'

    class Meta:
        # abstract = True
        verbose_name = "Collections Page"