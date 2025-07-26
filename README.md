# himalaya.justbetemple.org 웹사이트

[![Website](https://img.shields.io/badge/Website-himalaya.justbetemple.org-blue.svg)](https://himalaya.justbetemple.org)

> justbetemple의 히말라야 트레킹 및 여행 정보 제공을 위한 서브 웹사이트입니다.
> 이 저장소는 해당 웹사이트를 구성하는 정적 파일(HTML, CSS, JS)을 관리합니다.

---

## 🏔️ 프로젝트 소개 (About This Project)

이 웹사이트는 [justbetemple.org](https://justbetemple.org)의 메인 서비스와는 별도로, 히말라야 지역에 특화된 정보를 제공하기 위해 만들어졌습니다. GitHub Pages를 통해 호스팅되며, 방문자들에게 아래와 같은 정보를 제공하는 것을 목표로 합니다.

## ✨ 주요 기능 및 내용 (Features)

* **JustBe 히말라야 불사 모연 안내**: JustBe 히말라야 불사에 대한 상세한 안내

* **히말라야 지역 소개**: 지역의 문화와 자연 환경에 대한 설명
* **주요 트레킹 코스 안내**: 코스별 난이도, 기간, 상세 경로 정보 제공
* **여행 사진 갤러리**: 전문 작가와 여행객들이 직접 찍은 생생한 사진 모음
* **여행 준비물 및 팁**: 고산병 예방, 필수 장비, 현지 에티켓 등 실용적인 정보

## 🛠️ 사용 기술 (Tech Stack)

* **`HTML5`**
* **`CSS3`**
* **`JavaScript`**
* **Hosting**: `GitHub Pages`

## 🚀 로컬에서 확인하는 방법 (Getting Started Locally)

1.  이 저장소를 로컬 컴퓨터로 복제(Clone)합니다.
    ```bash
    git clone [https://github.com/](https://github.com/)[Your-GitHub-Username]/[Your-Repository-Name].git
    ```
    2.  프로젝트 폴더로 이동합니다.
    ```bash
    cd [Your-Repository-Name]
    ```

3.  `index.html` 파일을 웹 브라우저에서 직접 열어서 확인합니다.

## 📊 동참자 수 관리 (Donor Count Management)

동참자 수는 `data/donors.json` 파일에서 관리됩니다.

### 업데이트 방법:
1. GitHub에서 `data/donors.json` 파일 편집
2. `"count"` 값만 변경 (예: `68` → `75`)
3. "Commit changes" 버튼으로 저장
4. 웹사이트에서 자동으로 업데이트된 숫자 확인

### JSON 파일 구조:
```json
{
  "count": 76,
  "goal": 300,
  "lastUpdated": "2025-01-25T12:00:00Z",
  "updatedBy": "관리자"
}
```
