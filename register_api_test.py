import requests
import random

BASE_URL = 'https://api.example.com/' #임의 URL, 실제 API 엔드포인트로 변경해야 합니다.
PATH = 'api/register'
RAND_LOWER = 1
RAND_UPPER = 10000000

#{"status": "success","statusCode": X00,"message": <MSG>}

#POST 요청을 보내는 유틸리티 메소드
#이 메소드는 새로운 유저를 생성하기 위해 Post 요청을 보냅니다.
#반환값은 JSON 형식의 API 응답입니다.
def send_post_request(data):
    """Utility method to send a Post request to create a new user.
        :return: API Response in JSON format
    """
    url = BASE_URL + PATH
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

#TC_POST_001: 유효한 이메일과 최소 8자의 비밀번호로 유저 등록
def register_new_valid_user():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com", # 랜덤 변수를 이메일 문자열에 추가하여 충돌 방지
        "password": "supersecret!"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200

#TC_POST_002: 대소문자 혼합된 이메일로 유저 등록
def register_mixed_case():
    data = {
        "email": f"JohnDoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",  # 랜덤 변수를 이메일 문자열에 추가하여 충돌 방지
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200

#TC_POST_003: 유효한 길이의 비밀번호로 유저 등록
def register_valid_length_password():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",
        "password": "validpassword123!" #최소 8자 이상
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200

#TC_POST_004: 특수문자가 포함된 비밀번호로 유저 등록    
def register_special_characters_password():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",
        "password": "P@ssw0rd!123"  # 특수문자 포함
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200

#TC_POST_005: 최대 길이 비밀번호로 유저 등록
#최대 길이 비밀번호는 128자로 가정
def register_max_length_password():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",
        "password": "X" * 128  # 최대 길이 비밀번호 (128자)
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200


#Boundary Test Cases
#TC_BOUNDARY_001: 비밀번호가 7자인 경우
def register_password_boundary():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",
        "password": "1234567"  # 7자 비밀번호
    }
    response = send_post_request(data)
    assert response['statusCode'] == 400
    assert response['message'] == '비밀번호는 8자 이상이어야 합니다.'


#EDGE TEST CASES
#TC_EDGE_001: 이메일에 숫자만 포함된 유저 등록
def register_numeric_email():
    data = {
        "email": f"{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",  # 숫자만 포함된 이메일
        "password": "validpassword123!"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200

#TC_EDGE_002: 이메일에 하이픈과 밑줄이 포함된 유저 등록
def register_hyphen_underscore_email():
    data = {
        "email": f"john-doe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",  # 하이픈과 밑줄 포함
        "password": "validpassword123!"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200

#TC_EDGE_003: 이메일에 공백 포함 (양끝)
def register_email_with_spaces():
    data = {
        "email": f" johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com ",  # 이메일 양끝에 공백 포함
        "password": "validpassword123!"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200
    #트리밍 여부에 따라 다르게 처리될 수 있음    

#TC_EDGE_004: 비밀번호에 연속된 숫자 포함
def register_password_with_consecutive_numbers():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",
        "password": "12345678"  # 연속된 숫자 포함
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200
    #보안 정책이나 필요정책에 따라 다르게 처리될 수 있음

#TC_EDGE_005: 비밀번호에 연속된 문자 포함   
def register_password_with_consecutive_letters():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",
        "password": "abcdefgh"  # 연속된 문자 포함
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200
    #보안 정책이나 필요정책에 따라 다르게 처리될 수 있음

#NEGATIVE TEST CASES
#TC_NEG_001: 중복된 이메일로 유저 등록
def register_duplicate_user():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER,RAND_UPPER)}@example.com",
        "password": "supersecret!"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 200

    duplicate_response = send_post_request(data)
    assert duplicate_response['statusCode'] == 400
    assert duplicate_response['message'] == 'User already exists'

#TC_NEG_002: 유효하지 않은 길이의 비밀번호로 유저 등록
def register_new_user_invalid_length_password():
    data = {
        "email": f"johndoe_{random.randint(RAND_LOWER, RAND_UPPER)}@example.com",
        "password": "short"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 400
    assert response['message'] == '비밀번호는 8자 이상이어야 합니다.'

#TC_NEG_003: 이메일 도메인이 누락된 유저 등록
def register_new_user_missing_email_domain():
    data = {
        "email": "johndoe",
        "password": "XXXXXXXXXXX!"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 400
    assert response['message'] == '이메일 형식이 잘못되었습니다.'

#TC_NEG_004: 유효하지 않은 이메일 형식으로 유저 등록
def register_new_user_invalid_email_format():
    data = {
        "email": "johndoeexample.com",
        "password": "XXXXXXXXXXX!"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 400
    assert response['message'] == '이메일 형식이 잘못되었습니다.'

#TC_NEG_005: 이메일 누락된 유저 등록
def register_new_user_missing_email():
    data = {
        "password": "XXXXXXXXXXX!"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 400
    assert response['message'] == '이메일을 입력해주세요.'

#TC_NEG_006: 비밀번호 누락된 유저 등록
def register_new_user_missing_password():
    data = {
        "email": "johndoe@example.com"
    }
    response = send_post_request(data)
    assert response['statusCode'] == 400
    assert response['message'] == '비밀번호를 입력해주세요.'


if __name__=="__main__":
    register_new_valid_user()
    register_duplicate_user()
    register_new_user_invalid_length_password()
    register_new_user_missing_email_domain()
    register_new_user_invalid_email_format()
    register_new_user_missing_email()
    register_new_user_missing_password()


# Assumption: JSON 형식의 API 응답은 {"status": "success","statusCode": X00,"message": <MSG>}입니다. 
# Assumption: 이메일 유효성 검사는 도메인 확인이 아닌 정규식 검사만 수행합니다.
# Assumption: 비밀번호 유효성 검사는 복잡도가 아닌 길이만 확인합니다.
# Assumption: 비밀번호의 최대 길이는 128자입니다.
# Assumption: API는 이러한 테스트에 대해 속도 제한이나 CAPTCHA를 적용하지 않습니다.