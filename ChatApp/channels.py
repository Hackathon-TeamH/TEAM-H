from jinja2 import Template
from models import models

def renderUsers(learning_lang):
    users = models.getOtherLanguageUserList(learning_lang)
    print(users)

    html = '''
        {% if users %}
            {% for user in users %}
            <li class="user_card">
                <form class="matching" action="/matching" method="POST">

                    <input type="hidden" name="partner_id" value="{{user.id}}">
                    <button type="submit"><div class="user_icon">{{ user.user_name[0] }}</div></button>
                </form>
                
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
    print(result)
    return result