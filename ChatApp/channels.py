from jinja2 import Template
from models import models

def renderUsers(learning_lang):
    users = models.getOtherLanguageUserList(learning_lang)

    html = '''
        {% if users %}
            {% for user in users %}
            <li class="user_card">
                <div class="user_icon">{{ user.user_name[0] }}</div>
                <p class="user_name">{{ user.user_name }}</p>
            </li>
            {% endfor %}
        {% else %}
        <li><p>アクティブなユーザーが居ません</p></li>
        {% endif %}
    '''

    template = Template(html)
    data = {"users" : users}

    result = template.render(data)
    return result