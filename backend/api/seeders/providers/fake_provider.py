from faker.providers import BaseProvider
from django.utils import timezone
from api.models.course import Course
from api.models.project import Project
from api.models.group import Group
from authentication.models import User


class ModelProvider(BaseProvider):
    min_salt = 1
    max_salt = 100_000

    def fake_username(self, first_name: str, last_name: str) -> str:
        """Fake username for users"""
        rand = self.random_int(min=self.min_salt, max=self.max_salt)
        return f"{first_name.lower()}{last_name.lower()}{rand}"[:12]

    def fake_user(self, fake, id: int, staff_probability: float = 0.001) -> User:
        """Create a fake user"""
        return User(
            id=id,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            create_time=timezone.now(),
            last_enrolled=timezone.now().year,
            is_staff=fake.boolean(chance_of_getting_true=staff_probability)
        )

    def fake_course(self, fake, min_year=2022, max_year=2025) -> Course:
        """Create a fake course"""
        course = Course(
            name=fake.catch_phrase(),
            academic_startyear=fake.random_int(min=min_year, max=max_year),
            faculty=fake.real_faculty(),
            description=fake.paragraph()
        )

        return course

    def fake_project(self,
                     fake,
                     min_start_date_dev=-100,
                     max_start_date_dev=100,
                     min_deadline_dev=1,
                     max_deadline_dev=100,
                     visible_prob=80,
                     archived_prob=10,
                     score_visible_prob=30,
                     locked_groups_prob=30,
                     min_max_score=1,
                     max_max_score=100,
                     min_group_size=1,
                     max_group_size=15):
        """Create a fake project"""
        start_date = timezone.now() + timezone.timedelta(
            days=fake.random_int(min=min_start_date_dev, max=max_start_date_dev)
        )

        course = fake.real_course()

        return Project(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            visible=fake.boolean(chance_of_getting_true=visible_prob),
            archived=fake.boolean(chance_of_getting_true=archived_prob),
            score_visible=fake.boolean(chance_of_getting_true=score_visible_prob),
            locked_groups=fake.boolean(chance_of_getting_true=locked_groups_prob),
            deadline=start_date + timezone.timedelta(days=fake.random_int(min=min_deadline_dev, max=max_deadline_dev)),
            course=course,
            start_date=start_date,
            max_score=fake.random_int(min=min_max_score, max=max_max_score),
            group_size=fake.random_int(min=min_group_size, max=max_group_size)
        )

    def fake_group(self, fake, min_score: int = 0):
        """Create a fake group"""
        project: Project = fake.real_project()

        group: Group = Group(
            project=fake.real_project(),
            score=fake.random_int(min=min_score, max=project.max_score)
        )

        return group
