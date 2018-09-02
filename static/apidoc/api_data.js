define({ "api": [
  {
    "description": "<p>Изменение пароля</p>",
    "type": "post",
    "url": "/core/change_password/",
    "title": "04. Поменять пароль [change_password]",
    "name": "Change_password",
    "group": "01__Core",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "current_password",
            "description": "<p>Current password</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "new_password",
            "description": "<p>New password</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/change_password/"
      }
    ]
  },
  {
    "description": "<p>Изменение номера телефона <br>Завершение Изменения почты происходит в методе change_email_complete</p>",
    "type": "post",
    "url": "/core/change_email/",
    "title": "07. Поменять почту [change_email]",
    "group": "01__Core",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "new_email",
            "description": "<p>New email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "name": "PostCoreChange_email",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/change_email/"
      }
    ]
  },
  {
    "description": "<p>Завершение смены email. Полсе подтверждения высланного кода, процесс считается завершенным.</p>",
    "type": "post",
    "url": "/core/change_email_complete/",
    "title": "08. Завершение смены email [change_email_complete]",
    "group": "01__Core",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Auth Token</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "new_email",
            "description": "<p>New email</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>Code sent to phone or email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "name": "PostCoreChange_email_complete",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/change_email_complete/"
      }
    ]
  },
  {
    "description": "<p>Изменение номера телефона <br>Завершение Изменения номера происходит в методе change_phone_complete</p>",
    "type": "post",
    "url": "/core/change_phone/",
    "title": "05. Поменять номер телефона [change_phone]",
    "group": "01__Core",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "new_phone",
            "description": "<p>New Phone</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "name": "PostCoreChange_phone",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/change_phone/"
      }
    ]
  },
  {
    "description": "<p>Завершение смены номера. Полсе подтверждения высланного кода, процесс считается завершенным.</p>",
    "type": "post",
    "url": "/core/change_phone_complete/",
    "title": "06. Завершение смены номера [change_phone_complete]",
    "group": "01__Core",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Auth Token</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "new_phone",
            "description": "<p>New phone or email</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>Code sent to phone or email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "name": "PostCoreChange_phone_complete",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/change_phone_complete/"
      }
    ]
  },
  {
    "description": "<p>Cброс пароля по почте <br>Завершение Сброса пароля происходит в методе reset_email_password_complete</p>",
    "type": "post",
    "url": "/core/reset_email_password/",
    "title": "11. Cброс пароля по почте  [reset_email_password]",
    "group": "01__Core",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>Email</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "new_password",
            "description": "<p>New Password</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "name": "PostCoreReset_email_password",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/reset_email_password/"
      }
    ]
  },
  {
    "description": "<p>Завершение cброса пароля по почте</p>",
    "type": "post",
    "url": "/core/reset_email_password_complete/",
    "title": "12. Завершение cброса пароля по почте [reset_email_password_complete]",
    "group": "01__Core",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "email",
            "description": "<p>Email</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>code</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "name": "PostCoreReset_email_password_complete",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/reset_email_password_complete/"
      }
    ]
  },
  {
    "description": "<p>Сброс пароля <br>Завершение Сброса пароля происходит в методе reset_password_complete</p>",
    "type": "post",
    "url": "/core/reset_password/",
    "title": "09. Сброс пароля [reset_password]",
    "group": "01__Core",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "phone",
            "description": "<p>Phone</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "new_password",
            "description": "<p>New Password</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "name": "PostCoreReset_password",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/reset_password/"
      }
    ]
  },
  {
    "description": "<p>Завершение сброса пароля. <br>Полсе подтверждения высланного кода, процесс считается завершенным.</p>",
    "type": "post",
    "url": "/core/reset_password_complete/",
    "title": "10. Завершение сброса пароля [reset_password_complete]",
    "group": "01__Core",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "phone",
            "description": "<p>Phone or email</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>Code sent to phone or email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "name": "PostCoreReset_password_complete",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/reset_password_complete/"
      }
    ]
  },
  {
    "description": "<p>Регистрация с помощью телефона или почты. <br>После регистрации, следует Завершение регистрации(<code>sign_up_complete</code>) с помощью высланного кода.<br></p>",
    "type": "post",
    "url": "/core/sign_up/",
    "title": "02. Регистрация [sign_up]",
    "name": "Sign_Up",
    "group": "01__Core",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>E-mail or Phone</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "name",
            "description": "<p>Name</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>Password</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/sign_up/"
      }
    ]
  },
  {
    "description": "<p>Завершение регистрации. Полсе подтверждения высланного кода, регистрация считается завершенной, и только после этого пользователь числится в базе.</p>",
    "type": "post",
    "url": "/core/sign_up_complete/",
    "title": "03. Завершение регистрации [sign_up_complete]",
    "name": "Sign_Up_Complete",
    "group": "01__Core",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>Registration phone or email</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "code",
            "description": "<p>Code sent to phone or email</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/sign_up_complete/"
      }
    ]
  },
  {
    "description": "<p>Авторизация через <code>email</code> или <code>номер телефона</code></p>",
    "group": "01__Core",
    "type": "post",
    "url": "/core/sign_in/",
    "title": "01. Вход в систему [sign_in]",
    "name": "Sign_in",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "username",
            "description": "<p>email or phone number</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "password",
            "description": "<p>Password</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./core/views.py",
    "groupTitle": "01__Core",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/core/sign_in/"
      }
    ]
  },
  {
    "description": "<p>Информация о Пользователе. user_id is optional</p>",
    "type": "get",
    "url": "/user/info/",
    "title": "01. Информация о Пользователе",
    "group": "02__User",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": true,
            "field": "user_id",
            "description": "<p>User id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./user/views.py",
    "groupTitle": "02__User",
    "name": "GetUserInfo",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/user/info/"
      }
    ]
  },
  {
    "description": "<p>Список всех пользователей.</p>",
    "type": "post",
    "url": "/user/list_users/",
    "title": "05. Список пользователей",
    "group": "02__User",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./user/views.py",
    "groupTitle": "02__User",
    "name": "PostUserList_users",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/user/list_users/"
      }
    ]
  },
  {
    "description": "<p>Удалить аватар.</p>",
    "type": "post",
    "url": "/user/remove_avatar/",
    "title": "04. Удалить аватар",
    "group": "02__User",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./user/views.py",
    "groupTitle": "02__User",
    "name": "PostUserRemove_avatar",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/user/remove_avatar/"
      }
    ]
  },
  {
    "description": "<p>Обновить аватар.</p>",
    "type": "post",
    "url": "/user/update_avatar/",
    "title": "03. Обновить аватар",
    "group": "02__User",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "avatar",
            "description": "<p>Файл изображения</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./user/views.py",
    "groupTitle": "02__User",
    "name": "PostUserUpdate_avatar",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/user/update_avatar/"
      }
    ]
  },
  {
    "description": "<p>Обновить профиль.</p>",
    "type": "post",
    "url": "/user/update_profile/",
    "title": "02. Обновить профиль",
    "group": "02__User",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": true,
            "field": "name",
            "description": "<p>Name</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "language",
            "description": "<p>Language {RUSSIAN = 1, KAZAKH = 2, ENGLISH = 3}</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "on_save",
            "description": "<p>On Save {ON_SAVE_SUM_30 = 30, ON_SAVE_SUM_31 = 31}</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "on_full",
            "description": "<p>On Full {ON_FULL_OPEN_FOUR = 1, ON_FULL_FINISH_GAME = 2}</p>"
          },
          {
            "group": "Parameter",
            "type": "Boolean",
            "optional": true,
            "field": "ace_allowed",
            "description": "<p>Ace allowed {True, False}</p>"
          },
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": true,
            "field": "on_eggs",
            "description": "<p>On eggs {ON_EGGS_OPEN_FOUR = 1, ON_EGGS_OPEN_DOUBLE = 2}</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./user/views.py",
    "groupTitle": "02__User",
    "name": "PostUserUpdate_profile",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/user/update_profile/"
      }
    ]
  },
  {
    "description": "<p>Список всех активных комнат <br>Список всех активных комнат</p>",
    "type": "get",
    "url": "/room/all/",
    "title": "11. Список всех активных комнат [all_rooms]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "GetRoomAll",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/all/"
      }
    ]
  },
  {
    "description": "<p>Тест <br>Тестирование простого метода <code>GET</code></p>",
    "type": "get",
    "url": "/room/test/",
    "title": "01. Тест [test]",
    "group": "03__Room",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "GetRoomTest",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/test/"
      }
    ]
  },
  {
    "description": "<p>Создание комнаты <br>Создание комнаты. Метод <code>post</code></p>",
    "type": "post",
    "url": "/room/create/",
    "title": "02. Создание комнаты [create_room]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomCreate",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/create/"
      }
    ]
  },
  {
    "description": "<p>Показать список разрешенных карт для хода <br>Показать список разрешенных карт в комнате с id <code>room_id</code> в колоде с id <code>deck_id</code></p>",
    "type": "post",
    "url": "/room/deck/allowed/",
    "title": "09. Показать список разрешенных карт [get_allowed]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "room_id",
            "description": "<p>Room id</p>"
          },
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "deck_id",
            "description": "<p>Deck id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomDeckAllowed",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/deck/allowed/"
      }
    ]
  },
  {
    "description": "<p>Создать колоду <br>Создать колоду в комнате с id <code>room_id</code> и козырем <code>trump</code></p>",
    "type": "post",
    "url": "/room/deck/create/",
    "title": "07. Создать комнату [create_deck]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "room_id",
            "description": "<p>Room id</p>"
          },
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "trump",
            "description": "<p>Trump</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomDeckCreate",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/deck/create/"
      }
    ]
  },
  {
    "description": "<p>Сделать ХОД <br>Сделать ход картой с id <code>card_id</code> из списка разрешенных карт в комнате с id <code>room_id</code> в колоде с id <code>deck_id</code></p>",
    "type": "post",
    "url": "/room/deck/make_move/",
    "title": "10. Сделать ХОД [make_move]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "room_id",
            "description": "<p>Room id</p>"
          },
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "deck_id",
            "description": "<p>Deck id</p>"
          },
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "card_id",
            "description": "<p>Card id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomDeckMake_move",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/deck/make_move/"
      }
    ]
  },
  {
    "description": "<p>Показать колоду <br>Показать колоду с id <code>deck_id</code>. Можно просматривать БЕЗ авторизации</p>",
    "type": "post",
    "url": "/room/deck/show/",
    "title": "08. Показать колоду [show_deck]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": true,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "deck_id",
            "description": "<p>Deck id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomDeckShow",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/deck/show/"
      }
    ]
  },
  {
    "description": "<p>Вход в комнату</p>",
    "type": "post",
    "url": "/room/enter/",
    "title": "03. Вход в комнату [enter_room]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "room_id",
            "description": "<p>Room id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomEnter",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/enter/"
      }
    ]
  },
  {
    "description": "<p>Покинуть комнату <br>Вход в комнату с id room_id</p>",
    "type": "post",
    "url": "/room/leave/",
    "title": "04. Покинуть комнату [leave_room]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "room_id",
            "description": "<p>Room id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomLeave",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/leave/"
      }
    ]
  },
  {
    "description": "<p>Готов <br>Нажатие кнопки ГОТОВ</p>",
    "type": "post",
    "url": "/room/ready/",
    "title": "06. Готов [ready]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "room_id",
            "description": "<p>Room id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomReady",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/ready/"
      }
    ]
  },
  {
    "description": "<p>Удалить игрока <br>Удалить игрока из комнаты с id <code>user_id</code></p>",
    "type": "post",
    "url": "/room/remove_user/",
    "title": "05. Удалить игрока [remove_user]",
    "group": "03__Room",
    "header": {
      "fields": {
        "Header": [
          {
            "group": "Header",
            "type": "String",
            "optional": false,
            "field": "auth-token",
            "description": "<p>Токен авторизации</p>"
          }
        ]
      }
    },
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "integer",
            "optional": false,
            "field": "user_id",
            "description": "<p>User id</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "json",
            "optional": false,
            "field": "result",
            "description": "<p>Json</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./room/views.py",
    "groupTitle": "03__Room",
    "name": "PostRoomRemove_user",
    "sampleRequest": [
      {
        "url": "http://localhost:8000/api/v1/room/remove_user/"
      }
    ]
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./static/apidoc/main.js",
    "group": "_home_msi_dev_projects_belka_static_apidoc_main_js",
    "groupTitle": "_home_msi_dev_projects_belka_static_apidoc_main_js",
    "name": ""
  }
] });
