## 화면(UI) : 기본 · 대화창 · 상단 정보 · 미션 선택 · 결과 카드 · 메뉴 ###################

## ---------------------------------------------------------------- 기본 스타일

style default:
    font "fonts/NotoSansKR-Medium.otf"
    size 40
    color "#3b3a4a"
    language "korean-with-spaces"
    line_spacing 6

style button:
    activate_sound "audio/sfx_click.ogg"

style input:
    font "fonts/NotoSansKR-Medium.otf"
    size 52
    color "#3b3a4a"

style bold_text is default:
    font "fonts/NotoSansKR-Black.otf"

## ---------------------------------------------------------------- 대화창

style say_window is default:
    xalign 0.5
    yalign 1.0
    yoffset -6
    xsize 1848
    ysize 348
    background Frame("gui/textbox.png", 70, 70)
    padding (104, 76, 104, 40)

style say_dialogue is default:
    size 46
    line_spacing 12
    xsize 1640
    ypos 8

style say_label is default:
    font "fonts/NotoSansKR-Black.otf"
    size 40
    color "#ffffff"

style namebox is default:
    xpos -36
    ypos -122
    xminimum 240
    padding (50, 26, 50, 30)

image ctc_blink:
    Text("▼", size=34, color="#f28b6b", font="fonts/NotoSansKR-Black.otf")
    xalign 0.955
    yalign 0.955
    alpha 1.0
    block:
        linear 0.5 alpha 0.25 yoffset 6
        linear 0.5 alpha 1.0 yoffset 0
        repeat

define NAMEBOX = {
    "default": "gui/namebox.png",
    "me": "gui/namebox_me.png",
    "riri": "gui/namebox_riri.png",
    "sasha": "gui/namebox_sasha.png",
    "minjun": "gui/namebox_minjun.png",
}

screen say(who, what, ncolor="default"):
    window:
        id "window"

        if who is not None:
            window:
                id "namebox"
                style "namebox"
                background Frame(NAMEBOX.get(ncolor, "gui/namebox.png"), 40, 40)
                text who id "who"

        text what id "what"

## ---------------------------------------------------------------- 상단 정보(HUD)

style pill_frame is default:
    background Frame("gui/pill.png", 44, 44)
    padding (32, 16, 32, 20)

style hud_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 32
    color "#3b3a4a"

screen hud():
    zorder 10

    hbox:
        xpos 22
        ypos 18
        frame:
            style "pill_frame"
            hbox:
                spacing 10
                add "gui/pin.png" yalign 0.5 zoom 0.55
                text place_name style "hud_text"

    hbox:
        xalign 1.0
        xoffset -22
        ypos 18
        spacing 10

        frame:
            style "pill_frame"
            hbox:
                spacing 8
                text step_name style "hud_text" color "#e0724f" yalign 0.5
                null width 4
                for i in range(len(SCENE_ORDER)):
                    if i < scene_idx:
                        add "gui/dot_done.png" yalign 0.5 zoom 0.6
                    elif i == scene_idx:
                        add "gui/dot_now.png" yalign 0.5 zoom 0.9
                    else:
                        add "gui/dot_todo.png" yalign 0.5 zoom 0.6

        frame:
            style "pill_frame"
            text "통과 {}/{}".format(missions_passed, len(SCENE_ORDER)) style "hud_text" color "#3f8f80"

        frame:
            style "pill_frame"
            hbox:
                spacing 8
                add "gui/coin.png" yalign 0.5 zoom 0.55
                text "{:,}원".format(money) style "hud_text"

        frame:
            style "pill_frame"
            hbox:
                spacing 8
                add "gui/star.png" yalign 0.5 zoom 0.55
                text "{}점".format(total_score()) style "hud_text"

## ---------------------------------------------------------------- 장소 안내 카드

transform place_card_anim:
    alpha 0.0
    yoffset -30
    ease 0.45 alpha 1.0 yoffset 0
    pause 1.9
    ease 0.45 alpha 0.0 yoffset -20

style place_frame is default:
    background Frame("gui/card.png", 90, 90)
    padding (110, 56, 110, 62)

screen place_card(name, step, topic=""):
    zorder 15
    frame at place_card_anim:
        style "place_frame"
        xalign 0.5
        ypos 150
        vbox:
            spacing 2
            text "읽걷쓰 4P · {}".format(step) xalign 0.5 font "fonts/NotoSansKR-Black.otf" size 36 color "#e0724f"
            text name xalign 0.5 font "fonts/NotoSansKR-Black.otf" size 60 color "#3b3a4a"
            if topic:
                text topic xalign 0.5 size 34 color "#3f8f80"
    timer 2.9 action Hide("place_card")

## ---------------------------------------------------------------- 미션·퀴즈 선택 (제한시간)

style question_frame is default:
    background Frame("gui/question.png", 44, 44)
    padding (70, 24, 70, 30)
    xalign 0.5
    xmaximum 1600

style question_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 44
    color "#ffffff"
    text_align 0.5
    xalign 0.5

style q_head_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 32
    color "#fff3c4"
    xalign 0.5

style choice_button is default:
    xsize 1560
    xalign 0.5
    background Frame("gui/choice_idle.png", 50, 50)
    hover_background Frame("gui/choice_hover.png", 50, 50)
    padding (50, 22, 50, 28)
    activate_sound "audio/sfx_click.ogg"

style choice_text is default:
    size 38
    color "#3b3a4a"
    hover_color "#b4553a"
    xsize 1330
    yalign 0.5

style timer_bar:
    xsize 900
    ysize 30
    left_bar Frame("gui/bar_full.png", 13, 13)
    right_bar Frame("gui/bar_empty.png", 13, 13)
    thumb None

style timer_bar_warn is timer_bar:
    left_bar Frame("gui/bar_warn.png", 13, 13)

screen mission(q, opts, seconds=20, head="미션"):
    modal True
    zorder 20
    default remain = float(seconds)
    add Solid("#2e2c3a77")

    if seconds:
        timer 0.1 repeat True action If(remain > 0.1, SetScreenVariable("remain", remain - 0.1), Return(-1))

    vbox:
        xalign 0.5
        yalign 0.55
        spacing 12

        frame:
            style "question_frame"
            vbox:
                spacing 4
                text head style "q_head_text"
                text q style "question_text"

        if seconds:
            hbox:
                xalign 0.5
                spacing 18
                bar value StaticValue(remain, seconds) style ("timer_bar_warn" if remain <= 5 else "timer_bar") yalign 0.5
                text "{}초".format(int(math.ceil(remain))) font "fonts/NotoSansKR-Black.otf" size 40 color ("#d0664c" if remain <= 5 else "#ffffff") yalign 0.5 outlines [(3, "#2e2c3a", 0, 0)]

        for i, o in enumerate(opts):
            button:
                style "choice_button"
                action Return(i)
                hbox:
                    spacing 24
                    fixed:
                        xysize (72, 72)
                        yalign 0.5
                        add "gui/num.png"
                        text "{}".format(i + 1) font "fonts/NotoSansKR-Black.otf" size 40 color "#ffffff" xalign 0.5 yalign 0.5
                    text o style "choice_text"

    for i in range(len(opts)):
        key "K_{}".format(i + 1) action Return(i)

## 예비용: 일반 menu 문이 쓰일 때의 선택지 화면
screen choice(items):
    zorder 20
    add Solid("#2e2c3a66")
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 16
        for i, item in enumerate(items):
            button:
                style "choice_button"
                action item.action
                text item.caption style "choice_text"

## ---------------------------------------------------------------- 결과 카드

style card_frame is default:
    background Frame("gui/card.png", 90, 90)
    padding (120, 84, 120, 84)

style card_title is default:
    font "fonts/NotoSansKR-Black.otf"
    size 62
    xalign 0.5
    text_align 0.5

style card_body is default:
    size 40
    line_spacing 14
    xsize 1180
    xalign 0.5
    text_align 0.5

style tag_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 34

style big_button is default:
    background Frame("gui/btn_idle.png", 50, 50)
    hover_background Frame("gui/btn_hover.png", 50, 50)
    insensitive_background Frame("gui/btn2_idle.png", 50, 50)
    padding (70, 26, 70, 32)
    xminimum 320
    activate_sound "audio/sfx_click.ogg"

style big_button_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 42
    color "#ffffff"
    xalign 0.5

style sub_button is big_button:
    background Frame("gui/btn2_idle.png", 50, 50)
    hover_background Frame("gui/btn2_hover.png", 50, 50)

style sub_button_text is big_button_text:
    size 34

transform card_pop:
    alpha 0.0
    zoom 0.92
    easein 0.25 alpha 1.0 zoom 1.0

screen feedback(fb):
    modal True
    zorder 30
    add Solid("#2e2c3a88")

    frame at card_pop:
        style "card_frame"
        xalign 0.5
        yalign 0.45
        xsize 1480

        vbox:
            spacing 26
            xalign 0.5

            text fb.get("head", TAG_HEAD.get(fb["tag"], "")) style "card_title" color TAG_COLOR.get(fb["tag"], "#3b3a4a")

            if fb.get("answer"):
                text "정답: {}".format(fb["answer"]) font "fonts/NotoSansKR-Black.otf" size 46 color "#e0724f" xalign 0.5

            hbox:
                xalign 0.5
                spacing 14
                for name, v in fb.get("gains", []):
                    frame:
                        background Frame("gui/tag_plus.png", 28, 28)
                        padding (26, 8, 26, 12)
                        text "{} +{}".format(name, v) style "tag_text" color "#2f7a6c"
                if fb.get("cost"):
                    frame:
                        background Frame("gui/tag_minus.png", 28, 28)
                        padding (26, 8, 26, 12)
                        text "용돈 −{:,}원".format(fb["cost"]) style "tag_text" color "#b4553a"

            text fb.get("text", fb.get("why", "")) style "card_body"

            hbox:
                xalign 0.5
                style_prefix "big"
                textbutton "다음으로 ▶" action Return()

    key "K_RETURN" action Return()
    key "K_SPACE" action Return()

## ---------------------------------------------------------------- 이름 입력

style name_pick_button is default:
    background Frame("gui/choice_idle.png", 50, 50)
    hover_background Frame("gui/choice_hover.png", 50, 50)
    padding (44, 20, 44, 26)
    activate_sound "audio/sfx_click.ogg"

style name_pick_button_text is default:
    size 40
    hover_color "#b4553a"

screen name_entry():
    modal True
    zorder 40
    add Solid("#fff5e8aa")

    frame at card_pop:
        style "card_frame"
        xalign 0.5
        yalign 0.5
        xsize 1380

        vbox:
            spacing 28
            xalign 0.5

            text "탐험가 이름을 정해 주세요" style "card_title" color "#e0724f"
            text "키보드로 입력하거나, 아래 이름 중 하나를 골라요 (최대 8글자)" size 34 color "#8a7f73" xalign 0.5

            frame:
                xalign 0.5
                xsize 760
                background Frame("gui/input.png", 36, 36)
                padding (40, 18, 40, 24)
                input:
                    value VariableInputValue("player_name", returnable=True)
                    length 8
                    exclude "[]{}\\"
                    xalign 0.5

            hbox:
                xalign 0.5
                spacing 16
                style_prefix "name_pick"
                for nm in ["하늘", "바다", "별빛", "무지개", "새싹"]:
                    textbutton nm action SetVariable("player_name", nm)

            hbox:
                xalign 0.5
                style_prefix "big"
                textbutton "이 이름으로 출발! ▶" action Return()

## ---------------------------------------------------------------- 확인 창

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200
    add Solid("#2e2c3aaa")

    frame:
        style "card_frame"
        xalign 0.5
        yalign 0.5
        xsize 1100
        vbox:
            spacing 44
            xalign 0.5
            text message style "card_body" xsize 860
            hbox:
                xalign 0.5
                spacing 40
                style_prefix "big"
                textbutton "예" action [yes_action, Hide("confirm")]
                textbutton "아니요" action no_action

    key "game_menu" action no_action

## ---------------------------------------------------------------- 명예의 전당

screen board_view():
    modal True
    zorder 50
    add Solid("#2e2c3a99")

    frame at card_pop:
        style "card_frame"
        xalign 0.5
        yalign 0.5
        xsize 1300

        vbox:
            spacing 14
            xalign 0.5
            text "명예의 전당 TOP 10" style "card_title" color "#e0724f"
            if persistent.plays:
                text "이 기기 누적 참가 {}명 · 인증 통과 {}명 ({}%)".format(persistent.plays, persistent.passes, int(100.0 * persistent.passes / persistent.plays)) size 34 color "#3f8f80" xalign 0.5
            null height 6
            if not persistent.board:
                text "아직 기록이 없어요. 첫 번째 탐험가가 되어 보세요!" size 40 xalign 0.5
            for i, e in enumerate((persistent.board or [])[:10]):
                hbox:
                    spacing 20
                    text "{}위".format(i + 1) font "fonts/NotoSansKR-Black.otf" size 38 xsize 110
                    text e["name"] size 38 xsize 300
                    text e["tier"] size 36 xsize 400
                    text "{}점".format(e["score"]) font "fonts/NotoSansKR-Black.otf" size 38
            null height 12
            hbox:
                xalign 0.5
                style_prefix "big"
                textbutton "닫기" action Hide("board_view")

## ---------------------------------------------------------------- 메인 메뉴 (타이틀)

transform title_float:
    yoffset 0
    block:
        ease 1.8 yoffset -16
        ease 1.8 yoffset 0
        repeat

style menu_badge_text is default:
    size 30
    color "#6d5f55"

screen main_menu():
    tag menu

    add "bg title"
    add "riri happy" at title_float:
        xpos 1230
        ypos 110

    frame at card_pop:
        style "card_frame"
        xpos 90
        yalign 0.5
        xsize 1240

        vbox:
            spacing 20
            xalign 0.5

            text "리리와 함께하는" font "fonts/NotoSansKR-Black.otf" size 56 color "#e0724f" xalign 0.5
            text "인천 세계시민 탐험" font "fonts/NotoSansKR-Black.otf" size 86 color "#e0724f" xalign 0.5 outlines [(4, "#ffffff", 0, 0)]
            text "읽고 · 걷고 · 쓰는 10분 도전" size 42 xalign 0.5

            hbox:
                xalign 0.5
                spacing 10
                for b in ["인권", "평화", "문화다양성", "글로벌·환경", "금융", "AI 리터러시"]:
                    frame:
                        background Frame("gui/tag_plus.png", 28, 28)
                        padding (16, 6, 16, 10)
                        text b style "menu_badge_text"

            text "미션 8개 · 넌센스 4개 · AI 리리와 대결 4판 · 스크래치 복권" size 34 color "#5c5a6e" xalign 0.5
            text "제한시간 안에 골라야 해요! 통과율은 절반 이하!" size 34 color "#d0664c" xalign 0.5
            null height 4

            hbox:
                xalign 0.5
                style_prefix "big"
                textbutton "도전 시작! ▶" action Start()
            hbox:
                xalign 0.5
                spacing 26
                style_prefix "sub"
                textbutton "명예의 전당" action Show("board_view")
                textbutton "소리 켜기/끄기" action Preference("all mute", "toggle")
