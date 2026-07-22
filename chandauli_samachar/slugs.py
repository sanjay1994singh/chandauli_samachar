import re
import unicodedata


def unicode_slugify(value, fallback="item"):
    """Create a URL slug while preserving Hindi matras and other Unicode marks."""
    value = unicodedata.normalize("NFKC", str(value)).lower().strip()
    output = []
    previous_was_separator = False

    for character in value:
        category = unicodedata.category(character)
        if category[0] in {"L", "N", "M"}:
            output.append(character)
            previous_was_separator = False
        elif character.isspace() or character in {"-", "_"}:
            if output and not previous_was_separator:
                output.append("-")
                previous_was_separator = True

    slug = "".join(output).strip("-")
    return re.sub(r"-+", "-", slug) or fallback


def unique_slug(instance, source, *, fallback="item", max_length=50, queryset=None):
    queryset = queryset if queryset is not None else type(instance).objects.all()
    queryset = queryset.exclude(pk=instance.pk)
    base = unicode_slugify(source, fallback=fallback)[:max_length].rstrip("-") or fallback
    candidate = base
    counter = 2

    while queryset.filter(slug=candidate).exists():
        suffix = f"-{counter}"
        candidate = f"{base[:max_length - len(suffix)].rstrip('-')}{suffix}"
        counter += 1

    return candidate
