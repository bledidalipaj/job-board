import factory


class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "jobs.Job"

    title = factory.Faker("job")
    link_to_apply = factory.Faker("url")
    remote = True
    description = factory.Faker("sentence")
    company = factory.Faker("company")
    company_website = factory.Faker("url")
    company_logo = factory.django.ImageField(color="blue")
    posted_by = factory.SubFactory("accounts.tests.factories.UserFactory")

