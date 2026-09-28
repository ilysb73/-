## 미니게임 · 스크래치 복권 화면 ####################################################

style game_bar_frame is default:
    background Frame("gui/game_bar.png", 50, 50)
    padding (70, 26, 70, 30)
    xalign 0.5
    ypos 14
    xsize 1864

style game_title_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 40
    color "#e0724f"

style game_info_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 36
    color "#3b3a4a"

## 공통: 시작 안내 카드
screen game_intro(title, desc, start_action):
    add Solid("#2e2c3a88")
    frame at card_pop:
        style "card_frame"
        xalign 0.5
        yalign 0.5
        xsize 1400
        vbox:
            spacing 28
            xalign 0.5
            text "VS  AI 리리" font "fonts/NotoSansKR-Black.otf" size 38 color "#3f8f80" xalign 0.5
            text title style "card_title" color "#e0724f"
            text desc style "card_body"
            hbox:
                xalign 0.5
                style_prefix "big"
                textbutton "도전! ▶" action start_action

## 공통: 결과 카드 (result: "win" / "lose" / "draw")
screen game_result(result, detail):
    add Solid("#2e2c3a66")
    frame at card_pop:
        style "card_frame"
        xalign 0.5
        yalign 0.5
        xsize 1100
        vbox:
            spacing 24
            xalign 0.5
            if result == "win":
                text "승리!" style "card_title" color "#3f8f80" size 84
                text "황금 스크래치 복권 획득!" font "fonts/NotoSansKR-Black.otf" size 40 color "#c98a12" xalign 0.5
            elif result == "draw":
                text "무승부!" style "card_title" color "#c98a12" size 84
                text "스크래치 복권 1장 획득" font "fonts/NotoSansKR-Black.otf" size 40 color "#5c5a6e" xalign 0.5
            else:
                text "리리 승리…" style "card_title" color "#d0664c" size 84
                text "위로의 스크래치 복권 1장" font "fonts/NotoSansKR-Black.otf" size 40 color "#5c5a6e" xalign 0.5
            text detail style "card_body" xsize 860
            hbox:
                xalign 0.5
                style_prefix "big"
                textbutton "확인 ▶" action Return(result)

## ---------------------------------------------------------------- 1) 함정 상자 (지뢰)

style tile_button is default:
    xysize (190, 190)
    background "gui/tile.png"
    hover_background "gui/tile_hover.png"
    activate_sound "audio/sfx_click.ogg"

style tile_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 64
    color "#ffffff"
    outlines [(4, "#c98a4a", 0, 0)]
    xalign 0.5
    yalign 0.5

screen mine_screen(g):
    modal True
    zorder 30
    add "bg hambak"
    add Solid("#2e2c3a55")

    frame:
        style "game_bar_frame"
        hbox:
            spacing 60
            text "함정 상자 복불복" style "game_title_text"
            text "리리가 상자 16개 중 4개에 함정을 숨겼어요" style "game_info_text"
            text "안전한 상자 {}/{}".format(g.safe_count(), g.need) style "game_info_text" color "#3f8f80"

    grid 4 4:
        xalign 0.5
        yalign 0.62
        spacing 14
        for i in range(g.n):
            $ st = g.state(i)
            if st == "closed":
                button:
                    style "tile_button"
                    sensitive (g.started and not g.done)
                    action Function(g.open, i)
                    text "?" style "tile_text"
            elif st == "safe":
                frame:
                    xysize (190, 190)
                    background "gui/tile_safe.png"
                    text "통과" font "fonts/NotoSansKR-Black.otf" size 44 color "#2f7a6c" xalign 0.5 yalign 0.5
            elif st == "boom":
                frame:
                    xysize (190, 190)
                    background "gui/tile_boom.png"
                    text "꽝!" font "fonts/NotoSansKR-Black.otf" size 60 color "#b4553a" xalign 0.5 yalign 0.5
            else:
                frame:
                    xysize (190, 190)
                    background "gui/tile_mine.png"
                    text "함정" font "fonts/NotoSansKR-Black.otf" size 40 color "#8a7f99" xalign 0.5 yalign 0.5

    if not g.started:
        use game_intro("함정 상자 복불복", "리리(AI)가 상자 16개 중 4개에 함정을 숨겼어요.\n함정을 피해 안전한 상자 3개를 열면 승리!\n(10번 중 4번 정도만 이겨요… 운을 믿어 봐요!)", Function(g.start))
    elif g.done:
        use game_result("win" if g.won else "lose", "안전한 상자 {}개를 열었어요.".format(g.safe_count()))

## ---------------------------------------------------------------- 2) SDGs 빙고

screen bingo_board(board, g, mine):
    grid 3 3:
        spacing 8
        for k in range(9):
            $ n = board[k]
            frame:
                xysize (208, 162)
                background (("gui/cell_on.png" if mine else "gui/cell_ai_on.png") if g.marked(board, k) else "gui/cell.png")
                padding (10, 10, 10, 14)
                vbox:
                    xalign 0.5
                    yalign 0.5
                    text "{}".format(n) font "fonts/NotoSansKR-Black.otf" size 40 xalign 0.5 color ("#e0724f" if mine else "#3f8f80")
                    text SDGS[n - 1] size 30 xalign 0.5 text_align 0.5

screen bingo_screen(g):
    modal True
    zorder 30
    add "bg songdo"
    add Solid("#2e2c3a55")

    frame:
        style "game_bar_frame"
        hbox:
            spacing 60
            text "SDGs 빙고 대결" style "game_title_text"
            text "SDGs 번호를 뽑아 먼저 한 줄을 채우면 승리!" style "game_info_text"

    hbox:
        xalign 0.5
        ypos 170
        spacing 40

        vbox:
            spacing 10
            text "나 ([player_name])" font "fonts/NotoSansKR-Black.otf" size 40 color "#e0724f" xalign 0.5
            use bingo_board(g.me, g, True)
            text "완성한 줄 {}".format(g.lines(g.me)) size 36 xalign 0.5

        frame:
            style "card_frame"
            xsize 420
            padding (40, 40, 40, 40)
            yalign 0.4
            vbox:
                spacing 14
                xalign 0.5
                text "이번 번호" font "fonts/NotoSansKR-Black.otf" size 36 color "#8a7f73" xalign 0.5
                if g.last():
                    text "{}".format(g.last()) font "fonts/NotoSansKR-Black.otf" size 110 color "#e0724f" xalign 0.5
                    text SDGS[g.last() - 1] font "fonts/NotoSansKR-Black.otf" size 40 xalign 0.5 text_align 0.5
                else:
                    text "?" font "fonts/NotoSansKR-Black.otf" size 110 color "#c9bfb2" xalign 0.5
                    text "뽑기를 눌러요" size 34 xalign 0.5
                text "뽑은 횟수 {}".format(len(g.called)) size 32 xalign 0.5
                hbox:
                    xalign 0.5
                    style_prefix "big"
                    textbutton "번호 뽑기!" action Function(g.draw) sensitive (g.started and not g.done)

        vbox:
            spacing 10
            text "리리 (AI)" font "fonts/NotoSansKR-Black.otf" size 40 color "#3f8f80" xalign 0.5
            use bingo_board(g.ai, g, False)
            text "완성한 줄 {}".format(g.lines(g.ai)) size 36 xalign 0.5

    if not g.started:
        use game_intro("SDGs 빙고 대결", "나와 리리(AI)의 빙고판에는 SDGs 목표가 9개씩 있어요.\n‘번호 뽑기’를 누를 때마다 목표가 하나씩 나와요.\n먼저 가로·세로·대각선 한 줄을 채우면 승리!", Function(g.start))
    elif g.done:
        use game_result(g.result, "{}번 뽑았어요. 마지막 번호: {}번 {}".format(len(g.called), g.last(), SDGS[g.last() - 1]))

## ---------------------------------------------------------------- 3) 가짜 뉴스 슈팅

style bubble_button is default:
    xsize 560
    ysize 200
    background Frame("gui/bubble.png", 60, 60)
    hover_background Frame("gui/bubble_hover.png", 60, 60)
    padding (54, 34, 54, 60)
    activate_sound "audio/sfx_click.ogg"

style bubble_text is default:
    font "fonts/NotoSansKR-Black.otf"
    size 34
    color "#3b3a4a"
    xalign 0.5
    yalign 0.5
    text_align 0.5

screen shooter_screen(g):
    modal True
    zorder 30
    add "bg ganghwa"
    add Solid("#2e2c3a44")

    if g.started and not g.done:
        timer 0.04 repeat True action Function(g.tick)

    for i, b in enumerate(g.bubbles):
        if b["state"] == "fly":
            button:
                style "bubble_button"
                xpos int(b["x"])
                ypos int(b["y"])
                action Function(g.hit, i)
                text b["text"] style "bubble_text"
        elif b["state"] == "pop":
            frame:
                xpos int(b["x"])
                ypos int(b["y"])
                xysize (560, 200)
                background Frame("gui/bubble_pop.png", 60, 60)
                padding (54, 34, 54, 60)
                text "가짜 뉴스 격파! +1" style "bubble_text" color "#2f7a6c"
        elif b["state"] == "oops":
            frame:
                xpos int(b["x"])
                ypos int(b["y"])
                xysize (560, 200)
                background Frame("gui/bubble_oops.png", 60, 60)
                padding (54, 34, 54, 60)
                text "앗! 진짜 뉴스야 −1" style "bubble_text" color "#b4553a"

    frame:
        style "game_bar_frame"
        hbox:
            spacing 50
            text "가짜 뉴스 슈팅" style "game_title_text"
            text "남은 시간 {}초".format(g.seconds_left()) style "game_info_text" color ("#d0664c" if g.left <= 5 else "#3b3a4a")
            text "격파 {} · 실수 {}".format(g.fake_hit, g.true_hit) style "game_info_text"
            text "점수 {} / 목표 {}".format(g.net(), g.need) style "game_info_text" color "#3f8f80"

    if not g.started:
        use game_intro("가짜 뉴스 슈팅", "말풍선이 날아가요! {b}가짜 뉴스{/b}만 눌러서 격파하세요.\n진짜 뉴스를 누르면 1점 깎여요.\n18초 안에 {b}4점{/b} 이상이면 승리!", Function(g.start))
    elif g.done:
        use game_result("win" if g.won else "lose", "가짜 뉴스 {}개 격파, 진짜 뉴스 {}개 실수 → {}점".format(g.fake_hit, g.true_hit, g.net()))

## ---------------------------------------------------------------- 4) 사목 대결

style omok_button is default:
    xysize (104, 104)
    background "gui/omok_cell.png"
    hover_background "gui/omok_cell_hover.png"
    activate_sound "audio/sfx_click.ogg"

screen omok_screen(g):
    modal True
    zorder 30
    add "bg library"
    add Solid("#2e2c3a55")

    frame:
        style "game_bar_frame"
        hbox:
            spacing 50
            text "AI 리리와 사목 대결" style "game_title_text"
            text "가로·세로·대각선으로 내 돌 4개를 먼저 이으면 승리!" style "game_info_text"

    hbox:
        xalign 0.5
        ypos 160
        spacing 70

        grid 7 7:
            spacing 4
            for i in range(g.n * g.n):
                $ v = g.b[i]
                if v == 0:
                    button:
                        style "omok_button"
                        sensitive (g.started and not g.done)
                        action Function(g.play, i)
                else:
                    frame:
                        xysize (104, 104)
                        background ("gui/omok_cell_win.png" if i in g.win_line else ("gui/omok_cell_last.png" if (i == g.last_ai and v == 2) else "gui/omok_cell.png"))
                        add ("gui/stone_me.png" if v == 1 else "gui/stone_ai.png") xalign 0.5 yalign 0.5

        vbox:
            spacing 18
            yalign 0.3
            add "riri think" zoom 0.5 xalign 0.5
            hbox:
                spacing 14
                add "gui/stone_me.png" zoom 0.6 yalign 0.5
                text "나 ([player_name])" font "fonts/NotoSansKR-Black.otf" size 38 yalign 0.5
            hbox:
                spacing 14
                add "gui/stone_ai.png" zoom 0.6 yalign 0.5
                text "리리 (AI)" font "fonts/NotoSansKR-Black.otf" size 38 yalign 0.5
            text "남은 수 {}번".format(g.moves_left()) font "fonts/NotoSansKR-Black.otf" size 44 color ("#d0664c" if g.moves_left() <= 3 else "#3f8f80")
            text "12수 안에 못 이기면 리리 승리!" size 32 color "#5c5a6e"

    if not g.started:
        use game_intro("AI 리리와 사목 대결", "7×7 판에서 돌 {b}4개{/b}를 한 줄로 먼저 이으면 승리!\n리리(AI)가 먼저 가운데에 둬요. 내 돌은 {b}12번{/b}까지만!\nAI의 수를 잘 읽고 막으면서 공격해요.", Function(g.start))
    elif g.done:
        use game_result(g.result, "내가 둔 수: {}번".format(g.moves))

## ---------------------------------------------------------------- 스크래치 복권

define TICKET_INFO = {
    "free": ("gui/ticket_free.png", "세계시민 스크래치 복권", "★ +10점   ♥ +6점   ▲ +3점"),
    "gold": ("gui/ticket_gold.png", "황금 스크래치 복권", "★ +10점   ♥ +6점   ▲ +3점  (당첨 확률 UP!)"),
    "shop": ("gui/ticket_shop.png", "인생역전 즉석 복권", "★ 5,000원   ♥ 2,000원   ▲ 1,000원"),
}
define SYM_COLOR = {"★": "#e0a020", "♥": "#e0604f", "▲": "#3f8f80", "●": "#8f86c4"}

style patch_button is default:
    xysize (108, 108)
    background "gui/patch.png"
    hover_background "gui/patch_hover.png"

screen scratch_screen(t, count_text=""):
    modal True
    zorder 35
    add Solid("#2e2c3acc")

    $ info = TICKET_INFO[t.kind]

    fixed at card_pop:
        xysize (1208, 838)
        xalign 0.5
        yalign 0.3
        add info[0]

        text info[1] font "fonts/NotoSansKR-Black.otf" size 46 color "#ffffff" xpos 80 ypos 62
        if count_text:
            text count_text font "fonts/NotoSansKR-Black.otf" size 32 color "#ffffff" xalign 0.93 ypos 70

        text ("같은 그림 3개가 나오면 당첨!  " + info[2]) size 32 xalign 0.5 ypos 170 color "#5c5a6e"

        grid 3 2:
            xalign 0.5
            ypos 222
            spacing 14
            for i in range(6):
                $ sym = t.cells[i]
                fixed:
                    xysize (236, 236)
                    if t.all_revealed() and t.won() and sym == t.prize_sym:
                        add "gui/sym_cell_win.png"
                    else:
                        add "gui/sym_cell.png"
                    text sym font "fonts/NotoSansKR-Black.otf" size 120 color SYM_COLOR.get(sym, "#3b3a4a") xalign 0.5 yalign 0.5
                    if not t.revealed(i):
                        grid 2 2:
                            xpos 10
                            ypos 10
                            spacing 0
                            for j in range(4):
                                if t.patches[i][j]:
                                    null width 108 height 108
                                else:
                                    button:
                                        style "patch_button"
                                        hovered Function(t.scratch, i, j)
                                        action Function(t.scratch, i, j)

    if not t.all_revealed():
        vbox:
            xalign 0.5
            yalign 0.955
            spacing 10
            text "마우스로 은박을 문지르거나 눌러서 긁어요!" font "fonts/NotoSansKR-Black.otf" size 36 color "#ffffff" xalign 0.5
            hbox:
                xalign 0.5
                style_prefix "sub"
                textbutton "한 번에 긁기" action Function(t.reveal_all)
    else:
        vbox:
            xalign 0.5
            yalign 0.955
            spacing 12
            if t.won():
                text t.prize_text() font "fonts/NotoSansKR-Black.otf" size 60 color "#ffe08a" xalign 0.5 outlines [(4, "#2e2c3a", 0, 0)]
            elif t.near_miss():
                text "아깝다! ★이 2개… 꽝!" font "fonts/NotoSansKR-Black.otf" size 56 color "#ffffff" xalign 0.5
            else:
                text "꽝! 다음 기회에…" font "fonts/NotoSansKR-Black.otf" size 56 color "#ffffff" xalign 0.5
            hbox:
                xalign 0.5
                style_prefix "big"
                textbutton "확인 ▶" action Return(t.won())
