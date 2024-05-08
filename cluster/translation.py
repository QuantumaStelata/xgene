from modeltranslation.translator import TranslationOptions, register

from apps.directory.models import ReserveType, Role, StrongholdBuildType, Tank


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
