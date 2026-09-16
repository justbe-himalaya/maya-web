#!/usr/bin/env python3
"""Build data/sosik.json (public "소식방 엿보기" feed) from a KakaoTalk open-chat CSV export.

The chat room is for 한평 불사 participants, so the raw export contains member names
(join/leave records) and must never be published. This script keeps only posts written by
the JustBe team, drops system/bot/deleted messages, masks phone numbers, and removes posts
listed in EXCLUDE.

Usage: python3 scripts/build-sosik.py [resource/doc/sosik.csv] [data/sosik.json]
"""
import csv
import json
import re
import sys
from datetime import datetime

src = sys.argv[1] if len(sys.argv) > 1 else "resource/doc/sosik.csv"
dst = sys.argv[2] if len(sys.argv) > 2 else "data/sosik.json"

# 카카오톡 표시 이름 -> 홈페이지 표시 이름 / 아바타 키
TEAM = {
    "준한Junehan": ("준한 스님", "junhan"),
    "JustBe Himalaya": ("JustBe Himalaya", "justbe"),
    "seungwon(승원)🙏": ("승원", "seungwon"),
    "마승": ("마승", "maseung"),
    "진태진": ("중현", "junghyun"),
    "이슬기(Seulgi Lee)": ("이슬기", "seulgi"),
    "지웅 G": ("지웅", "jiwoong"),
}

SYSTEM = re.compile(
    r"(joined this chatroom|left this chatroom|assigned as the admin|no longer an admin|"
    r"has been deleted|hidden by the managers|^KakaoTalk Profile$|^/\S+\s*$)"
)
# 공개 페이지에 올리지 않을 게시글 (본문 앞부분으로 식별)
EXCLUDE = [
    "반가운 새 가족",  # 스태프 자녀(영아) 이름·나이 소개
]
PHONE = re.compile(r"01[016789][-. ]?\d{3,4}[-. ]?\d{4}")
MEDIA = re.compile(r"^(?:(\d+) photos|Photo|Video)$")
URL = re.compile(r"https?://\S+")
YOUTUBE = re.compile(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|live/|shorts/))([\w-]{11})")


def link_card(url):
    yt = YOUTUBE.search(url)
    if yt:
        return {"kind": "youtube", "url": url, "id": yt.group(1)}
    host = re.sub(r"^www\.", "", url.split("/")[2])
    return {"kind": "link", "url": url, "host": host}


rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
items, seen_text = [], set()
for r in rows:
    user, msg, date = r["User"], r["Message"].strip(), r["Date"].strip()
    if user not in TEAM or not date or SYSTEM.search(msg):
        continue
    if any(msg.startswith(x) or x in msg[:40] for x in EXCLUDE):
        continue
    if msg.startswith("Announcement in Boards: "):
        msg = msg[len("Announcement in Boards: "):]
    msg = PHONE.sub("(연락처는 소식방에서 확인)", msg)
    name, avatar = TEAM[user]
    ts = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    item = {"t": ts.strftime("%Y-%m-%dT%H:%M"), "who": name, "av": avatar}

    m = MEDIA.match(msg)
    if m:
        item["media"] = "video" if msg == "Video" else "photo"
        item["n"] = int(m.group(1)) if m.group(1) else 1
    elif URL.fullmatch(msg):
        item["card"] = link_card(msg)
    else:
        key = re.sub(r"\s+", "", msg)[:120]
        if key in seen_text:  # 공지 재게시 중복 제거
            continue
        seen_text.add(key)
        item["text"] = msg
        urls = URL.findall(msg)
        if urls:
            item["card"] = link_card(urls[-1].rstrip(").,"))
    items.append(item)

items.sort(key=lambda x: x["t"])

# ---- 스토리 묶기: 같은 사람이 20분 안에 이어 올린 글·사진·링크는 한 스토리 ----
TOPICS = ["순례", "수행·법회", "불사 현장", "사람들", "라이브·영상", "언론", "나눔·구호"]
# 첫 게시 시각 -> (제목, 주제). 여기 없는 스토리는 첫 줄로 제목을 자동 생성한다.
STORIES = {
    "2026-02-09T21:40": ("소식방을 열며, 두 손 모아", ["수행·법회"]),
    "2026-02-15T11:30": ("청년불자 리더 스무 명, 선명상 트레킹 1기", ["순례", "사람들"]),
    "2026-02-17T06:49": ("보리수 아래에서 올린 새해 발원", ["수행·법회"]),
    "2026-02-17T19:02": ("후원자님들께 드리는 새해 인사", ["사람들"]),
    "2026-02-18T13:23": ("방사 완성, 이제 템플스테이를 할 수 있어요", ["불사 현장", "언론"]),
    "2026-02-18T13:35": ("제3차 원정대 · 템플스테이 모집", ["순례"]),
    "2026-02-20T19:37": ("4·5월 템플스테이 안내", ["순례"]),
    "2026-02-21T11:43": ("네팔 부처님 오신 날로의 초대", ["순례"]),
    "2026-02-23T14:29": ("BBS 뉴스에 소개된 히말라야 선원", ["언론"]),
    "2026-02-23T18:36": ("1년 전, 포카라 언덕의 작은 게스트하우스", ["불사 현장"]),
    "2026-02-26T13:23": ("부처님 오신 날 성지순례단 모집", ["순례"]),
    "2026-02-26T14:17": ("푼힐 트레킹, 누구나 걸을 수 있어요", ["순례"]),
    "2026-03-01T09:33": ("구법순례 45명, 선원에서 회향 수계식", ["순례", "수행·법회"]),
    "2026-03-01T13:34": ("모두 떠난 다음날, 스태프 화보", ["사람들"]),
    "2026-03-04T16:23": ("현대불교신문 기고", ["언론"]),
    "2026-03-06T18:51": ("특별순례 자주 묻는 질문 TOP 5", ["순례"]),
    "2026-03-10T11:46": ("공항에서 만난 엄홍길 대장님", ["사람들"]),
    "2026-03-18T08:56": ("봄맞이 제2회 수계 법회", ["수행·법회"]),
    "2026-03-18T15:34": ("부처님 오신 날 프리뷰 라이브 토크", ["라이브·영상"]),
    "2026-03-20T10:48": ("국회정각회, 히말라야 선원을 찾다", ["순례", "사람들"]),
    "2026-03-24T06:25": ("준한 스님이 보내온 영상 한 편", ["라이브·영상"]),
    "2026-03-28T12:45": ("부처님 오신 날 특별순례 모집 마감", ["순례"]),
    "2026-03-28T14:18": ("오늘 아침, 뒤에 광명이 멋지죠?", ["불사 현장"]),
    "2026-04-14T08:44": ("네팔은 오늘 2083년 새해", ["사람들"]),
    "2026-04-14T13:16": ("지금, 다시 태어나기", ["수행·법회"]),
    "2026-04-16T11:58": ("법장스님과 창원 순례단의 방문", ["순례"]),
    "2026-04-18T13:29": ("이웃 티베트 사원 스님의 방문", ["사람들"]),
    "2026-04-24T09:34": ("첫 초파일, 수정 연등을 밝히다", ["수행·법회", "불사 현장"]),
    "2026-05-01T08:52": ("네팔 '부처님의 날' 아침에", ["수행·법회"]),
    "2026-05-12T16:22": ("첫 봉축법회 회향, 9월부터 법당 공사", ["수행·법회", "불사 현장"]),
    "2026-05-25T17:30": ("뉴욕 조계사 첫 봉축법회, 일생일대의 실수", ["수행·법회"]),
    "2026-06-12T08:19": ("'딱 3개월만' 했던 행자 생활이 출가로", ["사람들"]),
    "2026-06-13T06:15": ("새 행자님의 출가 삭발식", ["수행·법회", "사람들"]),
    "2026-06-18T09:13": ("포카라에서 올린 한국의 천수경", ["수행·법회"]),
    "2026-06-19T18:49": ("불금 라이브", ["라이브·영상"]),
    "2026-06-26T15:38": ("우기의 히말라야, 천둥번개 치는 저녁", ["불사 현장"]),
    "2026-07-03T10:09": ("우기에 열린 설산, 그리고 현대불교 기사", ["언론"]),
    "2026-07-05T09:06": ("JustBe 히말라야 첫 유튜브 라이브", ["라이브·영상"]),
    "2026-07-05T18:49": ("첫 라이브, 떨리네요", ["라이브·영상"]),
    "2026-07-12T18:00": ("순례 일정, 조금만 더 기다려 주세요", ["순례"]),
    "2026-07-14T13:05": ("웃음 한 스푼, 쇼츠 공유", ["라이브·영상"]),
    "2026-07-14T14:55": ("한가위를 히말라야 무스탕에서", ["순례"]),
    "2026-07-15T08:44": ("스튜디오 랜선 차담 라이브", ["라이브·영상"]),
    "2026-07-15T18:55": ("한가위 & 개원법회 순례 안내", ["순례"]),
    "2026-08-03T14:30": ("개원법회 순례 모집 마감", ["순례"]),
    "2026-08-04T08:58": ("동참 1,000명을 앞두고, 법당 설계하러 네팔로", ["불사 현장"]),
    "2026-08-06T08:07": ("봉철대선사 15주기 다례재 안내", ["수행·법회"]),
    "2026-08-07T09:14": ("천상천하 명당, 내가 서 있는 자리", ["불사 현장"]),
    "2026-08-09T12:26": ("한가위 순례 사전 답사기", ["순례"]),
    "2026-08-15T08:15": ("광복절, 별을 노래하는 마음으로", ["수행·법회"]),
    "2026-08-15T11:27": ("홍대선원 4주년 파티에 초대합니다", ["사람들"]),
    "2026-08-22T07:41": ("조계사 대웅전 싯다르타 순례길 법문", ["수행·법회"]),
    "2026-08-22T14:04": ("성지순례 모집 현황 안내", ["순례"]),
    "2026-08-27T07:34": ("하안거 해제 덕담", ["수행·법회"]),
    "2026-08-27T16:46": ("네팔 홍수, 도량 지역 상황 안내", ["나눔·구호"]),
    "2026-08-29T07:15": ("네팔 재해 긴급 구호 성금", ["나눔·구호"]),
    "2026-09-01T09:25": ("3일 만에 400명, 5천만 원의 마음", ["나눔·구호"]),
    "2026-09-05T07:57": ("홍대선원 개원 4주년", ["사람들"]),
    "2026-09-06T17:09": ("4주년 법회, 감사 인사", ["사람들"]),
    "2026-09-07T11:01": ("4주년 법회를 마치며, 청년들에게", ["사람들"]),
    "2026-09-07T13:39": ("4년의 기록, 영상과 사진", ["라이브·영상"]),
    "2026-09-07T19:51": ("구호성금 1차 현지 보고: 무너진 다리를 잇다", ["나눔·구호"]),
}
# 공개하지 않는 스토리: 단순 알림 반복, 연락처 안내, 영아 사진, 설명 없는 단독 미디어
DROP = {
    "2026-02-26T14:48", "2026-03-18T18:26", "2026-03-20T09:59", "2026-04-03T08:33",
    "2026-04-29T11:19", "2026-07-05T18:43", "2026-07-05T19:51", "2026-07-15T18:49",
    "2026-09-05T17:38",
}
# 앞 스토리에 붙일 후속 미디어/링크
MERGE = {"2026-05-25T19:17": "2026-05-25T17:30", "2026-06-13T09:54": "2026-06-13T06:15",
         "2026-09-01T10:27": "2026-09-01T09:25"}

groups = []
for x in items:
    t = datetime.fromisoformat(x["t"])
    g = groups[-1] if groups else None
    if g and g["who"] == x["who"] and (t - g["_last"]).total_seconds() <= 20 * 60:
        g["_items"].append(x)
        g["_last"] = t
    else:
        groups.append({"id": x["t"], "who": x["who"], "av": x["av"], "_last": t, "_items": [x]})

by_id = {g["id"]: g for g in groups}
for src_id, dst_id in MERGE.items():
    if src_id in by_id and dst_id in by_id:
        by_id[dst_id]["_items"] += by_id.pop(src_id)["_items"]
groups = [g for g in by_id.values() if g["id"] not in DROP]

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]")


def auto_title(text):
    for line in text.splitlines():
        line = EMOJI.sub("", line).strip(" <>[]-~.·")
        if len(line) >= 6:
            return line[:40]
    return "히말라야 소식"


stories = []
for g in sorted(groups, key=lambda g: g["id"]):
    texts = [i["text"] for i in g["_items"] if "text" in i]
    cards = []
    for i in g["_items"]:
        c = i.get("card")
        if c and c["url"] not in [k["url"] for k in cards]:
            cards.append(c)
    photos = sum(i["n"] for i in g["_items"] if i.get("media") == "photo")
    videos = sum(i["n"] for i in g["_items"] if i.get("media") == "video")
    if not texts and not cards:
        continue
    title, tags = STORIES.get(g["id"], (auto_title("\n".join(texts)), []))
    stories.append({"id": g["id"], "who": g["who"], "av": g["av"], "title": title, "tags": tags,
                    "text": "\n\n".join(texts), "photos": photos, "videos": videos, "cards": cards})

json.dump({"generated": datetime.now().strftime("%Y-%m-%d"), "topics": TOPICS, "stories": stories},
          open(dst, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(f"{len(stories)} stories -> {dst}")
