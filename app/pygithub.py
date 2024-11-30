from github import Github
import os

from github import Auth
from dotenv import load_dotenv
load_dotenv()

auth = Auth.Token(os.getenv('GIT_HUB_API'))


g = Github(auth=auth)

repo_name = "skachpro/photos_lyceum_bot"
repo = g.get_repo(repo_name)

def upload_to_github(file_name, file_content):
    try:

        path = f"photos/{file_name}"
        repo.create_file(path, f"Upload {file_name}", file_content)
        print(f"Файл {file_name} успішно завантажено в {path}")
        return
    except Exception as e:
        print(f"Помилка при завантаженні: {e}")
        return


g.close()