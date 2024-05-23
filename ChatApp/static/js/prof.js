const userIcon = document.querySelector(".edit_profile_page_user_icon");
const userTextField = document.querySelector(".signup_input_for_profile");
userIcon.innerHTML = userTextField.value.slice(0, 1);

userTextField.addEventListener("input", () => {
  userIcon.innerHTML = userTextField.value.slice(0, 1);
});

const submitButton = document.querySelector(".confirm_contained");
const nameField = document.getElementById("signup-name-input");
const countryField = document.getElementById("signup-living-country-input");
const cityField = document.getElementById("signup-living-town-input");

// フィールドの変更を監視
[nameField, countryField, cityField].forEach((field) => {
  field.addEventListener("input", () => {
    // いずれかのフィールドに変更があればボタンを有効化
    if (
      nameField.value.trim() !== "" ||
      countryField.value.trim() !== "" ||
      cityField.value.trim() !== ""
    ) {
      submitButton.disabled = false;
    } else {
      submitButton.disabled = true;
    }
  });
});

const onSubmit = () => {
  const form = document.querySelector(".edit_profile_wrapper");
  const name = document.querySelector(".signup_input_for_profile").value;
  const nameErrorMessage = document.querySelector(".profile_name");
  nameErrorMessage.innerHTML = "";
  if (!name) {
    nameErrorMessage.innerHTML = "ユーザー名を記入してください";
    return;
  }

  form.submit();
};
