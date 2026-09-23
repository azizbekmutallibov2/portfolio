from django.core.management.base import BaseCommand

from apps.content.models import Project, ProjectTag, SiteSettings


class Command(BaseCommand):
    help = "Seed initial site content (idempotent)."

    def handle(self, *args, **options):
        SiteSettings.objects.get_or_create(pk=1)

        Project.objects.update_or_create(
            slug="tuitdorm",
            defaults={
                "title": "TuitDorm",
                "tag": ProjectTag.PRODUCTION,
                "problem": (
                    "TATU yotoqxonasida davomat qog'oz daftarlarda yuritilgan: sekin, "
                    "xatoga moyil, natijani tez ko'rib bo'lmaydi."
                ),
                "solution": (
                    "Yotoqxonani boshqarish uchun production-grade tizim: ma'lumotlar "
                    "PostgreSQL'da, ilova Nginx orqasida VPS'da ishlaydi."
                ),
                "role": "Arxitektura, backend va deployment — noldan o'zim.",
                "stack": "Django, PostgreSQL, Nginx",
                "repo_url": "",
                "demo_url": "",
                "order": 1,
                "is_published": True,
            },
        )

        Project.objects.update_or_create(
            slug="ozbekiston-kitobxonlari-jamiyati",
            defaults={
                "title": "O'zbekiston Kitobxonlari Jamiyati",
                "tag": ProjectTag.TEAM,
                "problem": "[TO'LDIRING: platforma qaysi ehtiyojni yopadi — 1–2 jumla]",
                "solution": (
                    "Backend Django REST'da, frontend Next.js (App Router)da. Django "
                    "loyihasi 13 ta ilovaga bo'lingan; biznes mantiq services va "
                    "selectors qatlamlarida (HackSoft yondashuvi)."
                ),
                "role": "[TO'LDIRING: siz qilgan qism]",
                "stack": "Django REST Framework, Next.js",
                "repo_url": "",
                "demo_url": "",
                "order": 2,
                "is_published": False,
            },
        )

        self.stdout.write(self.style.SUCCESS("Seed content applied."))
