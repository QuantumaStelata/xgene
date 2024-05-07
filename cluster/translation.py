from modeltranslation.translator import TranslationOptions, register

from apps.directory.models import StrongholdBuildType, Tank


@register(Tank)
class TankTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(StrongholdBuildType)
class StrongholdBuildTypeTranslationOptions(TranslationOptions):
    fields = ('name',)
