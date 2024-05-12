from jinja2 import Template
from models import models

def make_HTML(user_id, channel_id):
    messages = models.getMessageAll(channel_id)

    html = '''
            {% if messages %}
            {% for msg in messages%}
            {% if msg.user_id != user_id %}
            <div class="messages">
                <p class="user_name">{{msg.user_name}}</p>
                <div class="message">
                    <p class="upper_message">{{msg.translated_message}}</p>
                    <a class="lower_message" data-hidden-message="{{msg.message}}">原文表示</a>
                </div>
            </div>
            {% else %}
            <div class="my_messages">
                <div class="my_message">
                    <p class="upper_message">{{msg.message}}</p>
                    <a class="lower_message" data-hidden-message="{{msg.translated_message}}">翻訳文表示</a>
                </div>
                <div class="buttons">
                    <a class="change_message" type="submit" href="#"><ion-icon name="pencil-outline"></ion-icon>
                    </a>
                    <a class="delete_message" type="submit" href="/delete/{{msg.id}}">
                        <ion-icon name="trash-outline"></ion-icon>
                    </a>
                </div>
            </div>
            {% endif %} {% endfor %}
            {% else %}
            <div class="no_message"><p>投稿がありません</p></div>
            {% endif %}
    '''

    template = Template(html)
    data = {"messages" : messages, "user_id" : user_id}
    result = template.render(data)
    return result