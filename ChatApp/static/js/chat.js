//選択したチャンネルの色を変える

//channel_listクラスの要素を変数listに格納
const list = document.querySelectorAll(".channel_list");

//liタグをひとつずつ変数itemに格納
list.forEach((item) => {
  //itemがクリックされたときactive_link関数を呼び出す
  item.addEventListener("click", channel_activate);
});

//サブクラスactiveをリンクさせる関数
function channel_activate() {
  list.forEach((item) => {
    //listの中身を1つずつ変数itemに格納
    item.classList.remove("active"); //acticeをremoveする
  });
  //クリックしたもの(this)のクラスにactiveをaddする
  this.classList.add("active");
}

//ハンバーガーメニュー
document
  .querySelector(".hamburger_menu_button")
  .addEventListener("click", () => {
    const hamburgerMenu = document.querySelector(".hamburger_menu");
    const outer = document.querySelector(".outer_menu");
    if (hamburgerMenu.classList.contains("active")) {
      hamburgerMenu.classList.remove("active");
      hamburgerMenu.classList.add("closing");
      hamburgerMenu.addEventListener(
        "animationend",
        () => {
          hamburgerMenu.classList.remove("closing");
          outer.classList.remove("outer");
        },
        { once: true }
      );
    } else {
      hamburgerMenu.classList.add("active");
      outer.classList.add("outer");
    }
  });

document
  .querySelector(".close_hamburger_menu")
  .addEventListener("click", () => {
    const hamburgerMenu = document.querySelector(".hamburger_menu");
    const outer = document.querySelector(".outer_menu");
    hamburgerMenu.classList.remove("active");
    hamburgerMenu.classList.add("closing");
    outer.classList.remove("outer");
    hamburgerMenu.addEventListener(
      "animationend",
      () => {
        hamburgerMenu.classList.remove("closing");
        outer.classList.remove("outer");
      },
      { once: true }
    );
  });

document.querySelector(".outer_menu").addEventListener("click", () => {
  document.querySelector(".outer_menu").classList.remove("outer");
  document.querySelector(".hamburger_menu").classList.add("closing");
  document
    .querySelector(".select_user_dialog")
    .classList.remove("select_user_dialog_active");
  document
    .querySelector(".profile_dialog")
    .classList.remove("profile_dialog_active");
  document.querySelector(".hamburger_menu").addEventListener(
    "animationend",
    () => {
      document.querySelector(".hamburger_menu").classList.remove("closing");
      document.querySelector(".hamburger_menu").classList.remove("active");
    },
    { once: true }
  );
});

document.querySelector(".join_channel").addEventListener("click", () => {
  getActiveUsers();
  document
    .querySelector(".select_user_dialog")
    .classList.add("select_user_dialog_active");
});

document.querySelector(".dli-close").addEventListener("click", () => {
  document
    .querySelector(".select_user_dialog")
    .classList.remove("select_user_dialog_active");
});

const getActiveUsers = () => {
  fetch("/list-user")
    .then((res) => res.text())
    .then((html) => {
      document.querySelector(".list_user_wrapper").innerHTML = html;
    })
    .catch((error) => console.error("Error:", error));
};

document.addEventListener("DOMContentLoaded", () => {
  const listUserWrapper = document.querySelector(".list_user_wrapper");

  listUserWrapper.addEventListener("wheel", (event) => {
    if (event.deltaY !== 0) {
      event.preventDefault();
      listUserWrapper.scrollLeft += event.deltaY;
    }
  });
});

document.querySelector(".active_profile").addEventListener("click", () => {
  getProfile();
  document
    .querySelector(".profile_dialog")
    .classList.add("profile_dialog_active");
});

document.querySelector(".dli_close_profile").addEventListener("click", () => {
  document
    .querySelector(".profile_dialog")
    .classList.remove("profile_dialog_active");
});

const getProfile = () => {
  fetch("/profile")
    .then((res) => res.text())
    .then((html) => {
      document.querySelector(".profile_render").innerHTML = html;
    })
    .catch((error) => console.error("Error:", error));
};

//原文・翻訳文表示切り替え
document
  .querySelector(".message_container")
  .addEventListener("click", function (event) {
    if (event.target.classList.contains("lower_message")) {
      switch_message.call(event.target);
    }
  });

function switch_message() {
  //クリックした要素のdata属性を取得
  const datavalue = this.dataset.hiddenMessage;
  //クリックした要素のinnerHTMLを取得
  const innervalue = this.innerHTML;
  //それぞれを入れ替えてセット
  this.dataset.hiddenMessage = innervalue;
  this.innerHTML = datavalue;
}

//ハンバーガーメニュー内のテキスト変換
const set_language = () => {
  const language = ["ja", "ja-JP"].includes(window.navigator.language);
  const profile = document.querySelector(".active_profile");
  const channel = document.querySelector(".join_channel");
  const logout = document.querySelector(".logout_button");

  profile.innerHTML = language ? "Profile" : "プロフィール";
  channel.innerHTML = language ? "Join Channel" : "チャットに参加する";
  logout.innerHTML = language ? "Logout" : "ログアウト";
};

set_language();


//scrollを一番下に
window.onload = () => {
  const elm = document.getElementById("message_wrapper");
  elm.scrollTo(0, elm.scrollHeight);
};


//メッセージ編集
let originalHTML = {};

function edit_message(message_id) {
    const container = document.getElementById(message_id);
    console.log(container)
    originalHTML[message_id] = container.innerHTML;

    const msg = container.querySelector(".upper_message").innerHTML
    container.innerHTML = `
      <form id="edit_${message_id}" class="edit_box" action="/editmessage" method="POST">\
          <textarea name="edit_message">${msg}</textarea>\
          <input type="hidden" value="${message_id}" name="message_id"/>\
      </form>
      <div class="buttons">
          <button type="submit" form="edit_${message_id}">
              <ion-icon name="checkmark-outline"></ion-icon>
          </button>
          <button class="right_button" onclick="undo('${message_id}')">
              <ion-icon name="close-outline"></ion-icon>
          </button>
      </div>
    `;
}

function undo(message_id) {
  const container = document.getElementById(message_id);
  if (originalHTML[message_id]) {
    container.innerHTML = originalHTML[message_id];
  }
}

    

