import logging

import pytest
from rdflib import OWL, RDF, RDFS, Graph, Literal, URIRef
from rdflib.compare import to_isomorphic

from laconia import ThingFactory

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def store():
    g = Graph()
    g.bind("rf", "http://rossfenning.co.uk/#")
    g.bind("foaf", "http://xmlns.com/foaf/0.1/")
    g.bind("rdf", RDF)
    g.bind("owl", OWL)
    return g


@pytest.fixture
def factory(store):
    return ThingFactory(store)


def test_creates_entity_with_type(factory):
    ross = factory("rf_me")
    ross.rdf_type.add(factory("foaf_Person"))

    expected = Graph()
    expected.add(
        (
            URIRef("http://rossfenning.co.uk/#me"),
            URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
            URIRef("http://xmlns.com/foaf/0.1/Person"),
        )
    )

    assert to_isomorphic(factory.store) == to_isomorphic(expected)


def test_uses_alias(factory):
    factory.addAlias(
        "favourite_cheese", "http://rossfenning.co.uk/#favourite-cheese"
    )

    ross = factory("rf_me")
    ross.favourite_cheese.add("Stinking Bishop")

    expected = Graph()
    expected.add(
        (
            URIRef("http://rossfenning.co.uk/#me"),
            URIRef("http://rossfenning.co.uk/#favourite-cheese"),
            Literal("Stinking Bishop"),
        )
    )

    assert to_isomorphic(factory.store) == to_isomorphic(expected)


def test_adds_props_during_construction(store):
    factory = ThingFactory(store)

    # We must use a list for the value as name is not a functional property (can only have one value)
    _ = factory("rf_me", foaf_name=["Ross Fenning"])

    expected = Graph()
    expected.add(
        (
            URIRef("http://rossfenning.co.uk/#me"),
            URIRef("http://xmlns.com/foaf/0.1/name"),
            Literal("Ross Fenning"),
        )
    )

    assert to_isomorphic(store) == to_isomorphic(expected)


def test_adds_unique_prop_during_construction(store):
    # Add the FOAF schema
    store.parse("foaf.rdf")
    factory = ThingFactory(store)

    # The FOAF schema tells us gender has only one value (we don't need to use a list)
    ross = factory("rf_me", foaf_gender="male")

    assert str(ross.foaf_gender) == "male"


def test_rejects_attempts_to_access_unknown_private_attributes(factory):
    ross = factory("rf_me")
    with pytest.raises(AttributeError):
        ross._badger


def test_attribute_error_when_asking_for_unique_property_without_value(
    factory,
):
    ross = factory("rf_me")
    factory.store.parse("foaf.rdf")
    with pytest.raises(AttributeError):
        ross.foaf_birthday


def test_setting_property_with_set(factory):
    ross = factory("rf_me")
    ross.foaf_myersBriggs = {"ENTP"}
    assert "ENTP" in ross.foaf_myersBriggs


def test_rejects_setting_properties_as_weird_things(factory):
    ross = factory("rf_me")
    with pytest.raises(TypeError):
        ross.rf_dict = dict(this_will="fail")


def test_allows_setting_and_deleting_of_private_attributes(factory):
    ross = factory("rf_me")
    ross._badger = "foo"
    assert ross._badger == "foo"
    del ross._badger
    with pytest.raises(AttributeError):
        ross._badger


def test_allows_deleting_of_properties(factory):
    ross = factory("rf_me")

    ross.foaf_name.add("Ross Fenning")
    assert "Ross Fenning" in ross.foaf_name

    del ross.foaf_name
    assert "Ross Fenning" not in ross.foaf_name


def test_allows_deleting_of_properties_with_multiple_values(factory):
    ross = factory("rf_me")

    ross.foaf_name.add("Ross Fenning")
    ross.foaf_name.add("Miguel Sanchez")
    assert "Ross Fenning" in ross.foaf_name
    assert "Miguel Sanchez" in ross.foaf_name

    del ross.foaf_name
    assert "Ross Fenning" not in ross.foaf_name
    assert "Miguel Sanchez" not in ross.foaf_name


def test_setting_list_property(factory):
    factory(
        "rf_todo",
        rdfs_range=[factory("rdf_List")],
        rdf_type=[factory("owl_FunctionalProperty")],
    )

    ross = factory("rf_me")
    ross.rf_todo = ["a", "b", "c"]

    assert ["a", "b", "c"] == ross.rf_todo


def test_setting_sequence_property(factory):
    factory(
        "rf_todo",
        rdfs_range=[factory("rdf_Seq")],
        rdf_type=[factory("owl_FunctionalProperty")],
    )

    ross = factory("rf_me")
    ross.rf_todo = ["a", "b", "c"]

    assert ["a", "b", "c"] == ross.rf_todo


def test_allows_setting_another_thing_as_attr_value(factory):
    ross = factory("rf_me")
    cheese = factory("http://dbpedia.org/Cheese")
    ross.rf_likes.add(cheese)

    assert cheese in ross.rf_likes


def test_allows_setting_another_thing_as_attr_value_even_when_stores_are_different(
    factory,
):
    ross = factory("rf_me")
    factory2 = ThingFactory(Graph())
    cheese = factory2("http://dbpedia.org/Cheese")
    ross.rf_likes.add(cheese)

    assert cheese in ross.rf_likes


def test_relating_things_with_different_stores_unifies_facts(factory):
    ross = factory("rf_me")

    factory2 = ThingFactory(Graph())
    cheese = factory2("http://dbpedia.org/Cheese")
    cheese.rdfs_label.add("Cheese")

    ross.rf_likes.add(cheese)

    # Fact about cheese copies into subject's store
    assert (
        URIRef("http://dbpedia.org/Cheese"),
        RDFS.label,
        Literal("Cheese"),
    ) in ross._store


def test_getting_single_valued_uri_object(store):
    store.parse("foaf.rdf")
    factory = ThingFactory(store)

    ross = factory("rf_me")
    male = factory("rf_gender_male")

    ross.foaf_gender = male

    assert str(ross.foaf_gender) == str(male)


def test_creating_anonymous_things(factory):
    logging.info("TEST:\t\tCreating Ross")
    ross = factory("rf_me")
    logging.info("TEST:\t\tCreating Cheese")
    cheese = factory()
    logging.info("TEST:\t\tCalling cheese, cheese")
    cheese.rdfs_label.add("Cheese")

    logging.info("TEST:\t\tSaying Ross likes cheese")
    ross.rf_likes.add(cheese)

    logging.info("TEST:\t\tChecking Ross likes cheese")
    assert "Cheese" in list(ross.rf_likes)[0].rdfs_label


def test_things_with_same_id_are_equal(factory):
    assert factory("rf_thing") == factory("rf_thing")


def test_things_with_different_ids_are_not_equal(factory):
    assert factory("rf_thing1") != factory("rf_thing2")


def test_things_equal_to_their_uriref(factory):
    uri = "http://rossfenning.co.uk/#thing"
    thing = factory(uri)

    assert thing == URIRef(uri)


def test_list_all_properties(factory):
    ross = factory("rf_me")
    ross.rdfs_label.add("Ross")
    ross.rf_likes.add("Cheese")

    assert set(ross.properties()) == {
        factory("rdfs_label"),
        factory("rf_likes"),
    }


def test_resource_set_copied_to_set(factory):
    ross = factory("rf_me")
    # Test both literals and objects just to exercise it a bit more
    ross.rf_likes.add("Beer")
    ross.rf_likes.add(factory("rf_Cheese"))

    # set() constructor should iterate using __iter__ to build up a set
    assert set(ross.rf_likes) == {factory("rf_Cheese"), "Beer"}


def test_assigning_resourceset_to_another_thing(factory):
    ross = factory("rf_me")
    ross.rf_likes.add("Beer")
    ross.rf_likes.add("Cheese")

    bill = factory("rf_Bill")
    # Bill likes all the things Ross likes
    bill.rf_likes = ross.rf_likes

    assert set(bill.rf_likes) == {"Beer", "Cheese"}


def test_removing_literal(factory):
    ross = factory("rf_me")
    ross.rf_likes.add("Beer")
    ross.rf_likes.add("Cheese")

    assert set(ross.rf_likes) == {"Beer", "Cheese"}

    ross.rf_likes.remove("Cheese")

    assert set(ross.rf_likes) == {"Beer"}


def test_removing_object(factory):
    ross = factory("rf_me")
    ross.rf_likes.add(factory("rf_Beer"))
    ross.rf_likes.add(factory("rf_Cheese"))

    assert set(ross.rf_likes) == {factory("rf_Beer"), factory("rf_Cheese")}

    ross.rf_likes.remove(factory("rf_Cheese"))

    assert set(ross.rf_likes) == {factory("rf_Beer")}


def test_keyerror_when_removing_nonexistant_object(factory):
    ross = factory("rf_me")

    with pytest.raises(KeyError):
        ross.rf_likes.remove("Coconut")


def test_inverse_properties(factory):
    john = factory("rf_John")
    janet = factory("rf_Janet")

    john.rf_likes.add(janet)
    assert john in janet.rf_likes_of
    assert len(janet.rf_likes_of) == 1

    janet.rf_likes_of.remove(john)
    assert john not in janet.rf_likes_of
    assert len(janet.rf_likes_of) == 0

    janet.rf_likes_of.add("Peter")
    assert "Peter" in janet.rf_likes_of
    assert len(janet.rf_likes_of) == 1


def test_filtering_for_one_language(factory):
    dog = factory("rf_dog")

    dog.rdfs_label.add("Dog", lang="en")
    dog.rdfs_label.add("Mutt", lang="en-gb")
    dog.rdfs_label.add("Chien", lang="fr")
    dog.rdfs_label.add("Pooch")

    assert set(dog.rdfs_label) == {"Dog", "Chien", "Pooch", "Mutt"}

    dog.lang = "en"
    assert set(dog.rdfs_label) == {"Dog", "Pooch", "Mutt"}

    dog.lang = "fr"
    assert set(dog.rdfs_label) == {"Chien", "Pooch"}

    dog.lang = "de"
    assert set(dog.rdfs_label) == {"Pooch"}
    assert dog.rdfs_label.any() == "Pooch"

    dog.lang = None
    assert set(dog.rdfs_label) == {"Dog", "Chien", "Pooch", "Mutt"}


def test_non_ascii(store):
    store.bind("schema", "http://schema.org/")
    store.parse("les-mis.ttl", format="turtle")

    factory = ThingFactory(store)
    film = factory(
        "http://dbpedia.org/resource/Les_Mis%C3%A9rables_(1935_film)"
    )
    film.lang = "en"
    assert set(film.schema_name) == {"Les Misérables (1935 film)"}


def test_hasattr_false_when_unknown_prefix_used(factory):
    mouse = factory("rf_mouse")
    assert hasattr(mouse, "unknown_attr") is False


def test_attribute_error_when_unknown_prefix_read(factory):
    mouse = factory("rf_mouse")
    with pytest.raises(AttributeError):
        mouse.unknown_attr


def test_attribute_error_when_unknown_prefix_written(factory):
    mouse = factory("rf_mouse")
    with pytest.raises(AttributeError):
        mouse.unknown_attr = "hello"
