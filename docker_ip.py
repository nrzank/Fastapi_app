import os
import re


def get_docker_ip():
    # Получаем значение переменной окружения DOCKER_HOST
    docker_host = os.environ.get("DOCKER_HOST", "127.0.0.1")

    # Ищем IP-адрес в строке, используя регулярное выражение
    docker_ip_match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", docker_host)

    # Если найден IP-адрес, возвращаем его, иначе возвращаем None или ошибку
    if docker_ip_match:
        return docker_ip_match.group(1)
    else:
        return "IP не найден"


# Пример использования
docker_ip = get_docker_ip()
print(f"Docker IP: {docker_ip}")
