import logging
from operator import itemgetter
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db.models import Value, CharField, F
from fiction_outlines.models import TimeStampedModel
from fiction_outlines.models import (
    Series,
    Outline,
    Character,
    Location,
    Arc,
    ArcElementNode,
)
from fiction_outlines.models import (
    CharacterInstance,
    LocationInstance,
    StoryElementNode,
)

# With much gratitude to Simon Willison for providing this method:
# https://simonwillison.net/2018/Mar/25/combined-recent-additions/


logger = logging.getLogger("maceoutliner.users")


def combined_recent(limit, **kwargs):
    datetime_field = kwargs.pop("datetime_field", "created")
    querysets = []
    for key, queryset in kwargs.items():
        querysets.append(
            queryset.annotate(
                recent_changes_type=Value(key, output_field=CharField())
            ).values("pk", "recent_changes_type", datetime_field)
        )
    union_qs = querysets[0].union(*querysets[1:])
    records = []
    for row in union_qs.order_by("-{}".format(datetime_field))[:limit]:
        records.append(
            {
                "type": row["recent_changes_type"],
                "when": row[datetime_field],
                "pk": row["pk"],
            }
        )
    # Now we bulk-load each object type in turn
    to_load = {}
    for record in records:
        to_load.setdefault(record["type"], []).append(record["pk"])
    fetched = {}
    for key, pks in to_load.items():
        for item in kwargs[key].filter(pk__in=pks):
            fetched[(key, item.pk)] = item
    # Annotate 'records' with loaded objects
    for record in records:
        record["object"] = fetched[(record["type"], record["pk"])]
    return records


# recent = combined_recent(
#     20,
#     entry=Entry.objects.all(),
#     photo=Photo.objects.all(),
# )


@python_2_unicode_compatible
class User(TimeStampedModel, AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    display_name = models.CharField(
        _("Display Name"),
        blank=True,
        null=True,
        max_length=255,
        help_text=_("🎶 What's your name, son? ALEXANDER HAMILTON"),
    )
    bio = models.CharField(
        _("Bio"),
        blank=True,
        null=True,
        max_length=255,
        help_text=_("A few words about you."),
    )
    homepage_url = models.URLField(
        _("Homepage"), blank=True, null=True, help_text=_("Your home on the web.")
    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def prepare_history_query_set_dict(self, datetime_field="created"):
        query_set_dict = {
            "datetime_field": datetime_field,
            "series": Series.objects.all().prefetch_related("tags"),
            "characters": Character.objects.all().prefetch_related("tags", "series"),
            "locations": Location.objects.all().prefetch_related("tags", "series"),
            "outlines": Outline.objects.all()
            .select_related("series")
            .prefetch_related("tags", "arc_set", "storyelementnode_set"),
            "arcs": Arc.objects.all()
            .select_related("outline")
            .prefetch_related("arcelementnode_set"),
            "characterinstances": CharacterInstance.objects.filter(
                character__user=self
            ),
        }
        if datetime_field == "created":
            query_set_dict["locationinstances"] = LocationInstance.objects.filter(
                location__user=self
            )
            query_set_dict["storynodes"] = (
                StoryElementNode.objects.filter(outline__user=self)
                .select_related("outline")
                .prefetch_related(
                    "assoc_characters", "assoc_locations", "arcelementnode_set"
                )
                .exclude(story_element_type="root")
            )
            query_set_dict["arcnodes"] = (
                ArcElementNode.objects.filter(arc__outline__user=self)
                .select_related("story_element_node")
                .prefetch_related("assoc_characters", "assoc_locations")
                .exclude(arc_element_type="root")
            )
        return query_set_dict

    def get_recent_additions(self, num_results):
        """
        Fetch a list of recent additions or edits a user has made across the site.
        """
        query_set_dict = self.prepare_history_query_set_dict()
        return combined_recent(num_results, **query_set_dict)

    def get_recent_edits(self, num_results):
        """
        Fetch recent edits the user has made.
        """
        query_set_dict = self.prepare_history_query_set_dict(datetime_field="modified")
        for key, item in query_set_dict.items():
            if key != "datetime_field":
                query_set_dict[key] = item.exclude(created=F("modified"))
        return combined_recent(num_results, **query_set_dict)

    def get_all_recent_changes(self, num_results):
        """
        Fetch the results of recent additions and modifications,
        merge them, resort, and then return as a list of dicts.
        """
        additions = self.get_recent_additions(num_results)
        for item in additions:
            item.update({"edit_type": "add"})
        modifications = self.get_recent_edits(num_results)
        for item in modifications:
            item.update({"edit_type": "edit"})
        all_changes_unsorted = additions + modifications
        sorted_changes = sorted(
            all_changes_unsorted, key=itemgetter("when"), reverse=True
        )
        return sorted_changes[:num_results]


@receiver(post_save, sender=ArcElementNode)
def update_arc_modify_based_on_arc_node(sender, instance, created, *args, **kwargs):
    """
    If an ArcElement Node is edited after the initial addition to the arc, update
    the arc's last modified timestamp.
    """
    if not created:
        arc = instance.arc
        arc.modified = instance.modified
        arc.save()


@receiver(post_save, sender=StoryElementNode)
def update_outline_modify_based_on_story_node(
    sender, instance, created, *args, **kwargs
):
    """
    If a StoryElementNode is edited after the initial addition to the outline, update the outline's
    last modified timestamp.
    """
    if not created:
        outline = instance.outline
        outline.modified = instance.modified
        outline.save()
