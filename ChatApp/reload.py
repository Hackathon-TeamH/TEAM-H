from jinja2 import Template
from models import models

def make_HTML(user_id, channel_id):
    messages = models.getMessageAll(channel_id)

    html = '''
            {% if messages %}
            {% for msg in messages %}
            {% if msg.user_id != user_id %}
            <div class="message_box">
                <p class="user_name">{{msg.user_name}}</p>
                <div class="message">
                    <p class="upper_message">{{msg.translated_message}}</p>
                    <p class="lower_message" data-hidden-message="{{msg.message}}">原文表示</p>
                </div>
            </div>
            {% else %}
            <div class="my_message_box">
                <div class="my_message">
                    <p class="upper_message">{{msg.message}}</p>
                    <p class="lower_message" data-hidden-message="{{msg.translated_message}}">翻訳文表示</p>
                </div>
                <div class="buttons">
                    <button class="change_message" type="submit"><ion-icon name="pencil-outline"></ion-icon>
                    </button>
                    <form class="delete_message" action="/delete" method="POST">
                        <input type="hidden" name="message_id" value="{{msg.id}}">
                        <button type="submit"><ion-icon name="trash-outline"></ion-icon></button>
                    </form>
                </div>
            </div>
            {% endif %} 
            {% endfor %}
            {% else %}
            <div class="no_message"><p>投稿がありません</p></div>
            {% endif %}
    '''

    template = Template(html)
    data = {"messages" : messages, "user_id" : user_id}
    result = template.render(data)
    print(result)
    return result