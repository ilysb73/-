## 엔딩 화면 (1쪽: 인증 결과 · 2쪽: 영역별 점수, 선택 돌아보기, 순위) ###################

style end_head is default:
    font "fonts/NotoSansKR-Black.otf"
    size 40
    color "#e0724f"

style score_bar:
    xsize 460
    ysize 30
    left_bar Frame("gui/bar_full.png", 13, 13)
    right_bar Frame("gui/bar_empty.png", 13, 13)
    thumb None

style stat_frame is default:
    background Frame("gui/tag_plus.png", 28, 28)
    padding (34, 18, 34, 22)

transform stamp_in:
    alpha 0.0
    zoom 2.2
    rotate -12
    pause 0.3
    easein 0.35 alpha 1.0 zoom 1.0 rotate -6

screen ending_screen():
    modal True
    zorder 30
    default page = 1

    frame at card_pop:
        style "card_frame"
        xalign 0.5
        yalign 0.5
        xsize 1860
        ysize 1050
        padding (84, 46, 84, 40)

        if page == 1:
            vbox:
                xalign 0.5
                spacing 10

                text "[player_name]의 세계시민 인증 결과" style "end_head" xalign 0.5 size 44

                frame at stamp_in:
                    xalign 0.5
                    background Frame(("gui/tile_safe.png" if final["passed"] else "gui/tile_boom.png"), 40, 40)
                    padding (70, 20, 70, 28)
                    if final["passed"]:
                        text "인증 통과!" font "fonts/NotoSansKR-Black.otf" size 84 color "#2f7a6c"
                    else:
                        text "아쉽게 탈락…" font "fonts/NotoSansKR-Black.otf" size 84 color "#b4553a"

                hbox:
                    xalign 0.5
                    spacing 16
                    add "gui/star.png" zoom 1.1 yalign 0.5
                    text final["tier"] font "fonts/NotoSansKR-Black.otf" size 58 yalign 0.5
                text final["msg"] size 36 color "#5c5a6e" xalign 0.5

                text "총점 {}점  ·  통과 기준 {}점  ·  만점 {}점".format(final["total"], PASS_SCORE, MAX_SCORE) font "fonts/NotoSansKR-Black.otf" size 44 xalign 0.5

                hbox:
                    xalign 0.5
                    spacing 18
                    frame:
                        style "stat_frame"
                        text "본미션 통과 {}/{}".format(missions_passed, len(SCENE_ORDER)) style "bold_text" size 36
                    frame:
                        style "stat_frame"
                        text "넌센스 {}/{}".format(len([q for q in quiz_log if q]), len(QUIZ_ORDER)) style "bold_text" size 36
                    frame:
                        style "stat_frame"
                        text "AI 대결 승리 {}/{}".format(count_wins(), len(GAME_NAMES)) style "bold_text" size 36
                    frame:
                        style "stat_frame"
                        text "복권 당첨 {}/{}".format(len([k for k in ticket_log if k["won"]]), len(ticket_log)) style "bold_text" size 36

                hbox:
                    xalign 0.5
                    spacing 40
                    text "남은 용돈 {:,}원".format(money) size 38
                    if lottery_spent:
                        text "복권에 쓴 돈 {:,}원 → 당첨금 {:,}원".format(lottery_spent, lottery_won) size 38 color ("#3f8f80" if lottery_won > lottery_spent else "#d0664c")
                if final["bonus"]:
                    text "예산대로 쓰고 용돈을 절반 이상 남겼어요! 금융 보너스 +{}".format(final["bonus"]) size 34 color "#3f8f80" xalign 0.5
                text "오늘 참가자 {}명 중 {}위!".format(final["count"], final["rank"]) font "fonts/NotoSansKR-Black.otf" size 46 color "#3f8f80" xalign 0.5

                hbox:
                    xalign 0.5
                    style_prefix "big"
                    textbutton "자세한 결과 보기 ▶" action SetScreenVariable("page", 2)

        else:
            hbox:
                spacing 70

                ## 왼쪽: 영역별 점수
                vbox:
                    xsize 800
                    spacing 12
                    text "영역별 점수" style "end_head"
                    for k, name in CATS:
                        hbox:
                            spacing 16
                            text name size 34 xsize 230 yalign 0.5
                            bar value StaticValue(min(score[k], CATMAX[k]), CATMAX[k]) style "score_bar" yalign 0.5
                            text "{}/{}".format(score[k], CATMAX[k]) size 34 yalign 0.5
                    text "※ 도전·행운에는 스크래치 복권 보너스가 더해질 수 있어요." size 30 color "#8a7f73"
                    null height 60
                    hbox:
                        spacing 24
                        hbox:
                            style_prefix "sub"
                            textbutton "◀ 이전" action SetScreenVariable("page", 1)
                        hbox:
                            style_prefix "big"
                            textbutton "처음으로 ↺" action Return("again")
                    null height 10
                    hbox:
                        style_prefix "sub"
                        textbutton "순위 초기화 (선생님용)" action Confirm("이 기기에 저장된 순위와 통과율 기록을 모두 지울까요?", yes=Function(clear_board))

                ## 오른쪽: 선택 돌아보기, 순위
                vbox:
                    xsize 840
                    spacing 6

                    text "나의 선택 돌아보기" style "end_head"
                    for i, l in enumerate(choice_log):
                        hbox:
                            spacing 14
                            if l["tag"] == "best":
                                add "gui/dot_done.png" yalign 0.5
                            elif l["tag"] == "ok":
                                add "gui/num.png" zoom 0.55 yalign 0.5
                            else:
                                add "gui/dot_now.png" yalign 0.5
                            text "[[{}] {}".format(l["step"], l["label"]) size 32 xsize 680 yalign 0.5
                            text "+{}".format(l["gained"]) font "fonts/NotoSansKR-Black.otf" size 32 color TAG_COLOR[l["tag"]] yalign 0.5

                    null height 14
                    text "오늘의 순위 TOP 5" style "end_head"
                    for i, e in enumerate((persistent.board or [])[:5]):
                        hbox:
                            spacing 14
                            text "{}위".format(i + 1) font "fonts/NotoSansKR-Black.otf" size 34 xsize 90 color ("#e0724f" if e["id"] == final["me"] else "#3b3a4a")
                            text e["name"] size 34 xsize 270 color ("#e0724f" if e["id"] == final["me"] else "#3b3a4a")
                            text e["tier"] size 32 xsize 300
                            text "{}점".format(e["score"]) font "fonts/NotoSansKR-Black.otf" size 34
