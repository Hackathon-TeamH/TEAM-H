 
//選択したチャンネルの色を変える

    //channel_listクラスの要素を変数listに格納
    const list = document.querySelectorAll(".channel_list");
    console.log(list);

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
        document
          .querySelector(".hamburger_menu")
          .classList.add("active_hamburger_menu");
          set_language()
      });

    document
      .querySelector(".close_hamburger_menu")
      .addEventListener("click", () => {
        document
          .querySelector(".hamburger_menu")
          .classList.remove("active_hamburger_menu");
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

    document
      .querySelector(".active_profile")
      .addEventListener("click", () => {
        getProfile();
        document
          .querySelector(".profile_dialog")
          .classList.add("profile_dialog_active");
      });

    document
      .querySelector(".dli_close_profile")
      .addEventListener("click", () => {
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
     document.querySelector(".message_container").addEventListener("click", function(event) {
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
        const language = ["ja", "ja-JP"].includes(window.navigator.language)
        const profile = document.querySelector(".active_profile")
        const channel = document.querySelector(".join_channel")
        const logout = document.querySelector(".logout_button")

        profile.innerHTML = language ? "Profile" : "プロフィール"
        channel.innerHTML = language ? "Join Channel" : "チャットに参加する"
        logout.innerHTML = language ? "Logout" : "ログアウト"         
    }

    set_language();