import vk_api
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def index(request):
    return render(request, 'main/index.html')


def get_vk_posts():
    import vk_api
    from django.conf import settings

    vk_session = vk_api.VkApi(token=settings.VK_API_TOKEN)
    vk = vk_session.get_api()
    group_id = settings.VK_GROUP_ID

    # Получаем последние 5 постов, включая репосты
    posts = vk.wall.get(owner_id=-int(group_id), count=5, filter='all')['items']

    data = []
    for post in posts:
        # Проверяем, является ли пост репостом
        if 'copy_history' in post:
            original_post = post['copy_history'][0]  # Первый элемент в copy_history — оригинальный пост
            text = original_post.get('text', 'Текста нет')  # Текст репоста
            attachments = original_post.get('attachments', [])  # Вложения репоста
        else:
            text = post.get('text', 'Текста нет')  # Текст оригинального поста
            attachments = post.get('attachments', [])  # Вложения оригинального поста

        # Извлекаем фотографии из вложений
        photos = [att['photo']['sizes'][-1]['url'] for att in attachments if att['type'] == 'photo']

        # Добавляем пост в список данных
        data.append({'text': text, 'photos': photos})

    return data


def index(request):
    posts = get_vk_posts()
    # Передаём только первый пост (или пустое значение, если нет постов)
    latest_post = posts[0] if posts else {'text': 'Нет доступных постов', 'photos': []}
    return render(request, 'main/index.html', {'post': latest_post})

from django.http import JsonResponse

def get_latest_post(request):
    posts = get_vk_posts()  # Используем вашу функцию для получения постов
    latest_post = posts[0] if posts else {'text': 'Нет доступных постов', 'photos': []}
    return JsonResponse(latest_post)
