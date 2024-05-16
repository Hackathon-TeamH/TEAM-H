from jinja2 import Template
from models import models

def renderUsers(learning_lang):
    users = []
    #自身の学ぶ言語が話す言語のuser取得
    match_users = models.getOtherLanguageUserList(learning_lang)
    for u in match_users:
        #各ユーザーが参加しているチャンネル取得
        channels = models.getChannelByUserId(u["id"])
        if len(channels) == 0:
            continue #いなかったら次へ
        else:
            for c in channels:
                #いたらそのチャンネルの参加人数取得
                num_users = len(models.getChannelMemberId(c["channel_id"]))
                if num_users >= 2:
                    continue
                else:
                    #必要な要素を取ってリストに格納
                    candidate = {
                        "partner_name":u['user_name'],
                        "channel_id":c['channel_id'],
                        "channel_name":c['channel_name']}
                    users.append(candidate)

    html = '''
        {% if users %}
            {% for user in users %}
            <li class="user_card">
                <form class="matching" action="/matching" method="POST">
                    <input type="hidden" name="channel_id" value="{{user.channel_id}}">
                    <button calss="matching_button" type="submit">
                        <div class="user_icon">{{ user.partner_name[0] }}</div>
                        <p class="channel_name">{{ user.channel_name }}</p>
                        <p class="user_name">{{ user.partner_name }}</p>
                    </button>
                </form>
                
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