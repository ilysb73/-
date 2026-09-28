## 미니게임 로직 (AI 리리와 대결) #####################################################
## 슈팅(가짜 뉴스) · 복불복 함정 상자(지뢰) · SDGs 빙고 · 사목(4목) · 스크래치 복권
## 난이도 조절: 각 클래스의 숫자(시간, 목표 점수, 꽝 개수, 수 제한, AI 실수 확률)를 바꾸면 돼요.

init -1 python:
    import random as _rnd
    import time as _time
    import math

    # ------------------------------------------------------------ 가짜 뉴스 슈팅
    class ShooterGame(object):
        FAKES = [
            "공유만 하면 1번에 100원 기부!",
            "강화도 갯벌에 공룡 출현 (AI 사진)",
            "초콜릿 먹으면 키가 10cm 쑥쑥",
            "내일부터 전국 학교 영원히 방학",
            "이 링크 누르면 게임 아이템 공짜",
            "송도 G타워는 초콜릿으로 지었다",
            "월미도 바다가 내일 사라진다?!",
        ]
        TRUES = [
            "1902년 인천에서 하와이 이민 출발",
            "송도에 녹색기후기금 사무국이 있다",
            "공정무역은 농부에게 정당한 값을",
            "함박마을엔 고려인 이웃이 산다",
            "인천대교는 바다 위를 지나는 다리",
        ]
        LANES = [175, 355, 535, 715]

        def __init__(self, duration=18.0, need=4):
            self.duration = duration
            self.left = duration
            self.need = need
            self.started = False
            self.done = False
            self.won = False
            self.fake_hit = 0
            self.true_hit = 0
            self.last = None
            items = [(t, True) for t in self.FAKES] + [(t, False) for t in self.TRUES]
            _rnd.shuffle(items)
            self.bubbles = []
            for i, (t, fake) in enumerate(items):
                self.bubbles.append(dict(
                    text=t, fake=fake, x=1960.0,
                    y=self.LANES[i % len(self.LANES)] + _rnd.randint(-20, 20),
                    speed=_rnd.uniform(360.0, 480.0),
                    spawn=0.5 + i * 1.3,
                    state="wait", flash=0.0))

        def start(self):
            self.started = True
            self.last = _time.time()

        def tick(self, dt=None):
            if not self.started or self.done:
                return
            now = _time.time()
            if dt is None:
                dt = min(0.12, max(0.0, now - self.last))
            self.last = now
            self.left -= dt
            elapsed = self.duration - self.left
            for b in self.bubbles:
                if b["state"] == "wait" and elapsed >= b["spawn"]:
                    b["state"] = "fly"
                if b["state"] == "fly":
                    b["x"] -= b["speed"] * dt
                    if b["x"] < -580:
                        b["state"] = "gone"
                elif b["state"] in ("pop", "oops"):
                    b["flash"] -= dt
                    if b["flash"] <= 0:
                        b["state"] = "gone"
            if self.left <= 0 or all(b["state"] == "gone" for b in self.bubbles):
                self.left = max(0.0, self.left)
                self.finish()

        def hit(self, i):
            b = self.bubbles[i]
            if self.done or b["state"] != "fly":
                return
            if b["fake"]:
                self.fake_hit += 1
                b["state"] = "pop"
            else:
                self.true_hit += 1
                b["state"] = "oops"
            b["flash"] = 0.7

        def net(self):
            return self.fake_hit - self.true_hit

        def finish(self):
            self.done = True
            self.won = self.net() >= self.need

        def seconds_left(self):
            return int(math.ceil(max(0.0, self.left)))

    # ------------------------------------------------------------ 복불복 뽑기 상자 (지뢰)
    class MineGame(object):
        def __init__(self, n=16, mines=4, need=3):
            self.n = n
            self.need = need
            self.mines = _rnd.sample(range(n), mines)
            self.opened = []
            self.done = False
            self.won = False
            self.started = False

        def start(self):
            self.started = True

        def open(self, i):
            if self.done or i in self.opened:
                return
            self.opened.append(i)
            if i in self.mines:
                self.done = True
                self.won = False
            elif len(self.opened) >= self.need:
                self.done = True
                self.won = True

        def state(self, i):
            if i in self.opened:
                return "boom" if i in self.mines else "safe"
            if self.done and i in self.mines:
                return "mine"
            return "closed"

        def safe_count(self):
            return len([i for i in self.opened if i not in self.mines])

    # ------------------------------------------------------------ SDGs 빙고
    SDGS = ["빈곤 퇴치", "기아 종식", "건강과 웰빙", "양질의 교육", "성평등", "깨끗한 물",
            "깨끗한 에너지", "좋은 일자리", "산업과 혁신", "불평등 감소", "지속가능 도시",
            "책임 소비", "기후 행동", "바다 생태계", "육지 생태계", "평화와 정의", "파트너십"]

    class BingoGame(object):
        LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

        def __init__(self):
            self.me = _rnd.sample(range(1, 18), 9)
            self.ai = _rnd.sample(range(1, 18), 9)
            self.pool = list(range(1, 18))
            _rnd.shuffle(self.pool)
            self.called = []
            self.done = False
            self.result = None
            self.started = False

        def start(self):
            self.started = True

        def lines(self, board):
            return len([L for L in self.LINES if all(board[k] in self.called for k in L)])

        def marked(self, board, k):
            return board[k] in self.called

        def draw(self):
            if self.done or not self.pool:
                return
            self.called.append(self.pool.pop())
            m = self.lines(self.me)
            a = self.lines(self.ai)
            if m or a or not self.pool:
                self.done = True
                if m and not a:
                    self.result = "win"
                elif a and not m:
                    self.result = "lose"
                else:
                    self.result = "draw"

        def last(self):
            return self.called[-1] if self.called else None

    # ------------------------------------------------------------ 사목 (7x7, 4개 연속) vs AI
    class OmokGame(object):
        DIRS = [(0, 1), (1, 0), (1, 1), (1, -1)]

        def __init__(self, n=7, k=4, max_moves=12, blunder=0.55):
            self.n = n
            self.k = k
            self.max_moves = max_moves
            self.blunder = blunder
            self.b = [0] * (n * n)      # 0 빈칸, 1 나, 2 리리
            self.moves = 0
            self.done = False
            self.result = None
            self.win_line = []
            self.started = False
            c = (n // 2) * n + n // 2
            self.b[c] = 2               # 리리가 먼저 가운데에 둔다
            self.last_ai = c

        def start(self):
            self.started = True

        def _rc(self, i):
            return divmod(i, self.n)

        def _in(self, r, c):
            return 0 <= r < self.n and 0 <= c < self.n

        def line_at(self, i, p):
            r0, c0 = self._rc(i)
            for dr, dc in self.DIRS:
                cells = [i]
                for sgn in (1, -1):
                    r, c = r0 + dr * sgn, c0 + dc * sgn
                    while self._in(r, c) and self.b[r * self.n + c] == p:
                        cells.append(r * self.n + c)
                        r += dr * sgn
                        c += dc * sgn
                if len(cells) >= self.k:
                    return cells
            return []

        def would_win(self, i, p):
            self.b[i] = p
            ok = bool(self.line_at(i, p))
            self.b[i] = 0
            return ok

        def _shape(self, i, p):
            r0, c0 = self._rc(i)
            s = 0
            for dr, dc in self.DIRS:
                cnt, opens = 1, 0
                for sgn in (1, -1):
                    r, c = r0 + dr * sgn, c0 + dc * sgn
                    while self._in(r, c) and self.b[r * self.n + c] == p:
                        cnt += 1
                        r += dr * sgn
                        c += dc * sgn
                    if self._in(r, c) and self.b[r * self.n + c] == 0:
                        opens += 1
                if cnt >= self.k:
                    s += 10000
                elif cnt == self.k - 1:
                    s += 800 if opens == 2 else (100 if opens == 1 else 0)
                elif cnt == self.k - 2:
                    s += 40 if opens == 2 else (8 if opens == 1 else 0)
                else:
                    s += 2 if opens == 2 else 0
            return s

        def score(self, i):
            r, c = self._rc(i)
            center = self.n // 2
            return 1.1 * self._shape(i, 2) + 1.0 * self._shape(i, 1) + (3 - (abs(r - center) + abs(c - center)) * 0.5)

        def ai_move(self):
            empties = [i for i in range(self.n * self.n) if self.b[i] == 0]
            for i in empties:
                if self.would_win(i, 2):
                    return i
            for i in empties:
                if self.would_win(i, 1):
                    return i
            ranked = sorted(empties, key=lambda i: -self.score(i))
            if len(ranked) > 3 and _rnd.random() < self.blunder:
                return _rnd.choice(ranked[1:4])
            return ranked[0]

        def play(self, i):
            if self.done or self.b[i] != 0:
                return
            self.b[i] = 1
            self.moves += 1
            line = self.line_at(i, 1)
            if line:
                self.done, self.result, self.win_line = True, "win", line
                return
            if 0 not in self.b:
                self.done, self.result = True, "draw"
                return
            j = self.ai_move()
            self.b[j] = 2
            self.last_ai = j
            line = self.line_at(j, 2)
            if line:
                self.done, self.result, self.win_line = True, "lose", line
                return
            if 0 not in self.b:
                self.done, self.result = True, "draw"
            elif self.moves >= self.max_moves:
                self.done, self.result = True, "lose"

        def moves_left(self):
            return max(0, self.max_moves - self.moves)

    # ------------------------------------------------------------ 스크래치 복권
    # kind: "free" 일반(점수), "gold" 황금(점수, 당첨 잘 됨), "shop" 복권 가게(돈, 1장 1,000원)
    # 같은 그림 3개가 나오면 당첨!  표: (그림, 확률, 상금)
    SCRATCH_TABLE = {
        "free": [("★", 0.08, 10), ("♥", 0.14, 6), ("▲", 0.20, 3)],
        "gold": [("★", 0.20, 10), ("♥", 0.25, 6), ("▲", 0.25, 3)],
        "shop": [("★", 0.05, 5000), ("♥", 0.10, 2000), ("▲", 0.15, 1000)],
    }
    SCRATCH_SYMBOLS = ["★", "♥", "▲", "●"]

    class ScratchTicket(object):
        def __init__(self, kind="free"):
            self.kind = kind
            self.prize_sym = None
            self.prize = 0
            r = _rnd.random()
            acc = 0.0
            for sym, p, amount in SCRATCH_TABLE[kind]:
                acc += p
                if r < acc:
                    self.prize_sym, self.prize = sym, amount
                    break
            self.cells = self._fill()
            self.patches = [[False] * 4 for _ in range(6)]   # 칸마다 은박 4조각

        def _fill(self):
            others = [s for s in SCRATCH_SYMBOLS if s != self.prize_sym]
            if self.prize_sym:
                cells = [self.prize_sym] * 3
                pool = others * 2
                _rnd.shuffle(pool)
                cells += pool[:3]
            else:
                if _rnd.random() < 0.5:
                    cells = ["★", "★"]                  # 아깝다! (★ 2개만)
                    pool = ["♥", "♥", "▲", "▲", "●", "●"]
                else:
                    cells = []
                    pool = SCRATCH_SYMBOLS * 2          # 그림마다 최대 2개 -> 꽝
                _rnd.shuffle(pool)
                cells += pool[:6 - len(cells)]
            _rnd.shuffle(cells)
            return cells

        def scratch(self, i, j):
            self.patches[i][j] = True

        def reveal_all(self):
            self.patches = [[True] * 4 for _ in range(6)]

        def revealed(self, i):
            return sum(self.patches[i]) >= 3

        def all_revealed(self):
            return all(self.revealed(i) for i in range(6))

        def won(self):
            return self.prize_sym is not None

        def prize_text(self):
            if not self.won():
                return "꽝! 다음 기회에…"
            if self.kind == "shop":
                return "당첨! 상금 {:,}원".format(self.prize)
            return "당첨! 보너스 +{}점".format(self.prize)

        def near_miss(self):
            return (not self.won()) and self.cells.count("★") == 2
