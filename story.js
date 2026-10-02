/* =====================================================================
   사라진 인천을 찾아서 — 이야기와 자료
   선생님 수정 안내: 대사, 선택지(t), 점수(pts), 해설(fb), 증거 카드(CLUES)를
   이 파일에서 바꾸면 바로 게임에 반영돼요.
   ===================================================================== */
'use strict';

/* ---------- 장소 (map: 그림 지도 위 핀 위치, 1920×1080 기준) ---------- */
const PLACES = {
  office:  { name:'부평역사박물관',        short:'역사박물관(본부)', step:'시작',    topic:'어린이 역사 탐정단 본부',        map:[1380, 600] },
  dohobu:  { name:'부평도호부 관아',       short:'부평도호부 관아', step:'관찰하기', topic:'계양구 계산동 · 조선 시대 관청', map:[820, 390] },
  sanseong:{ name:'계양산성',              short:'계양산성',        step:'탐구하기', topic:'계양구 · 삼국 시대 산성',        map:[470, 340] },
  hwangeo: { name:'황어장터',              short:'황어장터',        step:'질문하기', topic:'계양구 장기동 · 1919 만세운동',  map:[650, 180] },
  jul:     { name:'부평 미쓰비시 줄사택',   short:'미쓰비시 줄사택', step:'질문하기', topic:'부평구 부평2동 · 강제동원의 흔적', map:[930, 880] },
  camp:    { name:'캠프마켓 (옛 조병창)',   short:'캠프마켓',        step:'탐구하기', topic:'부평구 산곡동 · 무기 공장과 미군 기지', map:[710, 760] },
  youngdan:{ name:'부평 영단주택',          short:'영단주택',        step:'행동하기', topic:'부평구 산곡동 · 재개발로 사라진 마을', map:[520, 850] },
  gulpo:   { name:'굴포천',                short:'굴포천',          step:'행동하기', topic:'부평구 · 30년 만에 되살아난 물길', map:[1100, 700] },
};
const PLACES_ORDER = ['office','dohobu','sanseong','hwangeo','jul','camp','youngdan','gulpo'];

async function go(key, bgname){
  G.place = key; hideAll(); hideText(); bg(bgname); await wait(500);
  await placeCard(PLACES[key]);
}
function visited(key){ if(!G.visited.includes(key)) G.visited.push(key); save(); }

/* ---------- 증거 카드 ---------- */
const CLUES = {
  dohobu: { title:'부평도호부 관아', src:'위키백과 「부평도호부관아」 · 국가유산포털',
    text:'조선 시대 부평 고을을 다스리던 관청이에요. 그 자리에 **학교를 지으며 대부분의 건물이 헐렸고**, 남은 한 채도 1968년에 옮겨지며 모양(ㄱ자→ㅡ자)이 바뀌었어요. 1982년 인천시 유형문화유산이 되었어요.' },
  sanseong: { title:'계양산성의 논어 목간', src:'경향신문(2020.3.18)',
    text:'2005년 계양산성 집수정(빗물을 모으는 우물) 바닥에서 『논어』 글귀가 적힌 **나무 막대(목간)** 가 나왔어요. 4~5세기 한성백제 무렵 것으로 측정되었고, 계양산성은 2020년 **국가 사적**이 되었어요.' },
  hwangeo: { title:'황어장터 3·1만세운동', src:'계양구청 누리집 · 인천투데이',
    text:'**1919년 3월 24일** 황어장터에서 심혁성 등의 주도로 수백 명이 만세를 외쳤어요. 일본 경찰의 탄압으로 **이은선** 선생이 목숨을 잃었어요. 옛 장터는 사라졌고, 지금 장기동에 기념탑이 있어요.' },
  jul: { title:'부평 미쓰비시 줄사택', src:'경향신문(2022.12.20) · 대한민국 정책브리핑',
    text:'1938년 무렵 지어진 줄사택은 일본군 조병창에 **강제 동원된 노동자들의 합숙소**였어요. 9개 동 중 3개 동이 2018~2019년에 헐렸고, 주차장 계획이 멈춘 뒤 **남은 6개 동을 지키기로** 했어요. 지금은 국가등록문화유산이에요.' },
  camp: { title:'캠프마켓과 조병창', src:'월간 SPACE(공간) · 아시아경제(2023.1.19) · 인천투데이',
    text:'1941년 문을 연 인천 육군 조병창은 일본군의 **무기 공장**이었고 많은 사람이 강제로 동원되었어요. 해방 뒤 미군 기지(애스컴시티·캠프마켓)가 되었고 2019년 일부가 돌아왔어요. 조병창 병원 건물을 두고 **철거와 보존 논쟁**이 이어졌어요.' },
  youngdan: { title:'부평 영단주택', src:'인천투데이 · 부평역사박물관 학술총서',
    text:'1939년부터 조병창 노동자를 위해 지어진 집이에요. 해방 뒤엔 미군 부대 직원과 공장 노동자 가족들이 살았어요. 재개발로 **2023년 대부분 철거**되었고, 박물관과 주민들이 사진과 이야기를 **기록으로 남겼어요.**' },
  gulpo: { title:'되살아난 굴포천', src:'인천in(2025) · SBS 뉴스',
    text:'1990년대에 콘크리트로 덮였던 굴포천 약 **1.5km** 구간이 **2025년 12월** 생태하천으로 되살아났어요. 사라진 것도 사람들이 힘을 모으면 되찾을 수 있어요.' },
  unesco: { title:'인류 모두의 유산', src:'유네스코 세계유산협약(1972)',
    text:'유네스코는 1972년 **세계유산협약**을 만들어, 문화유산을 한 나라만의 것이 아닌 **인류 모두의 유산**으로 함께 지키자고 약속했어요.' },
};

/* =====================================================================
   0장. 탐정단 본부 (부평역사박물관)
   ===================================================================== */
async function ch_intro(){
  await go('office', 'office');
  show('curator', 'smile', 'center');
  await say('curator', '어서 와요, {name} 탐정! 부평역사박물관 어린이 역사 탐정단에 온 걸 환영해요.');
  await say('curator', '요즘 부평과 계양에서는 오래된 건물과 장소가 **도시개발**과 **무관심** 속에 하나둘 사라지고 있어요.');
  show('curator', 'normal', 'center');
  await say('curator', '사라지기 전에, 아니 이미 사라졌다면 그 기억이라도 되찾아 줄 탐정이 필요해요.');
  show('minjun', 'happy', 'left');
  await say('minjun', '나는 민준이! 너랑 같은 반이잖아. 나도 탐정단이야! 돋보기도 챙겨 왔지~');
  show('riri', 'happy', 'right');
  await say('riri', '안녕! 나는 **읽걷쓰 AI 리리**야. 자료를 빨리 찾아 읽어 주는 게 내 특기지!');
  show('riri', 'think', 'right');
  await say('riri', '하지만 기억해 줘. AI인 나도 **틀릴 때가 있어.** 그래서 우리는 이렇게 조사할 거야.');
  await say('riri', '**읽고**(자료 찾기) → **걷고**(현장에 가 보기) → **쓰기**(기록하고 알리기)! 그리고 관찰하기·질문하기·탐구하기·행동하기의 **4P** 순서로!');
  hide('minjun');
  show('curator', 'normal', 'center');
  await say('curator', '첫 번째 질문이에요. 탐정답게 골라 볼까요?');
  const pick = await choose('지역의 역사를 조사할 때, 옛 사진·지도와 지금 모습을 **비교하는** 가장 좋은 이유는?', [
    '옛날이 무조건 더 좋았기 때문에', '무엇이 **어떻게 달라졌는지** 확인할 수 있어서', '사진만 보면 모든 역사를 알 수 있어서', '지금 지도는 필요 없기 때문에']);
  if(pick === 1){ show('curator', 'smile', 'center'); await feedback({tag:'best', pts:10, fb:'정답! 비교해야 무엇이 사라지고 무엇이 새로 생겼는지 보여요. 이게 탐정의 첫 단계 **관찰하기**예요.'}, 'intro'); }
  else if(pick === 0){ await feedback({tag:'low', pts:0, fb:'옛것이 다 좋고 새것이 다 나쁜 건 아니에요. 편리해진 점과 잃어버린 것을 **함께** 살펴봐야 해요.'}, 'intro'); }
  else { await feedback({tag:'low', pts:0, fb:'사진 한 장이나 지도 하나로는 부족해요. 여러 자료를 **비교**해야 변화가 보여요.'}, 'intro'); }
  show('riri', 'happy', 'right');
  await say('riri', '오른쪽 위 **📓 탐정 수첩**에 증거 카드가 모이고, **🗺️ 지도**에서 우리가 갈 곳을 볼 수 있어!');
  await say('riri', '자, 첫 번째 현장으로 출발! 계양구 계산동의 **부평도호부 관아**야!');
  visited('office');
}

/* =====================================================================
   1장. 부평도호부 관아 [관찰하기]
   ===================================================================== */
async function ch_dohobu(){
  await go('dohobu', 'dohobu_now');
  show('minjun', 'wow', 'left');
  await say('minjun', '어? 여기 그냥 초등학교잖아! 한옥이 딱 한 채 있네?');
  show('riri', 'normal', 'right');
  await say('riri', '맞아. 여긴 조선 시대에 부평 고을을 다스리던 관청, **부평도호부 관아**가 있던 자리야.');
  await say('riri', '옛날엔 사또가 일하던 **동헌**, 손님이 묵던 **객사** 같은 건물이 여럿 있었대. 그런데 학교를 지으면서 대부분 헐렸어.');
  await say('me', '옛날 모습을 상상해 볼 수 있으면 좋겠다…');
  show('riri', 'happy', 'right');
  await say('riri', '기록을 바탕으로 **옛 모습 상상 그림**을 준비했어! 지금은 사라진 것을 찾아볼래?');
  bg('dohobu_past'); hideAll(); await wait(600);
  await gameSpot({ img:'dohobu_past', title:'관찰하기 · 사라진 것 찾기', goal:'상상 그림에서 지금은 사라진 것 3가지를 눌러요', need:3, targets:[
    { name:'담장', kind:'gone', x:0, y:500, w:1920, h:90, msg:'**담장** 발견! 관아를 둘러싸던 긴 담도 사라졌어요.' },
    { name:'객사', kind:'gone', x:80, y:230, w:540, h:270, msg:'**객사** 발견! 나라의 손님이 머물던 건물이에요. 지금은 남아 있지 않아요.' },
    { name:'문루', kind:'gone', x:790, y:600, w:380, h:290, msg:'**정문(문루)** 발견! 관아로 들어가던 큰 문도 지금은 없어요.' },
    { name:'동헌', kind:'info', x:640, y:210, w:680, h:290, msg:'가운데 큰 건물과 비슷한 한 채가 **지금도 남아 있어요.** 하지만 1968년 옮겨지며 모양이 바뀌었대요.' },
    { name:'내아', kind:'info', x:1320, y:280, w:440, h:220, msg:'이 건물은 기록이 분명하지 않아요. 남은 건물이 동헌인지 살림집(내아)인지 **학자들 의견도 나뉘어요.**' },
  ]});
  bg('dohobu_now'); await wait(500);
  show('minjun', 'think', 'left'); show('riri', 'think', 'right');
  await say('minjun', '와… 이렇게 큰 관아였는데, 지금은 한 채만 남은 거야?');
  await say('riri', '남은 건물도 1968년에 옮겨지면서 ㄱ자 모양이 ㅡ자로 바뀌었대. 1982년에야 인천시 문화유산으로 지정되었어.');
  await clue('dohobu');
  const pick = await choose('관찰을 마쳤어요. 다음 조사를 위해 가장 좋은 **탐정 질문**은?', [
    '옛날 건물은 어차피 필요 없지 않아?',
    '관아는 **언제, 왜** 헐렸고, 그때 사람들은 **어떻게 생각**했을까?',
    '학교 급식은 뭐가 맛있을까?' ], '관찰하기 → 질문하기');
  if(pick === 1){ show('riri', 'happy', 'right'); await feedback({tag:'best', pts:10, fb:'좋은 질문은 **언제·왜·누가·어떻게**를 품고 있어요. 이런 질문이 탐구의 길을 열어 줘요.'}, 'dohobu'); }
  else if(pick === 0){ await feedback({tag:'low', pts:0, fb:'쓸모만 따지면 역사는 금방 사라져요. 그 장소가 품은 **이야기와 기억**도 생각해 봐요.'}, 'dohobu'); }
  else { show('minjun', 'happy', 'left'); await say('minjun', '헤헤, 그건 나도 궁금한데?'); await feedback({tag:'low', pts:0, fb:'재밌는 질문이지만 지금 조사와는 거리가 멀어요. 조사 대상에 딱 맞는 질문을 만들어 봐요.'}, 'dohobu'); }
  visited('dohobu');
}

/* =====================================================================
   2장. 계양산성 [탐구하기] — 사실과 추측 구분
   ===================================================================== */
async function ch_sanseong(){
  await go('sanseong', 'sanseong');
  show('minjun', 'happy', 'left');
  await say('minjun', '헉헉… 계양산 올라오니까 부평이랑 계양이 한눈에 보인다!');
  show('riri', 'normal', 'right');
  await say('riri', '여기가 **계양산성**이야. 돌로 쌓은 이 성은 삼국 시대부터 쓰였대.');
  await say('riri', '그리고 엄청난 발견이 있었어. 2005년, 성 안의 우물 바닥에서 **『논어』 글귀가 적힌 나무 막대(목간)** 가 나왔거든!');
  show('minjun', 'wow', 'left');
  await say('minjun', '1500년도 더 된 나무가 썩지 않고 남아 있었다고? 대박!');
  show('riri', 'think', 'right');
  await say('riri', '탐정은 **자료로 확인된 사실**과 **내 생각(추측)**을 구분해야 해. 한번 해 볼까?');
  await gameSort({ title:'탐구하기 · 사실일까, 추측일까?', cards:[
    { t:'2005년 계양산성 우물 바닥에서 『논어』 글귀가 적힌 목간이 나왔다.', fact:true, why:'발굴 기록으로 확인된 **사실**이에요.' },
    { t:'목간은 백제의 왕이 직접 쓴 것이 틀림없다.', fact:false, why:'누가 썼는지는 기록이 없어요. 근거 없는 **추측**이에요.' },
    { t:'목간은 4~5세기(한성백제 무렵)의 것으로 측정되었다.', fact:true, why:'과학적 연대 측정 결과로 확인된 **사실**이에요.' },
    { t:'성을 지킨 병사들은 모두 매일 논어를 외웠을 것이다.', fact:false, why:'그랬을 수도 있지만 증거가 없어요. **추측**이에요.' },
    { t:'계양산성은 2020년 국가 사적으로 지정되었다.', fact:true, why:'나라의 공식 지정 기록이 있는 **사실**이에요.' },
    { t:'이 성에는 틀림없이 보물 창고가 숨겨져 있다.', fact:false, why:'재밌는 상상이지만 **추측**이에요. 확인되지 않은 이야기를 사실처럼 말하면 안 돼요.' },
  ]});
  await clue('sanseong');
  show('minjun', 'think', 'left');
  await say('minjun', '어, 저기 봐. 무너진 성벽 돌 위에 올라가서 사진 찍는 사람들이 있어. 돌 하나 기념으로 가져가도 되나?');
  const pick = await choose('성벽 돌 위에서 사진을 찍고, 돌을 가져가려는 사람들을 봤어요. 어떻게 할까?', [
    '나도 올라가서 멋진 사진을 찍는다',
    '안내판 내용을 읽어 보고, 성벽은 **밟거나 가져가면 훼손**된다고 정중하게 알린다',
    '못 본 척 지나간다' ], '탐구하기 → 행동하기');
  if(pick === 1){ show('riri', 'happy', 'right'); await feedback({tag:'best', pts:10, fb:'문화유산은 **작은 무관심**으로도 망가져요. 자료를 근거로 정중하게 알려 주는 것이 지킴이의 행동이에요.'}, 'sanseong'); }
  else if(pick === 0){ await feedback({tag:'low', pts:0, fb:'한 사람 한 사람이 올라가면 오래된 돌은 조금씩 흔들리고 무너져요. 사진은 정해진 길에서 찍어요!'}, 'sanseong'); }
  else { await feedback({tag:'ok', pts:4, fb:'직접 훼손하진 않았지만, 모른 척하는 것도 **무관심**이에요. 용기 내어 한마디 해 볼까요?'}, 'sanseong'); }
  visited('sanseong');
}

/* =====================================================================
   3장. 황어장터 [질문하기] — 사라진 장터, 남은 기억
   ===================================================================== */
async function ch_hwangeo(){
  await go('hwangeo', 'hwangeo_now');
  show('minjun', 'normal', 'left');
  await say('minjun', '여긴 계양구 장기동이야. 아파트랑 도로뿐인데… 탐정 지도에는 **장터**라고 되어 있어.');
  show('riri', 'think', 'right');
  await say('riri', '맞아. 옛날 이곳엔 사람들이 모이던 **황어장터**가 있었어. 지금은 장터가 사라지고 기념탑만 남았지.');
  await say('riri', '1919년, 이 장터에서 무슨 일이 있었는지 옛 기록 속으로 들어가 볼까?');
  bg('hwangeo_1919'); hideAll(); await wait(700); playMusic('bgm_calm');
  await narr('1919년 3월 24일 오후, 황어장터. 장날을 맞아 모인 사람들 사이로 태극기가 올라갔다.');
  await narr('“대한 독립 만세!” 심혁성을 비롯한 사람들을 따라 수백 명의 함성이 장터를 가득 채웠다.');
  await narr('일본 경찰은 사람들을 칼과 총으로 막아섰고, 이 과정에서 이은선 선생이 목숨을 잃었다.');
  bg('hwangeo_now'); await wait(600); playMusic('bgm_main');
  show('minjun', 'think', 'left'); show('riri', 'normal', 'right');
  await say('minjun', '우리 동네에서 이런 일이 있었다니… 전혀 몰랐어.');
  await say('riri', '장터가 사라지면서 그날의 기억도 흐려졌어. 사건의 순서를 정리해서 기억해 보자!');
  await gameOrder({ title:'질문하기 · 그날의 순서', goal:'일어난 순서대로 눌러요', items:[
    '1919년 3월 1일, 서울 등 여러 곳에서 3·1운동이 시작되었다.',
    '3월 24일, 장날의 황어장터에 사람들이 모여 만세를 외쳤다.',
    '일본 경찰의 탄압으로 이은선 선생이 목숨을 잃었다.',
    '세월이 흘러 장터는 사라지고, 장기동에 기념탑이 세워졌다.' ]});
  await clue('hwangeo');
  const pick = await choose('장터가 사라진 뒤에도 그날을 **기억하려면** 어떤 질문을 던져야 할까?', [
    '“기념탑만 있으면 충분하지 않을까?”',
    '“오래된 일이니 이제 잊어도 되지 않을까?”',
    '“그날의 이야기를 **우리 또래가 알 수 있게** 전하려면 무엇이 필요할까?”' ], '질문하기');
  if(pick === 2){ show('riri', 'happy', 'right'); await feedback({tag:'best', pts:10, fb:'장소가 사라져도 **이야기를 전하는 사람**이 있으면 기억은 이어져요. 이것이 인권과 평화를 지키는 세계시민의 질문이에요.'}, 'hwangeo'); }
  else if(pick === 0){ await feedback({tag:'ok', pts:4, fb:'기념탑은 소중해요. 하지만 찾아와서 읽는 사람이 없다면 기억은 흐려져요. 탑 **너머**를 질문해 봐요.'}, 'hwangeo'); }
  else { await feedback({tag:'low', pts:0, fb:'잊으면 같은 아픔이 되풀이될 수 있어요. 억울하게 희생된 사람들을 기억하는 건 **인권**을 지키는 일이에요.'}, 'hwangeo'); }
  visited('hwangeo');
}

/* =====================================================================
   4장. 미쓰비시 줄사택 [질문하기] — 인터뷰와 토론
   ===================================================================== */
async function ch_jul(){
  await go('jul', 'jul');
  show('minjun', 'wow', 'left');
  await say('minjun', '길쭉한 집들이 한 줄로 붙어 있어! 그런데 옆은 갑자기 주차장이네?');
  show('riri', 'normal', 'right');
  await say('riri', '여기는 **부평 미쓰비시 줄사택**이야. 일제강점기에 무기 공장인 **조병창**에 끌려온 노동자들이 지내던 합숙소였대.');
  await say('riri', '원래 9개 동이 있었는데, 몇 개 동은 이미 헐렸어. 이 동네에 오래 사신 할머니께 여쭤볼까?');
  hide('riri');
  show('grandma', 'normal', 'center');
  await say('grandma', '아이고, 꼬마 탐정들이구나. 이 늙은이한테 뭐가 궁금하니?');
  const r = await gamePick({ title:'질문하기 · 인터뷰 질문 고르기', goal:'할머니께 드릴 좋은 질문 3개를 골라요', need:3, qs:[
    { t:'할머니가 기억하시는 줄사택의 **옛 모습**은 어땠나요?', good:true },
    { t:'할머니 집 **주소랑 전화번호**를 알려 주세요.', good:false },
    { t:'이곳에 살던 사람들은 **어떤 일**을 했나요?', good:true },
    { t:'옛날이야기는 좀 **지루하지** 않아요?', good:false },
    { t:'건물이 **헐릴 때 어떤 마음**이 드셨어요?', good:true },
    { t:'이 집은 **몇 원**에 팔 수 있어요?', good:false },
  ]});
  if(r.good === 3){
    show('grandma', 'smile', 'center');
    await say('grandma', '옛날엔 골목마다 아이들 소리가 가득했지. 다닥다닥 붙은 집에서 서로 반찬도 나눠 먹고…');
    show('grandma', 'sad', 'center');
    await say('grandma', '어른들 말로는 그 전엔 공장에 끌려와 힘들게 일하던 사람들이 살던 곳이래. 벽이 얇아서 겨울엔 참 추웠단다.');
    await say('grandma', '몇 집이 헐려 나갈 땐… 내 어린 시절이 같이 없어지는 것 같아서 마음이 아팠어.');
  } else {
    show('grandma', 'sad', 'center');
    await say('grandma', '허허… 그런 건 대답하기가 곤란하구나. 인터뷰할 땐 **개인정보**를 묻지 말고, 상대의 **이야기와 마음**을 물어봐 주렴.');
    show('grandma', 'normal', 'center');
    await say('grandma', '그래도 하나만 말해 주마. 이 골목엔 공장에 끌려와 고생하던 사람들의 한숨이 배어 있단다.');
  }
  hide('grandma');
  show('riri', 'think', 'right'); show('minjun', 'think', 'left');
  await say('riri', '그런데 동네 사람들 중엔 **주차장이 부족하다**며 남은 건물도 헐자는 의견도 있었대.');
  await say('minjun', '음… 주차할 곳이 없으면 불편하긴 하겠다. 어떻게 하는 게 좋을까?');
  const pick = await choose('남은 줄사택, 어떻게 하는 것이 좋을까?', [
    '주차가 더 급하니까 **모두 헐고** 주차장을 만든다',
    '주민 불편은 신경 쓰지 말고 **무조건 그대로** 둔다',
    '주민들의 불편도 듣고, 남은 건물은 지키면서 **작은 전시관·쉼터처럼 함께 쓰는 방법**을 찾는다' ], '질문하기 → 토론하기');
  if(pick === 2){ show('riri', 'happy', 'right'); await say('riri', '실제로도 비슷했어! 문화재청의 보존 권고와 주민·전문가가 함께한 협의 끝에 남은 6개 동을 지키기로 했대.'); await feedback({tag:'best', pts:10, fb:'보존과 생활 불편은 둘 중 하나만 고르는 문제가 아니에요. **여러 사람의 목소리를 듣고** 함께 방법을 찾는 게 민주 시민, 세계시민의 해결법이에요.'}, 'jul'); G.flags.julBalanced = true; }
  else if(pick === 0){ await feedback({tag:'low', pts:0, fb:'한번 헐린 역사는 되돌릴 수 없어요. 강제동원의 아픔이 담긴 장소는 **다시 만들 수 없는 증거**예요.'}, 'jul'); }
  else { await feedback({tag:'ok', pts:4, fb:'지키려는 마음은 좋아요! 하지만 이웃의 불편을 외면하면 갈등이 커져요. 함께 쓰는 방법을 찾아봐요.'}, 'jul'); }
  await clue('jul');
  visited('jul');
}

/* =====================================================================
   5장. 캠프마켓(옛 조병창) [탐구하기] — AI 팩트체크
   ===================================================================== */
async function ch_camp(){
  await go('camp', 'campmarket');
  show('minjun', 'normal', 'left');
  await say('minjun', '긴 담장 너머에 오래된 벽돌 건물들이 보여. 여긴 어디야?');
  show('riri', 'happy', 'right');
  await say('riri', '**캠프마켓**이야! 이번엔 내가 인터넷 자료를 순식간에 읽고 요약해 줄게. 삐빅… 요약 완료!');
  show('riri', 'think', 'right');
  await say('riri', '…잠깐. 사실 나도 가끔 그럴듯한 **거짓 정보**를 만들어 낼 때가 있어. 내 요약에서 틀린 문장을 찾아 줄래?');
  await gameCheck({ title:'탐구하기 · 리리의 요약 팩트체크', goal:'맞으면 ⭕, 틀리면 ❌', items:[
    { t:'조병창은 1941년 문을 연 일본군의 무기 공장이었다.', ok:true, why:'여러 자료에서 확인되는 내용이에요.' },
    { t:'조병창에서 일한 사람들은 모두 스스로 원해서 즐겁게 일했다.', ok:false, why:'많은 조선 사람이 **강제로 동원**되어 힘들게 일했어요.' },
    { t:'해방 뒤 이곳에는 미군 기지(애스컴시티, 캠프마켓)가 들어섰다.', ok:true, why:'70년 넘게 미군 기지로 쓰였어요.' },
    { t:'2019년 캠프마켓 땅 일부가 우리에게 돌아왔다(반환).', ok:true, why:'2019년 12월 일부 구역이 반환되었어요.' },
    { t:'조병창 병원 건물은 1990년에 이미 모두 사라졌다.', ok:false, why:'2020년대까지 남아 있어서 **철거할지 보존할지** 큰 논쟁이 있었어요.' },
  ]});
  show('riri', 'wow', 'right');
  await say('riri', '고마워! AI가 쓴 글도 **다른 자료로 꼭 확인**해야 해. 이게 **AI 리터러시**야.');
  await clue('camp');
  show('riri', 'think', 'right');
  await say('riri', '조병창 병원 건물 아래 땅에서 기름 같은 오염 물질이 나왔대. 땅을 깨끗하게 하려면 건물을 헐어야 한다는 의견과, 역사를 지켜야 한다는 의견이 맞섰어.');
  show('minjun', 'think', 'left');
  await say('minjun', '둘 다 중요한데… 어렵다.');
  const pick = await choose('오염된 땅 위의 역사 건물, 어떻게 해야 할까?', [
    '오염은 신경 쓰지 말고 건물만 그대로 둔다',
    '빨리 헐어 버리고 새 건물을 짓는다',
    '땅을 안전하게 정화하면서도 역사를 남길 방법을 **전문가와 시민이 함께** 찾는다' ], '탐구하기');
  if(pick === 2){ show('riri', 'happy', 'right'); await feedback({tag:'best', pts:10, fb:'**안전**도 **역사**도 중요해요. 실제로 시민들이 참여한 위원회가 캠프마켓 건물 일부를 남기자는 의견을 내기도 했어요.'}, 'camp'); }
  else if(pick === 1){ await feedback({tag:'low', pts:0, fb:'서두르면 되돌릴 수 없는 것을 잃어요. 강제동원의 증거가 사라지면 다음 세대는 무엇으로 배울까요?'}, 'camp'); }
  else { await feedback({tag:'low', pts:0, fb:'오염된 땅은 사람의 건강을 해칠 수 있어요. 역사를 지키는 것도 **안전**이 먼저예요.'}, 'camp'); }
  visited('camp');
}

/* =====================================================================
   6장. 영단주택 [행동하기] — 사라져도 기록으로
   ===================================================================== */
async function ch_youngdan(){
  await go('youngdan', 'youngdan');
  show('minjun', 'wow', 'left');
  await say('minjun', '크레인이 엄청 많아! 새 아파트를 짓나 봐. 옆에 작은 옛날 집이 몇 채 남았네.');
  show('riri', 'normal', 'right');
  await say('riri', '여긴 산곡동 **부평 영단주택** 자리야. 1939년부터 조병창 노동자들을 위해 지은 집들이었어.');
  await say('riri', '해방 뒤엔 미군 부대 직원, 공장 노동자 가족들이 살았고… 재개발로 **2023년 대부분 철거**되었어.');
  show('minjun', 'think', 'left');
  await say('minjun', '이미 없어졌으면… 탐정이 할 수 있는 게 없잖아?');
  show('riri', 'happy', 'right');
  await say('riri', '아니! 부평역사박물관과 주민들은 철거 전에 사진을 찍고, 이야기를 듣고, 책으로 **기록**을 남겼어. 기록은 기억을 지켜 줘.');
  await say('riri', '지금까지 모은 기억들을 다시 떠올려 볼까? **기억 카드 짝 맞추기!**');
  await gameMemory({ title:'행동하기 · 기억 카드 짝 맞추기', goal:'장소와 그곳의 이야기를 짝지어요', pairs:[
    ['<b>부평도호부 관아</b>', '학교를 지으며<br>대부분 헐림'],
    ['<b>계양산성</b>', '『논어』 목간<br>발견'],
    ['<b>황어장터</b>', '1919년<br>만세운동'],
    ['<b>미쓰비시 줄사택</b>', '강제동원<br>노동자 합숙소'],
    ['<b>캠프마켓</b>', '옛 조병창<br>무기 공장 터'],
    ['<b>영단주택</b>', '철거 전<br>기록으로 남김'],
  ]});
  await clue('youngdan');
  const pick = await choose('곧 사라질 우리 동네의 오래된 장소, 탐정단은 무엇을 할 수 있을까?', [
    '사진 한 장만 찍어 휴대폰에 저장한다',
    '사진·지도·주민 인터뷰를 함께 기록해서 **박물관과 친구들에게 공유**한다',
    '어차피 사라질 곳이니 아무것도 하지 않는다' ], '행동하기');
  if(pick === 1){ show('riri', 'happy', 'right'); await feedback({tag:'best', pts:10, fb:'여러 자료를 함께 남기고 **나누면** 기억은 더 오래 살아요. 이것이 읽걷쓰의 **쓰기**예요.'}, 'youngdan'); }
  else if(pick === 0){ await feedback({tag:'ok', pts:4, fb:'시작은 좋아요! 하지만 나만 보는 사진은 쉽게 잊혀요. 이야기와 함께 **공유**해 봐요.'}, 'youngdan'); }
  else { await feedback({tag:'low', pts:0, fb:'무관심은 기억까지 지워요. 작은 기록 하나가 100년 뒤 누군가에겐 소중한 자료가 돼요.'}, 'youngdan'); }
  visited('youngdan');
}

/* =====================================================================
   7장. 굴포천 [행동하기] — 되살릴 수 있다 + 세계시민
   ===================================================================== */
async function ch_gulpo(){
  await go('gulpo', 'gulpo');
  show('minjun', 'happy', 'left');
  await say('minjun', '와, 물이 흐른다! 오리도 있어! 여긴 기분이 좋다~');
  show('riri', 'happy', 'right');
  await say('riri', '여기는 **굴포천**이야. 1990년대에 콘크리트로 덮여서 물길이 사라졌었대.');
  await say('riri', '그런데 사람들이 힘을 모아 **2025년 12월**, 약 1.5km 구간이 생태하천으로 다시 태어났어!');
  await clue('gulpo');
  show('minjun', 'think', 'left');
  await say('minjun', '사라진 것도 다시 살릴 수 있구나. 그럼 우리 탐정단이 한 일도 의미가 있겠네!');
  show('riri', 'think', 'right');
  await say('riri', '그리고 이건 인천만의 이야기가 아니야. 세계 곳곳에서도 개발이나 전쟁, 무관심으로 유산이 사라지고 있거든.');
  await say('riri', '그래서 세계는 문화유산을 **인류 모두의 것**으로 함께 지키기로 약속했어.');
  await clue('unesco');
  const pick = await choose('인천의 어린이 탐정이 **세계시민**으로서 할 수 있는 일은?', [
    '우리 동네 일은 세계와 상관없으니 신경 쓰지 않는다',
    '우리 동네 유산을 **읽고·걷고·써서** 기록하고, 다른 지역·나라 친구들과도 **나눈다**',
    '유명한 외국 유적만 중요하니 그것만 공부한다' ], '행동하기 · 세계시민');
  if(pick === 1){ show('riri', 'happy', 'right'); hop('riri'); await feedback({tag:'best', pts:10, fb:'정답! **우리 동네를 아끼는 마음이 세계를 아끼는 마음**으로 이어져요. 인천에서 시작하는 작은 기록이 세계시민의 첫걸음이에요.'}, 'gulpo'); }
  else if(pick === 2){ await feedback({tag:'low', pts:0, fb:'세계의 유산도 소중하지만, 우리 곁의 유산을 지키는 것부터가 세계시민의 시작이에요.'}, 'gulpo'); }
  else { await feedback({tag:'low', pts:0, fb:'우리 동네의 역사도 **인류의 역사**의 한 조각이에요. 강제동원, 만세운동 같은 기억은 세계의 인권·평화와 이어져 있어요.'}, 'gulpo'); }
  visited('gulpo');
}

/* =====================================================================
   8장. 본부로 돌아와 — 안내판 쓰기와 인증서
   ===================================================================== */
const AI_HELP = {
  '부평도호부 관아':'이곳은 조선 시대 부평 고을을 다스리던 관청이 있던 자리예요.',
  '계양산성':'계양산성에서는 1500년도 더 된 『논어』 목간이 나왔어요.',
  '황어장터':'1919년 3월 24일, 이곳 황어장터에서 만세 소리가 울려 퍼졌어요.',
  '부평 미쓰비시 줄사택':'이 집들은 일제강점기에 강제로 끌려온 노동자들이 살던 곳이에요.',
  '캠프마켓(옛 조병창)':'이곳에는 일제강점기에 일본군의 무기 공장이 있었어요.',
  '부평 영단주택':'이곳에는 80년 넘게 노동자 가족들이 살던 마을이 있었어요.',
};
async function ch_final(){
  G.place = 'office'; hideAll(); hideText(); bg('office'); await wait(500);
  await placeCard({ name:'다시 탐정단 본부로', step:'행동하기', topic:'기록하고, 알리고, 약속하기' });
  show('curator', 'smile', 'center');
  await say('curator', '{name} 탐정, 수고 많았어요! 탐정 수첩이 증거 카드로 가득하네요.');
  await say('curator', '마지막 임무예요. 지킬 곳 하나를 골라 **우리 동네 문화유산 안내판**을 써 주세요. 박물관 게시판에 붙일 거예요.');
  show('riri', 'normal', 'right');
  await say('riri', '내가 첫 문장을 도와줄 수도 있어. 대신 **생각의 주인은 너**야. 도움받았다면 솔직하게 밝혀 줘!');
  const w = await gameWrite({ sites:Object.keys(AI_HELP), aiText:AI_HELP });
  G.flags.sign = w;
  let pts = 10, tags = ['안내판 완성 +10'];
  if(w.usedAI && w.disclosed){ pts += 5; tags.push('AI 도움 솔직하게 밝힘 +5'); }
  else if(!w.usedAI){ pts += 5; tags.push('스스로 쓰기 +5'); }
  else { tags.push('AI 도움을 밝히지 않음 +0'); }
  addScore(pts); snd('sfx_best'); G.log.push({title:'final', tag:'best', pts});
  await card('안내판이 세워졌어요!', `「${w.site}」<br>“${w.text}”` + (w.usedAI && !w.disclosed ? '<br><br><span style="font-size:32px;color:#d0664c">리리의 도움을 받았다면 꼭 밝혀 주세요. 그게 AI 시대의 정직한 글쓰기예요.</span>' : ''), '#3f8f80', tags);
  show('riri', 'happy', 'right'); show('minjun', 'happy', 'left');
  await say('minjun', '우리 탐정단 진짜 멋졌다! 다음엔 우리 학교 근처도 조사해 보자!');
  await say('riri', '오늘 우리는 **읽고**(자료와 AI를 확인하고), **걷고**(현장을 찾아가고), **쓰며**(기록하고 알리며) 인천을 지켰어.');
  await say('riri', '우리 동네의 기억을 지키는 일은 세계의 기억을 지키는 일이야. **인천에서 읽걷쓰 AI로 자라는 세계시민, {name}!**');
  playMusic('bgm_calm');
  bg('ending'); hideAll(); hideText(); await wait(900);
  snd('sfx_fanfare');
  visited('office');
  await certificate();
}

const MAX_SCORE = 10 * 8 + 15 + 12 + 12 + 12 + 15 + 16 + 15; // 선택 8 + 게임 7
function rankOf(s){
  const r = s / MAX_SCORE;
  if(r >= .85) return ['문화유산 명탐정', '🏆'];
  if(r >= .65) return ['수석 역사 탐정', '🥇'];
  if(r >= .45) return ['역사 탐정', '🔎'];
  return ['견습 탐정', '🌱'];
}
function certificate(){
  const [rank, icon] = rankOf(G.score);
  const sign = G.flags.sign || { site:'', text:'' };
  const html = `<div class="cert">
      <div style="font-size:34px;color:#8a7f73" class="jua">부평·계양 문화유산 탐정단</div>
      <h1>${icon} 탐정 인증서</h1>
      <div class="rank">${esc(G.name)} · ${esc(rank)}</div>
      <div class="stats"><span>점수 ${G.score} / ${MAX_SCORE}</span><span>증거 카드 ${G.clues.length} / ${Object.keys(CLUES).length}</span><span>조사한 곳 ${G.visited.length}곳</span></div>
      <div class="quote">「${esc(sign.site)}」 안내판: “${esc(sign.text)}”</div>
      <p>위 어린이는 부평과 계양의 사라져 가는 문화유산을 <b>읽고, 걷고, 쓰며</b> 조사하고,<br>AI의 정보도 사실인지 확인하는 지혜를 보여 주었기에 이 인증서를 드립니다.</p>
      <div class="msg">우리 동네의 기억을 지키는 것, 그것이 세계시민의 첫걸음!</div>
    </div>`;
  $('#print-area').innerHTML = html;
  return new Promise(resolve => {
    const render = () => {
      const el = openOverlay(`<div class="dim" style="background:rgba(43,42,54,.35)">${html}
        <div style="display:flex;gap:24px"><button class="big teal" id="cNote">📓 수첩 보기</button><button class="big sub" id="cPrint">🖨️ 인쇄하기</button><button class="big" id="cAgain">처음으로 ↺</button></div></div>`);
      el.querySelector('#cNote').onclick = () => openNotebook(true, render);
      el.querySelector('#cPrint').onclick = () => window.print();
      el.querySelector('#cAgain').onclick = () => { closeOverlay(); clearSave(); resolve(); };
    };
    render();
  });
}

/* ---------- 장(章) 순서 ---------- */
const CHAPTERS = [ch_intro, ch_dohobu, ch_sanseong, ch_hwangeo, ch_jul, ch_camp, ch_youngdan, ch_gulpo, ch_final];

main();
