from django.core.management.base import BaseCommand, CommandError
from ...models import Render


class Command(BaseCommand):
    help = 'Deletes output of all expired renders'

    def handle(self, *args, **options):
        pointer = 0
        batch_size = 1000
        qs = Render.objects.expired()

        while True:
            # Batch because Django just seems to consume loads of memory and lock up
            batch = qs.filter(id__gt=pointer).order_by('id')[:batch_size]
            if not batch:
                break
            for render in batch:
                pointer = render.id
                try:
                    render.delete_output()
                except FileNotFoundError:
                    print(f"❌  Render {render.id} already deleted", flush=True)
                else:
                    print(f"✅  Render {render.id} deleted", flush=True)
