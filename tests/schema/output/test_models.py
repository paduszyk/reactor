from datetime import date

import pytest

from django.utils import translation


@pytest.mark.django_db
def test_article_str(baker):
    # Arrange.
    journal = baker.make(
        "publishers.Journal",
        abbreviation="J. Med. Chem.",
    )
    article = baker.make(
        "output.Article",
        title="Understanding the Impact of AI on Healthcare",
        journal=journal,
        year_published=2024,
        volume="4",
        issue="2",
        pagination="42-49",
    )
    author_1 = baker.make(
        "output.Author",
        alias="Doe, Joe Mark Anthony",
    )
    author_2 = baker.make(
        "output.Author",
        alias="Williams, Elizabeth Mary",
    )
    baker.make(
        "output.Contribution",
        order=1,
        author=author_1,
        work=article,
    )
    baker.make(
        "output.Contribution",
        order=2,
        author=author_2,
        work=article,
    )

    # Act.
    with translation.override("en"):
        article_str = str(article)

    # Assert.
    assert article_str == (
        "Doe J. M. A. and Williams E. M.: "
        "Understanding the Impact of AI on Healthcare. "
        "J. Med. Chem. 2024, vol. 4, no. 2, pp. 42-49."
    )


@pytest.mark.django_db
def test_book_str(baker):
    # Arrange.
    author_1 = baker.make(
        "output.Author",
        alias="Doe, Joe Mark Anthony",
    )
    author_2 = baker.make(
        "output.Author",
        alias="Williams, Elizabeth Mary",
    )
    author_3 = baker.make(
        "output.Author",
        alias="Smith, John",
    )
    publishing_house = baker.make(
        "publishers.PublishingHouse",
        name="Addison-Wesley",
    )
    book = baker.make(
        "output.Book",
        title="The Art of Computer Programming",
        year_published=1968,
        publishing_house=publishing_house,
    )
    baker.make(
        "output.Contribution",
        order=1,
        author=author_1,
        work=book,
    )
    baker.make(
        "output.Contribution",
        order=2,
        author=author_2,
        work=book,
    )
    baker.make(
        "output.Contribution",
        order=3,
        author=author_3,
        work=book,
    )

    # Act.
    with translation.override("en"):
        book_str = str(book)

    # Assert.
    assert book_str == (
        "Doe J. M. A., Williams E. M. and Smith J.: "
        "The Art of Computer Programming. Addison-Wesley, 1968."
    )


@pytest.mark.django_db
def test_chapter_str(baker):
    # Arrange.
    book_author_1 = baker.make(
        "output.Author",
        alias="Doe, Joe Mark Anthony",
    )
    book_author_2 = baker.make(
        "output.Author",
        alias="Williams, Elizabeth Mary",
    )
    book_author_3 = baker.make(
        "output.Author",
        alias="Smith, John",
    )
    publishing_house = baker.make(
        "publishers.PublishingHouse",
        name="Addison-Wesley",
    )
    book = baker.make(
        "output.Book",
        title="The Art of Computer Programming",
        year_published=1968,
        edited=True,
        publishing_house=publishing_house,
    )
    baker.make(
        "output.Contribution",
        order=1,
        author=book_author_1,
        work=book,
    )
    baker.make(
        "output.Contribution",
        order=2,
        author=book_author_2,
        work=book,
    )
    baker.make(
        "output.Contribution",
        order=3,
        author=book_author_3,
        work=book,
    )
    chapter = baker.make(
        "output.Chapter",
        title="Fundamental Algorithms",
        book=book,
        pagination="42-49",
    )
    chapter_author_1 = baker.make(
        "output.Author",
        alias="Smith, John",
    )
    chapter_author_2 = baker.make(
        "output.Author",
        alias="Johnson, Robert",
    )
    baker.make(
        "output.Contribution",
        order=1,
        author=chapter_author_1,
        work=chapter,
    )
    baker.make(
        "output.Contribution",
        order=2,
        author=chapter_author_2,
        work=chapter,
    )

    # Act.
    with translation.override("en"):
        chapter_str = str(chapter)

    # Assert.
    assert chapter_str == (
        "Smith J. and Johnson R.: Fundamental Algorithms. "
        "In: The Art of Computer Programming. "
        "Addison-Wesley, 1968. / Doe J. M. A., Williams E. M. and Smith J. (Eds.); "
        "pp. 42-49."
    )


@pytest.mark.django_db
def test_patent_str(baker):
    # Arrange.
    author_1 = baker.make(
        "output.Author",
        alias="Doe, Joe Mark Anthony",
    )
    author_2 = baker.make(
        "output.Author",
        alias="Williams, Elizabeth Mary",
    )
    patent = baker.make(
        "output.Patent",
        title="Method and System for Identifying a User",
        patent_number="US20200313G",
        date_applied=date(2017, 12, 21),
        date_granted=date(2020, 3, 13),
    )
    baker.make(
        "output.Contribution",
        order=1,
        author=author_1,
        work=patent,
    )
    baker.make(
        "output.Contribution",
        order=2,
        author=author_2,
        work=patent,
    )

    # Act.
    with translation.override("en"):
        patent_str = str(patent)

    # Assert.
    assert patent_str == (
        "Doe J. M. A. and Williams E. M.: Method and System for Identifying a User. "
        "Patent number: US20200313G. Applied on 2017-12-21, granted on 2020-03-13."
    )


@pytest.mark.django_db
def test_author_str(baker):
    # Arrange.
    author = baker.make(
        "output.Author",
        alias="Doe, Joe Mark Anthony",
    )

    # Act.
    author_str = str(author)

    # Assert.
    assert author_str == "Doe J. M. A."


@pytest.mark.django_db
def test_contribution_str(baker):
    # Arrange.
    article = baker.make(
        "output.Article",
        id=42,
    )
    author = baker.make(
        "output.Author",
        alias="Doe, Joe Mark Anthony",
    )
    contribution = baker.make(
        "output.Contribution",
        order=1,
        author=author,
        work=article,
    )

    # Act.
    with translation.override("en"):
        contribution_str = str(contribution)

    # Assert.
    assert contribution_str == "Doe J. M. A.: author no. 1 of article ID = 42"
