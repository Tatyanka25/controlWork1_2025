from django.contrib import admin

from .models import (
    Exhibition, 
    Show, 
    Sale, 
    Painter, 
    PainterImage, 
    GalleryPainting, 
    Student, 
    Program,
    ArtworkCostCalculation, 
    CanvasType, 
    MaterialType,
    Order,
    ArtistCategory,
    Artist,
    ArtistWork,
)

admin.site.register(Exhibition)
admin.site.register(Show)
admin.site.register(Sale)
admin.site.register(GalleryPainting)
admin.site.register(Student)
admin.site.register(Program)
admin.site.register(ArtworkCostCalculation)
admin.site.register(CanvasType)
admin.site.register(MaterialType)
admin.site.register(ArtistCategory)
admin.site.register(Artist)
admin.site.register(ArtistWork)
admin.site.register(Painter)
admin.site.register(PainterImage)
admin.site.register(Order)
