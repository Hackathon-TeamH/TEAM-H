from jinja2 import Template
from models import models

def renderProfile(id):
    user = models.getUserWithId(id)

    html = '''
        {% if user %}
            <p class="profile_icon">{{ user.user_name[0] }}</p>
            <h3 class="profile_user_name">{{ user.user_name }}</h3>
            <p class="profile_user_email">{{ user.email }}</p>
        {% else %}
            <p>アクティブなユーザーが居ません</p>
        {% endif %}
    '''

    template = Template(html)
    data = {"user" : user}
    result = template.render(data)
    return result