## 게임 기본 설정 ##################################################################

init -2 python:
    config.screen_width = 1920
    config.screen_height = 1080

define config.name = "리리와 함께하는 인천 세계시민 탐험"
define config.version = "1.0"
define build.name = "IncheonGlobalCitizen"
define config.save_directory = "IncheonGlobalCitizen-2026"
define config.window_icon = "gui/star.png"

## 소리
define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.main_menu_music = "audio/bgm_main.ogg"
define config.default_music_volume = 0.6
define config.default_sfx_volume = 0.9

## 화면 전환
define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = fade
define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)

## 축제 부스용: 되감기·저장 메뉴 끄기 (선택을 되돌려 점수를 바꾸지 못하게)
define config.rollback_enabled = False
define _game_menu_screen = None
define config.has_autosave = False

## 글자 속도 (초당 글자 수)
default preferences.text_cps = 45
default preferences.afm_time = 12

## 한글 글꼴: 굵게({b}) 쓰면 Black 글꼴로 바꿔 줌
init python:
    config.font_replacement_map["fonts/NotoSansKR-Medium.otf", True, False] = ("fonts/NotoSansKR-Black.otf", False, False)

## 빌드 설정
init python:
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)
