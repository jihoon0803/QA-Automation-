import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

RAND_LOWER = 10000000
RAND_UPPER = 99999999
TIMEOUT = 15 #인터넷 속도에 따라 변경 가능

class TestRegisterUI:
    """회원가입 기능 테스트 클래스"""
    def __init__(self, driver):
        self.driver = driver
        self.driver.get("https://test.example.com/register")  # 실제 테스트할 URL로 변경 필요, 지금은 빈 문자열로 설정되어 있음
        self.driver.implicitly_wait(TIMEOUT) # 요소가 로드될 때까지 최대 TIMEOUT 초 대기
        
        # 회원가입 요소 정리
        # 모든 요소는 XPATH로 정의; 이는 페이지 구조가 변경되더라도 유연하게 대응할 수 있도록 함
        # 실제 테스트 URL에 맞게 XPATH를 조정해야 할 수 있음; 임의로 XPATH 설정
        self.sign_up_link = (By.XPATH, "//a[@id='signup']")
        self.useremail_field = (By.XPATH, "//input[@id='sign-username']")
        self.password_field = (By.XPATH, "//input[@id='sign-password']")
        self.sign_up_button = (By.XPATH, "//button[normalize-space()='Sign up']")


        # 로그인 요소 정리
        # 위와 같이 로그인 관련 요소도 XPATH로 정의, 임의로 XPATH 설정
        self.log_in_link = (By.XPATH, "//a[@id='login2']")
        self.log_in_useremail_field = (By.XPATH, "//input[@id='loginuseremail']")
        self.log_in_password_field = (By.XPATH, "//input[@id='loginpassword']")
        self.log_in_button = (By.XPATH, "//button[normalize-space()='Log in']")
        self.name_of_user = (By.XPATH, "//a[@id='nameofuser']")

    #alert 메시지 확인 
    def handle_alert(self, expected_message):
        time.sleep(5)  # 알림이 나타날 때까지 대기
        alert = self.driver.switch_to.alert
        assert alert.text == expected_message, f"Actual Alert Text: {alert.text}"
        alert.accept()

    #페이지 회원가입
    def sign_up(self,user_email,password):
        """Sign up to the DemoBlaze website"""
        self.driver.find_element(*self.sign_up_link).click()
        WebDriverWait(self.driver,TIMEOUT).until(EC.visibility_of_element_located(self.useremail_field))
        self.driver.find_element(*self.username_field).send_keys(f"{user_email}")
        self.driver.find_element(*self.password_field).send_keys(f"{password}")
        self.driver.find_element(*self.sign_up_button).click()
        self.handle_alert("회원가입이 완료되었습니다")


    #중복 회원가입 시도
    def sign_up_duplicate_credentials(self, user_email, password):
        self.driver.find_element(*self.sign_up_link).click()
        WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located(self.useremail_field))
        self.driver.find_element(*self.username_field).send_keys(f"{user_email}")
        self.driver.find_element(*self.password_field).send_keys(f"{password}")
        self.driver.find_element(*self.sign_up_button).click()
        self.handle_alert("이메일이 이미 존재합니다")
   
    
    # 회원가입 시도 시 빈칸으로 회원가입 시도
    def sign_up_blank_credentials(self):
        self.driver.find_element(*self.sign_up_link).click()
        WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located(self.useremail_field))
        self.driver.find_element(*self.username_field).send_keys("") # 빈 사용자 이름
        self.driver.find_element(*self.password_field).send_keys("") # 빈 비밀번호
        self.driver.find_element(*self.sign_up_button).click()
        self.handle_alert("이메일과 비밀번호를 입력해주세요")


    # 비밀번호 가 7자 경우 회원가입 시도 (경계값 테스트)
    def sign_up_boundary_password(self, user_email):
        self.driver.find_element(*self.sign_up_link).click()
        WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located(self.useremail_field))
        self.driver.find_element(*self.username_field).send_keys(f"{user_email}")
        self.driver.find_element(*self.password_field).send_keys("1234567") # 7자 비밀번호
        self.driver.find_element(*self.sign_up_button).click()
        self.handle_alert("비밀번호는 최소 8자 이상이어야 합니다.")

    #이메일 도메인에 @가 없는 경우 회원가입 시도
    def sign_up_invalid_email(self, user_name, password):
        self.driver.find_element(*self.sign_up_link).click()
        WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located(self.useremail_field))
        self.driver.find_element(*self.username_field).send_keys(f"{user_name}") # @가 없는 사용자 이름
        self.driver.find_element(*self.password_field).send_keys(f"{password}") 
        self.driver.find_element(*self.sign_up_button).click()    
        self.handle_alert("이메일 형식이 올바르지 않습니다.")
    
    #SQL Injection 공격 시도
    def sign_up_sql_injection(self, password):
        self.driver.find_element(*self.sign_up_link).click()
        sql_payload = "' OR '1'='1"
        self.driver.find_element(*self.useremail_field).send_keys(sql_payload) # SQL Injection 공격
        self.driver.find_element(*self.password_field).send_keys(f"{password}")
        self.driver.find_element(*self.sign_up_button).click()
        self.handle_alert("입력값이 올바르지 않습니다")

    
    #XSS 공격 시도
    def sign_up_xss_attack(self, password):
        self.driver.find_element(*self.sign_up_link).click()
        xss_payload = "<script>alert('XSS Attack');</script>"
        self.driver.find_element(*self.useremail_field).send_keys(xss_payload) # XSS 공격
        self.driver.find_element(*self.password_field).send_keys(f"{password}")
        self.driver.find_element(*self.sign_up_button).click()
        self.handle_alert("입력값이 올바르지 않습니다")


    #로그인 기능 테스트
    def log_in(self,user_email,password):
        """Log in to the DemoBlaze website"""
        self.driver.find_element(*self.log_in_link).click()
        WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located(self.log_in_useremail_field))
        self.driver.find_element(*self.log_in_username_field).send_keys(f"{user_email}")
        self.driver.find_element(*self.log_in_password_field).send_keys(f"{password}")
        self.driver.find_element(*self.log_in_button).click()
        WebDriverWait(self.driver, TIMEOUT).until(EC.visibility_of_element_located(self.name_of_user)) #페이지 로딩 대기
        #요구사항에 따라 메시지가 다를 수 있으므로, 실제 테스트 환경에 맞게 조정 필요
        assert self.driver.find_element(*self.name_of_user).text == f"환영합니다 {user_name}", f"Actual Text:  {self.driver.find_element(*self.name_of_user).text}"


#테스트 실행
if __name__=="__main__":
    driver = webdriver.Chrome()
    page = TestRegisterUI(driver)
    random_int = random.randint(RAND_LOWER, RAND_UPPER)
    user_email = f"johndoe_{random_int}@example.com" #도메인 포함 사용자 이메일 생성
    user_name = f"johndoe_{random_int}" #도메인 없이 사용자 이름 생성
    password = f"pw{random_int}"
    page.sign_up(user_name,password)
    page.log_in(user_name, password)
    page.sign_up_duplicate_credentials(user_name, password)
    driver.quit()  # 테스트 후 브라우저 닫기
    print("테스트 완료")