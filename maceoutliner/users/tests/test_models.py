from test_plus.test import TestCase
from fiction_outlines.models import Outline, Series, Character, Location
from fiction_outlines.models import CharacterInstance, LocationInstance, StoryElementNode


class TestUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test__str__(self):
        self.assertEqual(
            self.user.__str__(),
            'testuser'  # This is the default username for self.make_user()
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.user.get_absolute_url(),
            '/users/testuser/'
        )


class TestRecentChangeFeed(TestCase):
    '''
    Test the retrieval of recent changes made by a user.
    '''

    def setUp(self):

        def get_sn(node_id):
            return StoryElementNode.objects.get(pk=node_id)
        self.user = self.make_user('u1')
        self.s1 = Series.objects.create(title='Urban Fantasy Trilogy', user=self.user)
        self.c1 = Character.objects.create(name='John Doe', user=self.user)
        self.c1.series.add(self.s1)
        self.c2 = Character.objects.create(name='Mary Sue', user=self.user)
        self.c2.series.add(self.s1)
        self.l1 = Location.objects.create(name='The bar', user=self.user)
        self.l1.series.add(self.s1)
        self.o1 = Outline.objects.create(title='Dark Embrace', user=self.user, series=self.s1)
        self.c1int = CharacterInstance.objects.create(character=self.c1, outline=self.o1)
        self.l1int = LocationInstance.objects.create(location=self.l1, outline=self.o1)
        self.arc1 = self.o1.create_arc(name='Coming of age', mace_type='character')
        self.arc2 = self.o1.create_arc(name='Dragon invasion', mace_type='event')
        self.part1 = self.o1.story_tree_root.add_child(name='Part 1', story_element_type='part')
        self.part2 = get_sn(self.o1.story_tree_root.pk).add_child(name='Part 2', story_element_type='part')
        self.c2.description = "Good at everything she does."
        self.c2.save()
        self.chap1 = self.part1.add_child(name='Chapter 1', story_element_type='chapter')
        self.part1.refresh_from_db()  # Make sure we have the treebeard changes.
        self.c1int.main_character = True
        self.c1int.save()
        self.o1.description = "Sexy vampires in the city"
        self.o1.save()
        self.hook = self.arc1.arc_root_node.get_children()[0]
        self.hook.description = "Our hero walks alone in the rain."
        self.hook.save()
        self.chap1.description = "The cold city..."
        self.chap1.save()
        self.l1.description = 'Dark, sticky, and reeks of poorly forgotten violence.'
        self.l1.save()

    def test_additions_list(self):
        '''
        Verify that the additions list is collected propery.
        '''
        additions_list = self.user.get_recent_additions(15)
        assert len(additions_list) == 15
        assert additions_list[0]['object'] == self.chap1
        assert additions_list[1]['object'] == self.part2
        assert additions_list[2]['object'] == self.part1
        assert additions_list[3]['object'] == self.arc2.arc_root_node.get_children()[6]
        assert additions_list[4]['object'] == self.arc2.arc_root_node.get_children()[5]
        assert additions_list[5]['object'] == self.arc2.arc_root_node.get_children()[4]
        assert additions_list[6]['object'] == self.arc2.arc_root_node.get_children()[3]
        assert additions_list[7]['object'] == self.arc2.arc_root_node.get_children()[2]
        assert additions_list[8]['object'] == self.arc2.arc_root_node.get_children()[1]
        assert additions_list[9]['object'] == self.arc2.arc_root_node.get_children()[0]
        assert additions_list[10]['object'] == self.arc2
        assert additions_list[11]['object'] == self.arc1.arc_root_node.get_children()[6]
        assert additions_list[12]['object'] == self.arc1.arc_root_node.get_children()[5]
        assert additions_list[13]['object'] == self.arc1.arc_root_node.get_children()[4]
        assert additions_list[14]['object'] == self.arc1.arc_root_node.get_children()[3]

    def test_edits_list(self):
        '''
        Verify that edits are retrieved correctly and in the right order.
        '''
        edits_list = self.user.get_recent_edits(15)
        print(edits_list)
        for edit in edits_list:
            print("{0}: created({1}), modifed({2})".format(edit['object'],
                                                           edit['object'].created, edit['object'].modified))
        assert len(edits_list) == 8
        assert edits_list[0]['object'] == self.l1
        assert edits_list[1]['object'] == self.o1
        assert edits_list[2]['object'] == self.arc1
        assert edits_list[3]['object'] == self.c1int
        assert edits_list[4]['object'] == self.c2
        assert edits_list[5]['object'] == self.arc2
        assert edits_list[6]['object'] == self.c1
        assert edits_list[7]['object'] == self.s1

    def test_combined_list(self):
        '''
        Verify that combined list is joined and sorted correctly.
        '''
        all_events = self.user.get_all_recent_changes(15)
        assert len(all_events) == 15
        assert all_events[0]['object'] == self.l1
        assert all_events[0]['edit_type'] == 'edit'
        assert all_events[1]['object'] == self.o1
        assert all_events[1]['edit_type'] == 'edit'
        assert all_events[2]['object'] == self.arc1
        assert all_events[2]['edit_type'] == 'edit'
        assert all_events[3]['object'] == self.c1int
        assert all_events[3]['edit_type'] == 'edit'
        assert all_events[4]['object'] == self.chap1
        assert all_events[4]['edit_type'] == 'add'
        assert all_events[5]['object'] == self.c2
        assert all_events[5]['edit_type'] == 'edit'
        assert all_events[6]['object'] == self.part2
        assert all_events[6]['edit_type'] == 'add'
        assert all_events[7]['object'] == self.part1
        assert all_events[7]['edit_type'] == 'add'
        assert all_events[8]['object'] == self.arc2.arc_root_node.get_children()[6]
        assert all_events[8]['edit_type'] == 'add'
        assert all_events[9]['object'] == self.arc2.arc_root_node.get_children()[5]
        assert all_events[9]['edit_type'] == 'add'
        assert all_events[10]['object'] == self.arc2.arc_root_node.get_children()[4]
        assert all_events[10]['edit_type'] == 'add'
        assert all_events[11]['object'] == self.arc2.arc_root_node.get_children()[3]
        assert all_events[11]['edit_type'] == 'add'
        assert all_events[12]['object'] == self.arc2.arc_root_node.get_children()[2]
        assert all_events[12]['edit_type'] == 'add'
        assert all_events[13]['object'] == self.arc2.arc_root_node.get_children()[1]
        assert all_events[13]['edit_type'] == 'add'
        assert all_events[14]['object'] == self.arc2.arc_root_node.get_children()[0]
        assert all_events[14]['edit_type'] == 'add'
