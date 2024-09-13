import os
import requests
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


load_dotenv()

options = webdriver.ChromeOptions()

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")

# Установка службы драйвера для Chrome с использованием менеджера драйверов
service = Service(
    executable_path=ChromeDriverManager().install(),
    options=options
)

# Класс, описывающий процесс от авторизации до завершения покупки
class AuthorPurchase:
    def __init__(self, driver):
        self.driver = driver

    # Метод для авторизации на сайте
    def authorize(self, name, password):
        self.driver.get("https://www.saucedemo.com/")

        # Ввод авторизационных данных
        self.driver.find_element(By.ID, 'user-name').send_keys(name)
        self.driver.find_element(By.ID, 'password').send_keys(password)

        self.driver.find_element(By.ID, 'login-button').click()
        time.sleep(3)

    # Метод для добавления товара в корзину
    def add_item_to_cart(self, product):
        self.driver.find_element(By.ID, product).click()
        time.sleep(3)

    # Метод для завершения процесса покупки
    def checkout(self, first_name, last_name, postal_code):
        # Оформление заказа
        self.driver.find_element(By.CLASS_NAME, 'shopping_cart_link').click()
        self.driver.find_element(By.ID, 'checkout').click()

        # Ввод данных
        self.driver.find_element(By.ID, 'first-name').send_keys(first_name)
        self.driver.find_element(By.ID, 'last-name').send_keys(last_name)
        self.driver.find_element(By.ID, 'postal-code').send_keys(postal_code)

        # Завершение покупки
        self.driver.find_element(By.ID, 'continue').click()
        self.driver.find_element(By.ID, 'finish').click()
        self.driver.find_element(By.ID, 'back-to-products').click()
        time.sleep(3)
        
# Класс для работы с репозиториями GitHub через API
class Repository:
    def __init__(self, user_name, user_token, rep_name, headers):
        self.user_name = user_name
        self.user_token = user_token
        self.rep_name = rep_name
        self.headers = headers

    # Метод для создания нового репозитория
    def create_repository(self):
        url = "https://api.github.com/user/repos"
        data = {
            "name": self.rep_name,
            "description": "Test repository created by API",
            "private": False
        }
        # Отправляем запрос на создание репозитория
        response = requests.post(url, headers=self.headers, json=data)
        
        if response.status_code == 201:
            print(f"Repository '{self.rep_name}' created successfully.")
        else:
            print(f"Failed to create repository: {response.status_code}")
            print(response.json())

    # Метод для получения списка репозиториев пользователя
    def check_repositories(self):
        url = f"https://api.github.com/user/repos"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            repos = response.json()
            print("Ваши репозитории:")
            for repo in repos:
                print(f"- {repo['name']}")
        else:
            print(f"Ошибка при получении списка репозиториев: {response.json()}")

    # Метод для удаления репозитория
    def delete_repository(self):
        url = f"https://api.github.com/repos/{self.user_name}/{self.rep_name}"
        response = requests.delete(url, headers=self.headers)

        if response.status_code == 204:
            print(f"Repository '{self.rep_name}' deleted successfully.")
        else:
            print(f"Failed to delete repository: {response.status_code}")

# Основная функция программы
def main():
    # Загрузка данных для работы с GitHub API из переменных окружения
    github_user_name = os.getenv("GITHUB_USERNAME")
    github_api_token = os.getenv("GITHUB_API_TOKEN")
    name_repository = os.getenv("GITHUB_REPOSITORY")
    
    # Формируем заголовки для запросов к GitHub API
    headers = {
        'Authorization': f'Bearer {github_api_token}',
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }

    # Создаём экземпляр класса Repository и выполняем операции
    added_repository = Repository(github_user_name, github_api_token, name_repository, headers)
    added_repository.create_repository()
    added_repository.check_repositories()
    added_repository.delete_repository()

    # Загрузка данных для работы с сайтом saucedemo.com из переменных окружения
    username = os.getenv("USER_NAME")
    password = os.getenv("USER_PASSWORD")
    first_name = os.getenv("FIRST_NAME")
    last_name = os.getenv("LAST_NAME")
    post_index = os.getenv("POST_INDEX")
    product = os.getenv("PRODUCT_ITEM")

    # Создание экземпляра класса AuthorPurchase и выполнение сценария авторизации и покупки
    pars = AuthorPurchase(webdriver.Chrome(service=service))
    pars.authorize(username, password)  # Авторизация
    pars.add_item_to_cart(product)  # Добавление товара в корзину
    pars.checkout(last_name, first_name, post_index)  # Оформление покупки


if __name__ == '__main__':
    main()