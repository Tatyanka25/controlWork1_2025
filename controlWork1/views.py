from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm, ArtworkCostCalculationForm
from .models import (
    ArtworkCostCalculation,
    Exhibition,
    Show,
    Sale,
    Student,
    Program,
    Painter,
    ArtistCategory,
    GalleryPainting,
)
from django.db.models import Count, Avg, Min, Max, Sum

from django.db import models

tests = [
    "кубизм|Москва|май;символизм|Москва|июнь;кубизм|Москва|июль;кубизм|Самара|сентябрь;реализм|Орел|май/Москва",
    "кубизм|Москва|май;символизм|Москва|июнь;кубизм|Москва|июль;кубизм|Самара|сентябрь;реализм|Орел|май/Самара",
    "символизм|Самара|май;модернизм|Казань|декабрь;кубизм|Москва|июль;кубизм|Самара|сентябрь;реализм|Орел|октябрь/Самара",
]


def main_page(request):
    return render(request, "main_page.html")


def page1(request):
    search_query = request.GET.get("q", "")
    if search_query:
        exhibitions = Exhibition.objects.filter(title__istartswith=search_query).order_by("title")
        shows = Show.objects.filter(title__istartswith=search_query).order_by("title")
    else:
        exhibitions = Exhibition.objects.all().order_by("title")
        shows = Show.objects.all().order_by("title")

    sales = Sale.objects.all()
    field_verbose_names = []
    desired_field_order_sales = ["title", "discount_percent_value", "required_document"]
    for field_name in desired_field_order_sales:
        try:
            field = Sale._meta.get_field(field_name)
            verbose_name = (
                field.verbose_name.capitalize()
                if field.verbose_name
                else field.name.replace("_", " ").capitalize()
            )
            field_verbose_names.append(verbose_name)
        except Exception as e:
            print(f"Не удалось получить verbose_name для поля {field_name}: {e}")
            field_verbose_names.append(field_name.replace("_", " ").capitalize())
    context = {
        "exhibitions": exhibitions,
        "shows": shows,
        "sales": sales,
        "sales_headers": field_verbose_names,
        "search_query": search_query,
    }
    return render(request, "page1.html", context)


def page1_exhibition(request, exhibition_id: int):
    try:
        current_exhibition = Exhibition.objects.get(pk=exhibition_id)

        context = {"cur_ex": current_exhibition, "page_title": current_exhibition.title}
        return render(request, "page1_exhibition.html", context)
    except Exhibition.DoesNotExist:
        error = "Такой выставки нет в нашей галлерее"
        context = {"error": error}
        return render(request, "page1_exhibition.html", context)


def page1_show(request, show_id: int):
    try:
        current_show = Show.objects.get(pk=show_id)

        context = {"cur_show": current_show, "page_title": current_show.title}
        return render(request, "page1_show.html", context)
    except Show.DoesNotExist:
        error = "Такой шоу программы нет в нашей галлерее"
        context = {"error": error}
        return render(request, "page1_show.html", context)


def page2(request, str_value=None, city_value=None):
    exhibition_list = []
    city = ""
    count = ""

    if str_value and city_value:
        exhibitions_info = str_value.split(";")
        city = city_value.strip()

        for exhibition in exhibitions_info:
            parts = exhibition.split("|")
            if len(parts) == 3:
                style = parts[0].strip()
                city_name = parts[1].strip()
                month = parts[2].strip()
                exhibition_list.append(
                    {"style": style, "city": city_name, "month": month}
                )
        count = sum(1 for exhibition in exhibition_list if exhibition["city"] == city)

    context = {
        "exhibition_list": exhibition_list,
        "city": city,
        "count": count,
        "tests": tests,
    }

    return render(request, "page2.html", context)


def page3(request):
    painters = Painter.objects.all().prefetch_related("images").order_by("name")
    artists = (
        ArtistCategory.objects.all()
        .prefetch_related("artists_in_category", "artists_in_category__works_of_artist")
        .order_by("name")
    )
    context = {"painters": painters, "artists": artists}
    return render(request, "page3.html", context)


def page4(request):
    my_info_object = None
    course_mates_objects = []
    program_info_object = None
    error_message = None
    my_info_object = Student.objects.get(name="Лапшина Татьяна Александровна")

    if my_info_object:
        course_mates_objects = Student.objects.exclude(id=my_info_object.id).order_by(
            "name"
        )
    else:
        course_mates_objects = Student.objects.all().order_by("name")

    program_info_object = Program.objects.get(title="Бизнес-нформатика")
    context = {
        "my_info": my_info_object,
        "program_info": program_info_object,
        "course_mates": course_mates_objects,
        "error": error_message,
    }
    return render(request, "page4.html", context)


def page5(request):
    return render(request, "page5.html")


def page6(request):
    galary = GalleryPainting.objects.all()
    context = {"galary": galary}
    return render(request, "page6.html", context)


def create_order_view(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш заказ успешно создан!")
            return redirect("controlWork1:create_order")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = OrderForm()

    context = {
        "form": form,
    }
    return render(request, "order_form.html", context)


def calculate_artwork_cost_view(request):
    last_calculation_details = None
    last_calculation_values_list = None
    form_submitted_successfully = request.session.pop(
        "form_submitted_successfully", False
    )
    if request.method == "POST":
        form = ArtworkCostCalculationForm(request.POST)
        if form.is_valid():
            height = form.cleaned_data["height"]
            width = form.cleaned_data["width"]
            canvas_type = form.cleaned_data["canvas_type"]
            material_type = form.cleaned_data["material_type"]

            area_sq_cm = height * width

            total_cost_decimal = (
                canvas_type.price_per_sq_cm + material_type.price_per_sq_cm
            ) * area_sq_cm
            calculated_cost_int = round(total_cost_decimal)

            instance = form.save(commit=False)
            instance.result_cost = calculated_cost_int
            instance.save()

            messages.success(request, "Стоимость картины успешно рассчитана!")
            request.session["form_submitted_successfully"] = True
            request.session["last_calculation_id"] = instance.id
            return redirect("controlWork1:calculate_artwork_cost")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
    else:
        form = ArtworkCostCalculationForm()

        last_calculation_id = request.session.pop("last_calculation_id", None)
        if last_calculation_id:
            try:
                last_instance = ArtworkCostCalculation.objects.get(
                    id=last_calculation_id
                )
                last_calculation_details = {
                    "Высота (см)": last_instance.height,
                    "Ширина (см)": last_instance.width,
                    "Тип холста": last_instance.canvas_type.name,  # Получаем имя связанного объекта
                    "Тип материалов": last_instance.material_type.name,  # Получаем имя связанного объекта
                    "Итоговая стоимость (руб.)": last_instance.result_cost,
                }

                last_calculation_values_list = [
                    last_instance.height,
                    last_instance.width,
                    last_instance.canvas_type.name,
                    last_instance.material_type.name,
                    last_instance.result_cost,
                ]
            except ArtworkCostCalculation.DoesNotExist:
                messages.warning(request, "Не удалось найти детали последнего расчета.")
                last_calculation_details = None
                last_calculation_values_list = None

    context = {
        "form": form,
        "last_calculation_details": last_calculation_details,
        "last_calculation_values_list": last_calculation_values_list,
        "form_submitted_successfully": form_submitted_successfully,
    }
    return render(request, "artwork_cost_form.html", context)


def get_model_concrete_field_names_and_verbose_names(model_class):
    name_list = []
    verbose_name_list = []

    pk_field = model_class._meta.pk
    if pk_field:
        name_list.append(pk_field.name)
        verbose_name_list.append(
            pk_field.verbose_name.capitalize()
            if pk_field.verbose_name
            else pk_field.name.capitalize()
        )

    for field in model_class._meta.get_fields():
        if field.concrete and field.name != pk_field.name:
            if field.many_to_one:
                custom_name_key = f"{field.name}_name"
                name_list.append(custom_name_key)
                verbose_name = (
                    f"{field.verbose_name.capitalize()}"
                    if field.verbose_name
                    else f"{field.name.replace('_', ' ').capitalize()}"
                )
                verbose_name_list.append(verbose_name)

            else:
                name_list.append(field.name)
                verbose_name_list.append(
                    field.verbose_name.capitalize()
                    if field.verbose_name
                    else field.name.capitalize()
                )

    return name_list, verbose_name_list


def all_calculations_view(request):
    name_list, verbose_name_list = get_model_concrete_field_names_and_verbose_names(
        ArtworkCostCalculation
    )
    all_calculation_objects = (
        ArtworkCostCalculation.objects.all()
        .order_by("-calculated_at")
        .select_related("canvas_type", "material_type")
    )

    processed_objects_values = []
    for obj in all_calculation_objects:
        item_dict = {}
        for custom_key in name_list:
            value_to_set = None
            if custom_key == ArtworkCostCalculation._meta.pk.name:
                value_to_set = getattr(obj, ArtworkCostCalculation._meta.pk.name)
            elif custom_key.endswith("_name"):
                original_fk_name = custom_key.removesuffix("_name")
                related_obj = getattr(obj, original_fk_name, None)
                if related_obj:
                    value_to_set = related_obj.name
            else:
                if hasattr(obj, custom_key):
                    field_value = getattr(obj, custom_key)
                    try:
                        field_object = ArtworkCostCalculation._meta.get_field(
                            custom_key
                        )
                        if isinstance(field_object, models.DateTimeField) and hasattr(
                            field_value, "strftime"
                        ):
                            value_to_set = field_value.strftime("%d.%m.%Y %H:%M")
                        else:
                            value_to_set = field_value
                    except models.FieldDoesNotExist:
                        value_to_set = field_value
                else:
                    value_to_set = None

            item_dict[custom_key] = value_to_set
        processed_objects_values.append(item_dict)

    headers_for_table2 = [
        "ID",
        "Высота",
        "Ширина",
        "Холст",
        "Материалы",
        "Итог. стоимость",
        "Время",
    ]
    objects_values_list_queryset = (
        ArtworkCostCalculation.objects.filter(result_cost__gt=0)
        .order_by("id")
        .values_list(
            "id",
            "height",
            "width",
            "canvas_type__name",
            "material_type__name",
            "result_cost",
            "calculated_at",
        )
    )

    processed_objects_values_list = []
    date_field_index_table2 = 6

    for item_tuple in objects_values_list_queryset:
        item_list = list(item_tuple)
        if date_field_index_table2 < len(item_list) and hasattr(
            item_list[date_field_index_table2], "strftime"
        ):
            item_list[date_field_index_table2] = item_list[
                date_field_index_table2
            ].strftime("%d.%m.%Y %H:%M")
        processed_objects_values_list.append(tuple(item_list))

    queryset_for_stats = ArtworkCostCalculation.objects.filter(result_cost__gt=0)
    statics_val_raw = []
    aggregation_field = "result_cost"
    if queryset_for_stats.exists():
        if any(
            f.name == aggregation_field
            for f in ArtworkCostCalculation._meta.concrete_fields
        ):
            statics_val_raw = [
                queryset_for_stats.aggregate(Count(aggregation_field)),
                queryset_for_stats.aggregate(Avg(aggregation_field)),
                queryset_for_stats.aggregate(Min(aggregation_field)),
                queryset_for_stats.aggregate(Max(aggregation_field)),
                queryset_for_stats.aggregate(Sum(aggregation_field)),
            ]
    statics_val = []
    for agg_result_dict in statics_val_raw:
        statics_val.append(list(agg_result_dict.values())[0] if agg_result_dict else 0)
    if not statics_val:
        statics_val = [0] * 5

    context = {
        "objects_values": processed_objects_values,
        "name_list": name_list,
        "objects_values_list": processed_objects_values_list,
        "headers_for_table2": headers_for_table2,
        "verbose_name_list": verbose_name_list,
        "statics_val": statics_val,
    }
    return render(request, "all_calculations_table.html", context)
