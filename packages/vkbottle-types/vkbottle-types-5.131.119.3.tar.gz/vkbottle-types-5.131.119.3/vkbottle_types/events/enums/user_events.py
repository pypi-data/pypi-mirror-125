from enum import IntEnum


class UserEventType(IntEnum):
    UNDEFINED_EVENT = -1

    REPLACE_MESSAGE_FLAGS = 1
    INSTALL_MESSAGE_FLAGS = 2
    RESET_MESSAGE_FLAGS = 3

    MESSAGE_NEW = 4
    MESSAGE_EDIT = 5
    IN_READ = 6
    OUT_READ = 7
    FRIEND_ONLINE = 8
    FRIEND_OFFLINE = 9
    RESET_DIALOG_FLAGS = 10
    REPLACE_DIALOG_FLAGS = 11
    INSTALL_DIALOG_FLAGS = 12
    MESSAGES_DELETE = 13
    MESSAGES_RESTORE = 14

    MESSAGE_CHANGE = 18
    CLEAR_MESSAGE_CACHE = 19

    CHANGE_MAJOR_ID = 20
    CHANGE_MINOR_ID = 21

    CHAT_EDIT = 51
    CHAT_INFO_EDIT = 52
    DIALOG_TYPING_STATE = 61

    CHAT_TYPING_STATE = 62
    USERS_TYPING_STATE = 63
    CHAT_VOICE_MESSAGE_STATES = 64
    PHOTO_UPLOAD_STATE = 65
    VIDEO_UPLOAD_STATE = 66
    FILE_UPLOAD_STATE = 67

    CALL = 70
    COUNTER = 80
    USER_INVISIBLE_CHANGE = 81
    NOTIFICATIONS_SETTINGS_CHANGED = 114
    CHAT_CALL = 115
    CALLBACK_BUTTON_REPLY = 119
