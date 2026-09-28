## 리리와 함께하는 인천 세계시민 탐험 ##################################################
## 인천형 세계시민교육(읽걷쓰 4P) × 읽걷쓰 AI × 금융교육  |  초등 1인칭 비주얼 노벨 (약 10분)
## 본미션 8 · 넌센스 퀴즈 4 · AI 리리와 대결 4 · 스크래치 복권

## ---------------------------------------------------------------- 이미지

image bg title = "images/bg/title.webp"
image bg home = "images/bg/home.webp"
image bg museum = "images/bg/museum.webp"
image bg hambak = "images/bg/hambak.webp"
image bg sinpo = "images/bg/sinpo.webp"
image bg baengnyeong = "images/bg/baengnyeong.webp"
image bg songdo = "images/bg/songdo.webp"
image bg ganghwa = "images/bg/ganghwa.webp"
image bg library = "images/bg/library.webp"
image bg ending = "images/bg/ending.webp"

image riri normal = "images/char/riri_normal.webp"
image riri happy = "images/char/riri_happy.webp"
image riri think = "images/char/riri_think.webp"
image riri wow = "images/char/riri_wow.webp"
image sasha smile = "images/char/sasha_smile.webp"
image sasha sad = "images/char/sasha_sad.webp"
image sasha happy = "images/char/sasha_happy.webp"
image minjun tease = "images/char/minjun_tease.webp"
image minjun sorry = "images/char/minjun_sorry.webp"

## ---------------------------------------------------------------- 등장인물

define base = Character(None, ctc="ctc_blink", ctc_position="fixed")
define narrator = Character(None, kind=base, what_color="#5c5a6e")
define me = Character("[player_name]", kind=base, show_ncolor="me")
define r = Character("리리", kind=base, show_ncolor="riri")
define s = Character("사샤", kind=base, show_ncolor="sasha")
define m = Character("민준", kind=base, show_ncolor="minjun")
define mom = Character("엄마", kind=base)
define h = Character("해설사 선생님", kind=base)
define g = Character("가게 사장님", kind=base)
define lotto = Character("복권방 아저씨", kind=base)

## ---------------------------------------------------------------- 위치·움직임

transform riri_pos(x=0.78):
    xanchor 0.5
    xpos x
    yalign 1.0
    yoffset 36
    block:
        ease 1.6 yoffset 14
        ease 1.6 yoffset 36
        repeat

transform kid_pos(x=0.25):
    xanchor 0.5
    xpos x
    yalign 1.0
    yoffset 0

transform hop:
    easein 0.12 yoffset -34
    easeout 0.14 yoffset 0

## ---------------------------------------------------------------- 게임 상태

default player_name = ""
default money = 10000
default score = {}
default choice_log = []
default game_log = []
default quiz_log = []
default ticket_log = []
default place_name = ""
default step_name = ""
default scene_idx = 0
default missions_passed = 0
default made_plan = False
default sasha_friend = False
default shared_fake = False
default lottery_spent = 0
default lottery_won = 0
default final = {}
default fb = {}
default pick_i = -1
default gres = "lose"
default mg = None
default tk = None
default n_tix = 0
default tix_i = 0
default persistent.board = []
default persistent.plays = 0
default persistent.passes = 0

## ================================================================= 공통 흐름

## 장소 이동
label move_to(sid, bgname):
    window hide
    play sound "audio/sfx_whoosh.ogg"
    scene expression bgname with Dissolve(1.0)
    $ enter_scene(sid)
    pause 0.6
    return

## 본미션 선택 (제한시간) -> pick_i 에 번호 (시간 초과 = -1)
label ask_mission(sid, q):
    window hide
    call screen mission(q, mission_options(sid), MISSION_TIME, "미션 {}/8 · 읽걷쓰 {} · 제한시간 {}초".format(SCENE_ORDER.index(sid) + 1, SCENES[sid]["step"], MISSION_TIME))
    $ pick_i = _return
    return

## 본미션 결과 카드
label mission_result(sid):
    $ fb = apply_choice(sid, pick_i)
    if fb["tag"] == "best":
        play sound "audio/sfx_best.ogg"
    elif fb["tag"] == "ok":
        play sound "audio/sfx_ok.ogg"
    else:
        play sound "audio/sfx_low.ogg"
    call screen feedback(fb)
    return

## 넌센스 퀴즈 (10초)
label quiz(qid):
    window hide
    call screen mission(QUIZZES[qid]["q"], QUIZZES[qid]["opts"], QUIZ_TIME, "넌센스 퀴즈 {}/4 · 10초 안에!".format(QUIZ_ORDER.index(qid) + 1))
    $ fb = apply_quiz(qid, _return)
    if fb["tag"] == "best":
        play sound "audio/sfx_best.ogg"
    else:
        play sound "audio/sfx_low.ogg"
    call screen feedback(fb)
    return

## AI 리리와 대결 -> 결과에 따라 스크래치 복권
label ai_game(name):
    window hide
    if name == "mine":
        $ mg = MineGame()
        call screen mine_screen(mg)
    elif name == "bingo":
        $ mg = BingoGame()
        call screen bingo_screen(mg)
    elif name == "shooter":
        $ mg = ShooterGame()
        call screen shooter_screen(mg)
    else:
        $ mg = OmokGame()
        call screen omok_screen(mg)
    $ gres = _return
    $ apply_game(name, gres)
    if gres == "win":
        play sound "audio/sfx_fanfare.ogg"
        call scratch("gold")
    else:
        play sound "audio/sfx_ok.ogg"
        call scratch("free")
    return

## 스크래치 복권 1장
label scratch(kind, count_text=""):
    $ tk = ScratchTicket(kind)
    call screen scratch_screen(tk, count_text)
    $ apply_ticket(tk)
    if tk.won():
        play sound "audio/sfx_coin.ogg"
    return

## ================================================================= 시작

label start:
    scene bg home with fade
    $ reset_game()
    $ player_name = ""
    call screen name_entry
    $ player_name = clean_name(player_name)

    play music "audio/bgm_main.ogg" fadein 1.5 if_changed
    show screen hud
    $ enter_scene("plan")
    pause 0.6

    ## ------------------------------------------------ 미션 1. 우리 집 [관찰하기] 금융
    "토요일 아침. 오늘은 인천 곳곳을 탐험하는 ‘세계시민 인증 챌린지’ 날!"
    mom "[player_name], 용돈 10,000원이야. 오늘 하루 잘 계획해서 써 보렴."
    play sound "audio/sfx_coin.ogg"
    show riri normal at riri_pos() with dissolve
    r "안녕, [player_name]! 나는 읽걷쓰 AI 친구 리리야."
    show riri happy
    r "오늘 미션은 모두 제한시간이 있어. 통과하는 친구는 절반도 안 된대!"
    show riri think
    r "나랑 대결도 하고, 이기면 황금 복권도 줄게. 첫 미션! 용돈 계획부터."

    call ask_mission("plan", "오늘 용돈 10,000원, 어떻게 쓸까?")
    if pick_i == 0:
        show riri think
        r "음… 그때그때 쓰면 편하긴 한데, 끝나고 나면 어디에 썼는지 모를걸?"
    elif pick_i == 1:
        show riri happy
        me "교통비·물 5,000원, 간식 3,000원, 나눔 2,000원! 이렇게 적어 둘래."
        r "와, 벌써 예산표 완성이야!"
    elif pick_i == 2:
        show riri wow
        r "몽땅 저금? 그럼 오늘 버스비는 어떡하지?"
    elif pick_i == 3:
        show riri think
        r "친구가 사는 게 나한테도 꼭 필요할까?"
    else:
        show riri wow
        r "앗, 시간이 다 됐어! 고민만 하다 끝나 버렸네."
    call mission_result("plan")

    ## ------------------------------------------------ 넌센스 1 + 미션 2. 월미도 한국이민사박물관 [질문하기] 인권·AI
    call move_to("museum", "bg museum")
    show riri happy at riri_pos() with dissolve
    me "월미도에 도착! 바다 냄새가 솔솔 난다."
    r "바다를 보니 넌센스 퀴즈가 떠올랐어! 딱 10초!"
    call quiz("q_sea")

    show riri normal
    h "1902년 겨울, 이곳 인천 제물포항에서 100여 명이 배를 타고 하와이로 떠났어요. 우리나라 첫 공식 이민이랍니다."
    show riri think
    r "그런데 AI 검색창에 이런 답이 떴어. “옛날 이민자들은 편하게 돈 벌러 간 거예요.”"
    me "음… 이 말, 정말 맞을까? 확인해 봐야겠다."

    call ask_mission("museum", "AI가 알려 준 정보, 어떻게 확인할까?")
    if pick_i == 0:
        show riri happy
        r "“네, 정말이에요!” …어라? 나한테 물으면 나는 또 같은 말을 할 수밖에 없는데?"
    elif pick_i == 1:
        show riri normal
        me "블로그에도 비슷하게 써 있네… 그런데 누가 쓴 글이지?"
    elif pick_i == 2:
        show riri happy
        h "이민자들은 뜨거운 사탕수수 농장에서 하루 10시간씩 일했어요. 편한 길이 아니었지요."
        me "직접 확인하길 잘했다!"
    elif pick_i == 3:
        show riri wow
        h "어머, 그건 사실과 달라요. 이민자들은 아주 힘들게 일했답니다."
    else:
        show riri wow
        r "시간 초과! 확인할 기회를 놓쳤어."
    call mission_result("museum")

    ## ------------------------------------------------ 미션 3. 함박마을 [탐구하기] 문화다양성·인권 + 대결 1 함정 상자
    call move_to("hambak", "bg hambak")
    me "함박마을에 왔다. 러시아어 간판과 우즈베키스탄 빵집이 가득해!"
    show sasha smile at kid_pos(0.26) with dissolve
    s "안녕! 나는 사샤야. 우리 할머니는 고려인이셔. 우즈베키스탄에서 왔어."
    show minjun tease at kid_pos(0.74) with dissolve
    m "사샤는 말투가 이상해! 학교 알림장도 못 읽는대~"
    show sasha sad at kid_pos(0.26)
    s "……엄마가 한국어 가정통신문을 읽기 어려워하셔서, 준비물을 자주 빠뜨려."

    call ask_mission("hambak", "사샤를 위해 나는 어떻게 할까?")
    if pick_i == 0:
        show sasha smile
        s "고마워… 그런데 나도 스스로 해 보고 싶어."
    elif pick_i == 1:
        show sasha sad
        s "……할머니랑은 고려말로 이야기하는데, 그것도 쓰면 안 돼?"
    elif pick_i == 2:
        show minjun sorry
        m "어… 그렇네. 사샤야, 미안해."
        show sasha happy at kid_pos(0.26), hop
        s "고마워! 번역 앱으로 가정통신문을 같이 읽어 주면 정말 좋겠어!"
    elif pick_i == 3:
        hide minjun with dissolve
        "뒤돌아 걷는데, 사샤의 작은 목소리가 자꾸 귀에 남는다."
    else:
        "머뭇거리는 사이 사샤가 고개를 숙이고 가게 안으로 들어갔다."
    call mission_result("hambak")

    hide sasha
    hide minjun
    with dissolve
    show riri happy at riri_pos() with dissolve
    r "잠깐 쉬어 가자! 나 리리와 첫 번째 대결! 상자 속 함정을 피해 봐!"
    call ai_game("mine")

    ## ------------------------------------------------ 넌센스 2 + 미션 4. 신포국제시장 [행동하기] 금융·동물복지 + 복권방
    call move_to("sinpo", "bg sinpo")
    show riri normal at riri_pos() with dissolve
    me "신포국제시장이다! 닭강정 냄새가 솔솔~"
    r "시장에 왔으니 돈에 관한 넌센스 퀴즈! 10초!"
    call quiz("q_king")

    mom "(문자) [player_name], 시장에서 달걀 10개만 사 올래? 심부름 돈 5,000원 줄게."
    g "달걀 사러 왔니? 종류가 많단다. 골라 보렴!"
    show riri think
    r "힌트! 포장 그림보다 ‘달걀 껍데기에 적힌 번호’를 읽어 봐."

    call ask_mission("sinpo", "달걀 10개, 어떤 걸 살까? (심부름 예산 5,000원)")
    if pick_i == 0:
        show riri think
        g "제일 싸지? 대신 좁은 철창에서 키운 닭들 달걀이란다."
    elif pick_i == 1:
        show riri happy
        g "오, 번호를 읽을 줄 아는구나! 1번은 닭들이 밖에서 뛰어놀며 낳은 달걀이야."
    elif pick_i == 2:
        play sound "audio/sfx_coin.ogg"
        show riri wow
        me "500원이 모자라서… 내 용돈으로 냈다."
    elif pick_i == 3:
        show riri wow
        g "포장이 예쁘지? 그런데 껍데기 번호를 한번 보렴."
    else:
        show riri wow
        g "얘야, 뒤에 손님 기다린다~ 시간이 다 됐어!"
    call mission_result("sinpo")

    show riri think
    lotto "어이, 꼬마 손님! ‘인생역전 즉석 복권’ 1장에 1,000원! 1등은 5,000원이야!"
    me "우와, 1,000원으로 5,000원을…?"
    r "[player_name], 잘 생각해 봐. 이건 제한시간은 없어."
    window hide
    call screen mission("인생역전 즉석 복권, 살까?", mission_options("shop"), 0, "유혹의 복권방 · 내 용돈 {:,}원".format(money))
    $ pick_i = _return
    $ fb = apply_choice("shop", pick_i)
    $ n_tix = [0, 1, 2][pick_i]
    $ lottery_spent = 1000 * n_tix
    $ tix_i = 0
    while tix_i < n_tix:
        call scratch("shop", "{}/{}장".format(tix_i + 1, n_tix))
        $ tix_i += 1
    $ fb["head"] = "복권의 진실"
    if n_tix:
        $ fb["text"] = fb["text"] + " (오늘 결과: 쓴 돈 {:,}원 → 당첨금 {:,}원)".format(lottery_spent, lottery_won)
    play sound ("audio/sfx_best.ogg" if n_tix == 0 else "audio/sfx_low.ogg")
    call screen feedback(fb)

    ## ------------------------------------------------ 미션 5. 백령도 바닷가 [질문하기] 환경·글로벌
    call move_to("baengnyeong", "bg baengnyeong")
    show riri normal at riri_pos() with dissolve
    r "여긴 인천의 가장 북쪽 섬, 백령도! 내 드론 카메라로 바닷가를 탐방 중이야."
    me "점박이물범이 쉬고 있어! 그런데… 해변에 쓰레기가 가득하네."
    show riri think
    r "병에 여러 나라 글자가 적혀 있어. 중국어, 일본어, 영어… 한글도 있어."

    call ask_mission("baengnyeong", "외국 글자가 적힌 쓰레기가 가득! 어떻게 할까?")
    if pick_i == 0:
        show riri wow
        r "잠깐! 한글이 적힌 병도 있었잖아. 우리 쓰레기도 바다를 건너가."
    elif pick_i == 1:
        show riri normal
        r "주운 건 멋져! 그런데 이 쓰레기, 계속 또 밀려오지 않을까?"
    elif pick_i == 2:
        show riri happy
        me "나라별로 세어 보니 플라스틱병이 제일 많아. 이웃 나라 친구들에게 편지를 써서 같이 줄이자고 해야지!"
        r "지역 문제를 세계와 연결했어!"
    elif pick_i == 3:
        show riri think
        r "물범들한텐 여기가 집인데…"
    else:
        show riri wow
        r "시간 초과! 파도가 쓰레기를 다시 바다로 데려가 버렸어."
    call mission_result("baengnyeong")

    ## ------------------------------------------------ 넌센스 3 + 미션 6. 송도 G타워 [탐구하기] 기후·AI + 대결 2 SDGs 빙고
    call move_to("songdo", "bg songdo")
    show riri normal at riri_pos() with dissolve
    me "송도 G타워! 녹색기후기금(GCF) 사무국이 있는 곳이다."
    r "GCF는 개발도상국이 기후 위기에 대응하도록 돈을 지원하는 국제기구야. 기후 하면… 넌센스 퀴즈!"
    call quiz("q_hot")

    show riri think
    r "로비에 ‘AI와 함께 기후 위기에 강한 집 짓기’ 전시가 있어. 내가 설계 아이디어를 4개 냈는데…"
    r "사실 그중 3개는 틀렸어. AI 말이라고 다 믿으면 안 되겠지? 과학으로 골라 봐!"

    call ask_mission("songdo", "리리(AI)의 제안 중 과학적으로 맞는 것은?")
    if pick_i == 2:
        show riri happy
        r "정답! 전통 한옥의 처마에도 숨어 있는 과학이야."
    elif pick_i == -1:
        show riri wow
        r "시간 초과! 집이 완성되지 못했어."
    else:
        show riri wow
        r "땡! 내 말을 그대로 믿었구나. 그 집에선 여름에 엄청 더울걸?"
    call mission_result("songdo")

    show riri happy
    r "두 번째 대결! 지속가능발전목표, SDGs 빙고로 붙어 보자!"
    call ai_game("bingo")

    ## ------------------------------------------------ 미션 7. 강화 평화전망대 [행동하기] 평화·AI + 대결 3 가짜 뉴스 슈팅
    call move_to("ganghwa", "bg ganghwa")
    show riri normal at riri_pos() with dissolve
    me "강화 평화전망대. 강 건너 북한 땅이 손에 잡힐 듯 가깝다."
    r "남과 북이 나뉜 지 70년이 넘었어. 지금도 세계 곳곳에 전쟁으로 집을 잃은 어린이들이 있어."
    play sound "audio/sfx_click.ogg"
    "그때 휴대폰 알림이 울렸다. 충격적인 전쟁 사진과 함께 ‘공유 1번에 100원 기부! 지금 후원하기 ▶ 링크’"

    call ask_mission("ganghwa", "돕고 싶은데… 어떻게 할까?")
    if pick_i == 0:
        show riri think
        r "잠깐, 이 글 누가 만들었는지 확인해 봤어?"
    elif pick_i == 1:
        show riri normal
        r "좋아요 100개가 모여도 실제로 전해지는 건 없대."
    elif pick_i == 2:
        play sound "audio/sfx_coin.ogg"
        show riri happy
        me "사진 출처가 없네. 대신 공식 구호 기관 누리집에서 나눔 예산으로 기부할래."
    elif pick_i == 3:
        show riri wow
        r "안 돼!! 그 링크, 주소가 이상해! 피싱 사이트일 수 있어!"
    else:
        show riri wow
        r "시간 초과! 알림이 사라져 버렸어."
    call mission_result("ganghwa")

    show riri happy
    r "세 번째 대결! 날아다니는 말풍선 중 가짜 뉴스만 골라 쏘는 슈팅 게임!"
    call ai_game("shooter")

    ## ------------------------------------------------ 넌센스 4 + 대결 4 사목 + 미션 8. 도서관 [행동하기] AI 리터러시
    call move_to("library", "bg library")
    show riri normal at riri_pos() with dissolve
    me "노을이 질 무렵, 도서관에 도착했다. 다리가 뻐근하다."
    if sasha_friend:
        show sasha happy at kid_pos(0.24) with dissolve
        s "[player_name]! 나도 세계시민 다짐 쓰러 왔어. 같이 쓰자!"
    if shared_fake:
        show riri think
        r "아 참, 아까 공유한 전쟁 사진… 알고 보니 AI로 만든 가짜 사진이었대."
        me "으… 친구들한테 사과 문자 보내야겠다."
    show riri happy
    r "마지막 넌센스 퀴즈야! 다양성과 관련 있어!"
    call quiz("q_dog")

    show riri think
    r "그리고 마지막 대결… 나 리리는 계산이 아주 빨라. 사목으로 붙어 보자!"
    call ai_game("omok")

    show riri happy
    r "진짜 마지막 미션! ‘나의 세계시민 다짐’을 써서 축제 게시판에 붙이자."
    show riri think
    r "나는 AI니까 글을 대신 써 줄 수도 있는데… 어떻게 할래?"

    call ask_mission("library", "다짐글, 어떻게 쓸까?")
    if pick_i == 0:
        show riri think
        r "단어만 바꾼다고 내 생각이 되진 않는데…"
    elif pick_i == 1:
        show riri happy
        me "‘다르다고 놀리지 않고, 사실을 확인하고, 돈을 계획해서 나누는 세계시민이 되겠습니다! (맞춤법: 리리 도움)’"
        r "오늘 하루가 다 들어 있는 멋진 글이야!"
    elif pick_i == 2:
        show riri normal
        r "솔직하게 밝힌 건 좋아. 그런데 이 글엔 [player_name]의 이야기가 없는걸?"
    elif pick_i == 3:
        show riri wow
        r "앗, 그건 다른 사람이 쓴 글이잖아!"
    else:
        show riri wow
        r "시간 초과! 게시판이 닫혀 버렸어."
    call mission_result("library")

    ## ================================================================= 엔딩
    window hide
    hide screen hud
    stop music fadeout 1.5
    scene bg ending with Fade(0.6, 0.3, 0.8)
    play music "audio/bgm_calm.ogg" fadein 2.0
    show riri happy at riri_pos(0.5) with dissolve
    r "[player_name], 오늘 정말 긴 하루였지?"
    r "인천에서 읽고, 걷고, 쓰면서 만난 세계… 과연 인증을 통과했을까?"
    $ finalize()
    hide riri with dissolve
    if final["passed"]:
        play sound "audio/sfx_fanfare.ogg"
    else:
        play sound "audio/sfx_low.ogg"
    call screen ending_screen
    stop music fadeout 1.5
    return
