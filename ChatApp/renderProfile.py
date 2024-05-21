from jinja2 import Template
from models import models

def renderProfile(id):
    user = models.getUserWithId(id)

    html = '''
        {% if user %}
            <p class="profile_icon">{{ user.user_name[0] }}</p>
            <h3 class="profile_user_name">{{ user.user_name }}</h3>
            <p class="profile_user_email">{{ user.email }}</p>
             <div class="profile_detail_table">
              <ul>
              {% if user.learning_language == "ja" %}
                <li>学ぶ言語：</li>
              {% else %}
                <li>Learning now：</li>
              {% endif %}
              {% if user.learning_language == "ja" %}
                <li>日本語</li>
              {% else %}
                <li>English</li>
              {% endif %}
              </ul>
              <ul>
              {% if user.learning_language == "ja" %}
                <li>お住まいの国：</li>
              {% else %}
                <li>Country：</li>
              {% endif %}
                <li>{{ user.country }}</li>
              </ul>
              <ul>
              {% if user.learning_language == "ja" %}
                <li>お住まいの都市：</li>
              {% else %}
                <li>City：</li>
              {% endif %}
                <li>{{ user.country }}</li>
              </ul>
            </div>
        {% else %}
            <p>アクティブなユーザーが居ません</p>
        {% endif %}
    '''

    template = Template(html)
    data = {"user" : user}
    result = template.render(data)
    return result