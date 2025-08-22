# Fundamental Web Login Scripts (Selenium + Python/Reqests)

This repo demonstrates QA automation practices(mainly log-in functionality):
- ✅ UI automation (Selenium + Pytest)
- ✅ API automation (Python + Requests)



# API UI 테스트 스크립트 
## 🚀 주요 기능

- **POST /api/register** 엔드포인트 테스트
- 랜덤 이메일 생성으로 **중복 충돌 방지**
- **Positive / Boundary / Edge / Negative** 시나리오 커버
- `statusCode` 및 `message` 값에 대한 **명확한 단언(assert)**

---

## 📝 테스트 가정 (Assumptions)

- 응답 JSON 스키마:  
  ```json
  { "status": "success", "statusCode": X00, "message": "<MSG>" }

## 설치 및 실행





# WEB UI 회원가입 테스트 스크립트

## 목적
이 스크립트는 Selenium을 이용하여 웹사이트의 회원가입 및 로그인 기능을 자동화 테스트합니다. 테스트는 기능 명세에 기반하여 정상, 경계값, 비정상, 보안 흐름을 검증하도록 설계되었습니다.

## 테스트 전 가정 및 주의사항 
테스트 대상 웹사이트 주소(URL) 및 XPath는 실제 환경에 맞게 조정되어야 합니다.

Alert 메시지는 시스템 요구사항에 따라 조정 필요합니다.

테스트 수행 시 실제 회원가입이 발생하므로, 중복 이메일 검증이 필수입니다.

## 사전 설치 항목
1. Python 3.7 이상
2. Google Chrome 브라우저 설치
3. ChromeDriver 
    - 본인의 크롬 브라우저 버전에 맞는 ChromeDriver를 https://chromedriver.chromium.org 에서 다운로드
    - ChromeDriver의 경로를 시스템 환경변수(PATH)에 추가 또는 코드 내에서 경로 지정 필요 

## 파일 설명
- `register_ui_test.py`: 회원가입 및 로그인 UI 테스트를 위한 Python 스크립트입니다.

## 실행 방법

1. **필수 패키지 설치**
   ```bash
   pip install selenium
   ```
   크롬 브라우저와 [ChromeDriver](https://chromedriver.chromium.org/downloads)가 필요합니다.

2. **테스트 실행**
   ```bash
   python register_ui_test.py
   ```
   특정 테스트 함수만 실행하고 싶을 경우, 실행하고자 하는 메서드명을 if __name__ == "__main__" 블록 아래에 직접 호출하면 됩니다.

   예시: 
   ```
   if __name__ == "__main__":
   page.sign_up_blank_credentials()
   page.sign_up_duplicate_credentials(user_name, password)
   page.sign_up_duplicate_credentials(user_name, password)

    ```

3. **테스트 시나리오 요약**
   - 유효한 이메일/비밀번호 입력 시 회원가입 성공
   - 잘못된 이메일 형식, 짧은 비밀번호, 중복 이메일 등 에러 상황 검증
   - 보안 테스트: XSS, SQL Injection 등 입력 필터링 확인
   - 로그인 기능 동작 확인

## 주요 클래스 및 함수

- [`TestRegisterUI`](register_ui_test.py): 회원가입 및 로그인 테스트를 위한 클래스
  - `sign_up(user_email, password)`: 회원가입 테스트
  - `sign_up_duplicate_credentials()`: 중복 계정 테스트 
  - `sign_up_blank_credentials()`: 빈칸으로 회원가입 테스트 
  - `sign_up_invalid_email()`: 이메일 도메인에 @가 없는 경우 회원가입 테스트
  - `log_in(user_name, password)`: 로그인 테스트

## 참고
- 모든 테스트들은 가정 기반으로 작성되었습니다 
- 테스트 결과는 웹사이트의 알림창(alert) 메시지로 검증합니다.
- 테스트 시 실제로 회원가입이 이루어지므로, 반복 실행 시 중복 가입 테스트도 가능합니다.
- XSS, SQL injection 스크립트는 로컬 테스트 환경과 스테이징 환경에서만 시용해야 합니다. 
