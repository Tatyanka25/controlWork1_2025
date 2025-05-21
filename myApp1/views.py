from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import isdigit


# Create your views here.
def hello(request):
    return render(request, "hello.html")

def hello2(request):
    return HttpResponse("Hello World")

def calc(request, str_value):
    if '+' in str_value:
        a = int(str_value.split('+')[0])
        b = int(str_value.split('+')[1])
        return HttpResponse(a + b)
    if '-' in str_value:
        a = int(str_value.split('-')[0])
        b = int(str_value.split('-')[1])
        return  HttpResponse(a - b)
    if '*' in str_value:
        a = int(str_value.split('*')[0])
        b = int(str_value.split('*')[1])
        return HttpResponse(a * b)
    #if '|' in str_value:
    #    a = int(str_value.split('/')[0])
    #    b = int(str_value.split('/')[1])
    #    if b==0:
    #        return HttpResponse("Вы не можете делить на 0")
    #    else:
    #        return HttpResponse(a / b)
    return HttpResponse("Вы ввели не верные данные")

signs_v2 = {
        "aries": {"title": "Овен", "description": "Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля).", "image": "images/aries.jpg"},
        "taurus": {"title": "Телец", "description": "Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая).", "image": "images/taurus.jpg"},
        "gemini": {"title": "Близнецы", "description": "Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня).", "image": "images/gemini.jpg"},
        "cancer": {"title": "Рак", "description": "Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля).", "image": "images/cancer.jpg"},
        "leo": {"title": "Лев", "description": "Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа).", "image": "images/leo.jpg"},
        "virgo": {"title": "Дева", "description": "Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября).", "image": "images/virgo.jpg"},
        "libra": {"title": "Весы", "description": "Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября).", "image": "images/libra.png"},
        "scorpio": {"title": "Скорпион", "description": "Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября).", "image": "images/scorpio.jpg"},
        "sagittarius": {"title": "Стрелец", "description": "Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря).", "image": "images/sagittarius.jpeg"},
        "capricorn": {"title": "Козерог", "description": "Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января).", "image": "images/capricorn.jpeg"},
        "aquarius": {"title": "Водолей", "description": "Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля).", "image": "images/aquarius.jpg"},
        "pisces": {"title": "Рыбы", "description": "Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта).", "image": "images/pisces.jpg"}
    }

signs = {
        "aries": "Овен - первый знак зодиака, планета Марс (с 21 марта по 20 апреля).",
        "taurus": "Телец - второй знак зодиака, планета Венера (с 21 апреля по 21 мая).",
        "gemini": "Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня).",
        "cancer": "Рак - четвёртый знак зодиака, Луна (с 22 июня по 22 июля).",
        "leo": "Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа).",
        "virgo": "Дева - шестой знак зодиака, планета Меркурий (с 22 августа по 23 сентября).",
        "libra": "Весы - седьмой знак зодиака, планета Венера (с 24 сентября по 23 октября).",
        "scorpio": "Скорпион - восьмой знак зодиака, планета Марс (с 24 октября по 22 ноября).",
        "sagittarius": "Стрелец - девятый знак зодиака, планета Юпитер (с 23 ноября по 22 декабря).",
        "capricorn": "Козерог - десятый знак зодиака, планета Сатурн (с 23 декабря по 20 января).",
        "aquarius": "Водолей - одиннадцатый знак зодиака, планеты Уран и Сатурн (с 21 января по 19 февраля).",
        "pisces": "Рыбы - двенадцатый знак зодиака, планеты Юпитер (с 20 февраля по 20 марта)."
    }

objects_array = [
        {
            "id": 1,
            "title": "gemini",
            "info": "Близнецы - третий знак зодиака, планета Меркурий (с 22 мая по 21 июня).",
            "all_info": "Приступайте к намеченным делам не откладывая. Вы сумеете добиться впечатляющих результатов и заложить фундамент будущих успехов. Многие Близнецы проявят свои лидерские качества, что не останется незамеченным со стороны руководства. Вам охотно окажут помощь надежные соратники. Некоторые давние недоброжелатели перейдут на вашу сторону. Мелкие неприятности не заставят вас отступить, вы без особого труда найдете необычный способ решения сложных задач.",
            "img": "https://horo.mail.ru/dist/images/zodiac/180/3.png"
        },
        {
            "id": 2,
            "title": "leo",
            "info": "Лев - пятый знак зодиака, солнце (с 23 июля по 21 августа).",
            "all_info": "Вы будете настроены доброжелательно, но серьезно. Это поможет справиться со многими сложными ситуациями, договориться с самыми разными людьми и достичь поставленных целей. Не все станет получаться с первой попытки, но вы не отступите. Ваша настойчивость оправдает себя. Многие Львы сумеют обзавестись влиятельными покровителями и надежными союзниками. Благоприятный день для заключения долгосрочных контрактов и крупных сделок.",
            "img": "https://horo.mail.ru/dist/images/zodiac/180/5.png"
        },
        {
            "id": 3,
            "title": "oven",
            "info": "oven - пятый знак зодиака, солнце (с 23 июля по 21 августа).",
            "all_info": "Вы будете настроены доброжелательно, но серьезно. Это поможет справиться со многими сложными ситуациями, договориться с самыми разными людьми и достичь поставленных целей. Не все станет получаться с первой попытки, но вы не отступите. Ваша настойчивость оправдает себя. Многие Львы сумеют обзавестись влиятельными покровителями и надежными союзниками. Благоприятный день для заключения долгосрочных контрактов и крупных сделок.",
            "img": "https://horo.mail.ru/dist/images/zodiac/180/5.png"
        }
    ]

def get_sign_info(request, sign: str):
    return HttpResponse(signs.get(sign, f'Знак зодиака {sign} не обнаружен.'))

def get_sign_info_by_num(request, sign: int):
    if 0 < sign < len(signs):
        cur_sign = list(signs)[sign - 1]
        return HttpResponseRedirect(f'/myApp1/get_signs/{cur_sign}')
    return HttpResponse(f'Знак зодиака {sign} не обнаружен.')

def signs_2(request, sign: str):
    data = {"signs": signs.get(sign, f'Знак зодиака {sign} не обнаружен.')}
    #data = {"signs": sign}
    return render(request, "signs.html", context = data)

def signs_3(request):
    data = {"signs": signs.keys()}
    #data = {"signs": sign}
    return render(request, "signs_3.html", context = data)

def get_sign_info_by_num_2(request, sign: int):
    if 0 < sign <= len(signs_v2):
        cur_sign = list(signs_v2)[sign - 1]
        data = {
            "sign": cur_sign,
            "title": signs_v2[cur_sign]["title"],
            "description": signs_v2[cur_sign]["description"],
            "image": signs_v2[cur_sign]["image"]
        }
        return render(request, "sign_info.html", context=data)
    return render(request, "sign_info.html", {"error": f'Знак зодиака {sign} не обнаружен.'})

def show_all(request):
    context = {"objects_array": objects_array}
    return render(request, "show_all.html", context)

def get_sign_one(request, sign: int):
    if 0 < sign <= len(objects_array):
        cur_sign = objects_array[sign-1]
        context = {"cur_sign": cur_sign}
        return render(request, "show1.html", context)
    else:
        error = "Такого знака нет"
        context = {"error": error}
        return render(request, "show1.html", context)