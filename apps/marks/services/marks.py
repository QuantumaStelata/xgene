from apps.directory.models import Tank
from apps.marks.models import GunMark, Mastery
from generic.services.poliroid import PoliroidRequestService


class MarkService:
    @classmethod
    def update_gun_marks(cls):
        marks = []

        tanks = Tank.objects.all().values_list('id', 'external_id', named=True)
        tanks_mapped = {tank.external_id: tank.id for tank in tanks}

        data = PoliroidRequestService.get('gunmarks/api/eu/vehicles/20,30,40,50,55,60,65,70,75,80,85,90,95,100')
        for tank in data['data']:
            if tank['id'] not in tanks_mapped.keys():
                continue

            marks.append(
                GunMark(
                    tank_id=tanks_mapped[tank['id']],
                    mark_20=tank['marks']['20'],
                    mark_30=tank['marks']['30'],
                    mark_40=tank['marks']['40'],
                    mark_50=tank['marks']['50'],
                    mark_55=tank['marks']['55'],
                    mark_60=tank['marks']['60'],
                    mark_65=tank['marks']['65'],
                    mark_70=tank['marks']['70'],
                    mark_75=tank['marks']['75'],
                    mark_80=tank['marks']['80'],
                    mark_85=tank['marks']['85'],
                    mark_90=tank['marks']['90'],
                    mark_95=tank['marks']['95'],
                    mark_100=tank['marks']['100'],
                ),
            )

        return GunMark.objects.bulk_create(
            marks,
            update_conflicts=True,
            update_fields=[
                'mark_20', 'mark_30', 'mark_40', 'mark_50', 'mark_55', 'mark_60', 'mark_65',
                'mark_70', 'mark_75', 'mark_80', 'mark_85', 'mark_90', 'mark_95', 'mark_100',
            ],
            unique_fields=['tank_id'],
        )

    @classmethod
    def update_mastery(cls):
        masters = []

        tanks = Tank.objects.all().values_list('id', 'external_id', named=True)
        tanks_mapped = {tank.external_id: tank.id for tank in tanks}

        data = PoliroidRequestService.get('mastery/api/eu/vehicles')
        for tank in data['data']:
            if tank['id'] not in tanks_mapped.keys():
                continue

            masters.append(
                Mastery(
                    tank_id=tanks_mapped[tank['id']],
                    class_3=tank['mastery'][0],
                    class_2=tank['mastery'][1],
                    class_1=tank['mastery'][2],
                    master=tank['mastery'][3],
                ),
            )

        return Mastery.objects.bulk_create(
            masters,
            update_conflicts=True,
            update_fields=['class_3', 'class_2', 'class_1', 'master'],
            unique_fields=['tank_id'],
        )
