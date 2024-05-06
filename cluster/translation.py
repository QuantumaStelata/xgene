from modeltranslation.translator import TranslationOptions, register

from apps.directory.models import Tank


@register(Tank)
class TankTranslationOptions(TranslationOptions):
    fields = ('name',)
