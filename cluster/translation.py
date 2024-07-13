from modeltranslation.translator import TranslationOptions, register

from apps.directory.models import Map, ReserveType, Role, StrongholdBuildType, Tank
from apps.news.models import New, NewCategory


@register(Tank)
class TankTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(StrongholdBuildType)
class StrongholdBuildTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ReserveType)
class ReserveTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Role)
class RoleTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Map)
class MapTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(New)
class NewTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'link')


@register(NewCategory)
class NewCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
