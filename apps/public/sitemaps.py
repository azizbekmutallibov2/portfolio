from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = "https"

    def items(self) -> list[str]:
        return ["public:home"]

    def location(self, item: str) -> str:
        return reverse(item)


sitemaps = {"static": StaticViewSitemap()}
