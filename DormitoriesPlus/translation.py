from modeltranslation.translator import register, TranslationOptions
from .models import Building, Room, InventoryTracking, Message, Request

@register(Building)
class BuildingTranslationOptions(TranslationOptions):
    fields = ('building_name',)

@register(Room)
class RoomTranslationOptions(TranslationOptions):
    fields = ('room_number', 'notes',)

@register(InventoryTracking)
class InventoryTrackingTranslationOptions(TranslationOptions):
    fields = ('item_name',)

@register(Message)
class MessageTranslationOptions(TranslationOptions):
    fields = ('content',)

@register(Request)
class RequestTranslationOptions(TranslationOptions):
    fields = ('fault_description', 'note', 'admin_note', 'fault_type', 'urgency',) 