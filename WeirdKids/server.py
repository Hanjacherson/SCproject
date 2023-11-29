from flask import Flask, session, render_template, redirect, request, url_for, flash, jsonify
from datetime import datetime
import pymysql
import requests
import logging
from http import HTTPStatus

mysql = pymysql.connect(host="project-db-stu3.smhrd.com", 
                       db="Insa4_IOTB_final_4", 
                       user="Insa4_IOTB_final_4", 
                       password="aischool4", 
                       port=3307,
                       cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
app.secret_key = "12345"

# IFTTT 웹훅 URL
ifttt_webhook_url = 'https://maker.ifttt.com/trigger/dog_check_please/with/key/d4BLCPHNfnxfSnep3Vl4dw'

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.static_url_path = '/static'
app.static_folder = 'static'

def DQL(sql, params=None):
    cursor = mysql.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    return result

def DML(sql, params=None):
    cursor = mysql.cursor()
    cursor.execute(sql, params)
    mysql.commit()
    cursor.close()
    return "success!!"

@app.route('/home/', methods=['GET', 'POST'])
def home():
    error = None

    if 'login_user' not in session:
        return redirect(url_for('login'))

    user_id = session['login_user']

   # 펫 정보 및 보호자 닉네임 가져오기
    pet_info, guardian_nickname = get_pet_and_guardian_info(user_id)
    
    return render_template('home.html', error=error, user_id=user_id, pet_info=pet_info, guardian_nickname=guardian_nickname)


def get_pet_and_guardian_info(user_id):
    # 가상의 코드: 사용자의 강아지 정보와 보호자 닉네임을 데이터베이스에서 가져온다고 가정
    pet_sql = "SELECT pet_idx, pet_name, created_at FROM t_pet WHERE t_pet.id = %s"
    guardian_sql = "SELECT nick FROM t_member WHERE id = %s"
    
    pet_result = DQL(pet_sql, (user_id,))
    guardian_result = DQL(guardian_sql, (user_id,))

    # 펫 정보가 있다면 첫 번째 행을 사용
    if pet_result:
        pet_info = pet_result[0]
    else:
        pet_info = None

    # 보호자 닉네임이 있다면 첫 번째 행을 사용
    if guardian_result:
        guardian_nickname = guardian_result[0]['nick']
    else:
        guardian_nickname = None

    # 디버깅 메시지 추가
    print("pet_info:", pet_info)
    print("guardian_nickname:", guardian_nickname)

    return pet_info, guardian_nickname


def get_pet_info(user_id):
    # 가상의 코드: 사용자의 강아지 정보를 데이터베이스에서 가져온다고 가정
    sql = "SELECT pet_idx, pet_name, created_at FROM t_pet JOIN t_member USING (id) WHERE t_pet.id = %s"
    result = DQL(sql, (user_id,))

    # 결과가 있다면 첫 번째 행을 사용
    if result:
        pet_info = result[0]
        return pet_info

    # 결과가 없다면 None 반환
    return None


@app.route('/update_pet_info', methods=['POST'])
def update_pet_info_route():
    if 'login_user' not in session:
        return redirect(url_for('login'))

    user_id = session['login_user']
    pet_name = request.form.get['pet_name']
    pet_birth_year = request.form['pet_birth_year']
    pet_birth_month = request.form['pet_birth_month']
    pet_birth_day = request.form['pet_birth_day']
    pet_submit_type = request.form.get('pet_submit_type')

    # created_at 생성
    created_at = datetime(int(pet_birth_year), int(pet_birth_month), int(pet_birth_day)).date()

    if pet_submit_type == '강아지 등록':
        insert_pet_info(user_id, pet_name, created_at)
    elif pet_submit_type == '강아지 정보 수정':
        update_pet_info(user_id, pet_name, created_at)

    return redirect(url_for('home'))

def insert_pet_info(user_id, pet_name, created_at):
    update_pet_sql = "INSERT INTO t_pet (pet_name, created_at, id) VALUES (%s, %s, %s)"
    try:
        DML(update_pet_sql, (pet_name, created_at, user_id))
        flash('강아지 정보가 성공적으로 등록되었습니다.','success')
    except Exception as e:
        print("강아지 정보 등록 중 오류 발생:", str(e))
        flash('강아지 정보 등록 중 오류가 발생했습니다.', 'error')


def update_pet_info(user_id, pet_name, created_at):
    update_pet_sql = "UPDATE t_pet SET pet_name = %s, created_at = %s WHERE id = %s"
    try:
        DML(update_pet_sql, (pet_name, created_at, user_id))
        flash('강아지 정보가 성공적으로 수정되었습니다.','success')
    except Exception as e:
        print("강아지 정보 수정 중 오류 발생:", str(e))
        flash('강아지 정보 수정 중 오류가 발생했습니다.', 'error')    



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id = request.form['ID']
        pw = request.form['Password']
        email = request.form['Email']
        nick = request.form['Nickname']
        phone = request.form['Phone']

        # 중복 아이디 및 이메일 검사
        if check_duplicate(id, email):
            flash('가입 아이디 또는 이메일이 이미 존재합니다.')
            return redirect(url_for('signup'))


        # 현재 날짜 및 시간을 가져와서 joined_at에 할당
        joined_at = datetime.now()

        # 회원 정보를 데이터베이스에 삽입하는 쿼리
        sql = "INSERT INTO t_member (id, pw, email, nick, phone, joined_at) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            DML(sql, (id, pw, email, nick, phone, joined_at))
            success_message = '회원 가입이 성공적으로 완료되었습니다.'

            # 성공 메시지를 세션에 저장
            session['signup_success_message'] = success_message

            return redirect(url_for('login'))  # 회원 가입이 성공하면 로그인 페이지로 리디렉션
        except Exception as e:
            print("Error during signup:", str(e))
  

    return render_template('signup.html')


# 중복 아이디 및 이메일 검사 함수
def check_duplicate(id, email):
    sql_id_check = "SELECT id FROM t_member WHERE id = %s"
    sql_email_check = "SELECT email FROM t_member WHERE email = %s"

    # 아이디 중복 검사
    result_id = DQL(sql_id_check, (id,))
    if result_id:
        return True

    # 이메일 중복 검사
    result_email = DQL(sql_email_check, (email,))
    if result_email:
        return True

    return False


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        id = request.form['ID']  # 폼에서 ID 필드로 전송되는 값
        pw = request.form['Password']  # 폼에서 password 필드로 전송되는 값

        sql = "SELECT id FROM t_member WHERE id = %s AND pw = %s"
        user = DQL(sql, (id, pw))

        if user:
            session['login_user'] = id
            return redirect(url_for('home'))  # 'home' 함수로 리디렉션
        else:
            error = 'Invalid input data detected!'

             # 세션에서 회원가입 성공 메시지를 가져와서 표시
    signup_success_message = session.pop('signup_success_message', None)
    
    return render_template('login.html', error=error, signup_success_message=signup_success_message)

@app.route('/home/profile')
def profile():
    # 로그인한 사용자의 ID를 가져옵니다.
    if 'login_user' not in session:
        return redirect(url_for('login'))
    user_id = session['login_user']

    # 사용자 정보를 데이터베이스에서 가져옵니다.
    sql = "SELECT id, email, nick, phone FROM t_member WHERE id = %s"
    user_info = DQL(sql, (user_id,))

    if not user_info:
        flash('사용자 정보를 찾을 수 없습니다.')
        return redirect(url_for('home'))  # 혹은 다른 경로로 리디렉션

    # 사용자 정보를 템플릿에 전달합니다.
    user_info = user_info[0]  # 결과가 리스트 형태이므로 첫 번째 요소를 사용

    # 펫 정보를 가져옵니다.
    pet_info = get_pet_info(user_id)

    return render_template('profile.html', user_id=user_info['id'], email=user_info['email'],
                           nickname=user_info['nick'], phone=user_info['phone'],  pet_info=pet_info)

from flask import flash


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'login_user' not in session:
        return redirect(url_for('login'))

    user_id = session['login_user']
    current_password = request.form['current_password']
    new_password = request.form['password']
    new_email = request.form['email']
    new_nickname = request.form['nickname']
    new_phone = request.form['phone']

    # 현재 비밀번호가 저장된 비밀번호와 일치하는지 확인
    check_password_sql = "SELECT id FROM t_member WHERE id = %s AND pw = %s"
    user = DQL(check_password_sql, (user_id, current_password))

    if not user:
        flash('현재 비밀번호가 일치하지 않습니다.')
        return redirect(url_for('profile'))

    # 데이터베이스에서 사용자 프로필 업데이트
    update_profile_sql = "UPDATE t_member SET pw = %s, email = %s, nick = %s, phone = %s WHERE id = %s"
    try:
        DML(update_profile_sql, (new_password, new_email, new_nickname, new_phone, user_id))
        flash('프로필이 성공적으로 업데이트되었습니다.','success')
    except Exception as e:
        print("프로필 업데이트 중 오류 발생:", str(e))
        flash('프로필 업데이트 중 오류가 발생했습니다.', 'error')

    return redirect(url_for('home'))



@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/termsofuse')
def termsofuse():
    return render_template('termsofuse.html')

@app.route('/data', methods=['GET','POST'])
def receive_data():
    #data = request.json
    data = request.get_json()
    if data is None:
        data = json.loads(request.data.decode('utf-8'))
    # 값이 2 이상인 경우에만 IFTTT로 알림 보내기
    if isinstance(data, dict) and 'value' in data and data['value'] > 0:
        try:
            # 데이터베이스에 연결
            connection = pymysql.connect(host="project-db-stu3.smhrd.com", 
                                        db="Insa4_IOTB_final_4", 
                                        user="Insa4_IOTB_final_4", 
                                        password="aischool4", 
                                        port=3307,
                                        cursorclass=pymysql.cursors.DictCursor)
            with connection:
                with connection.cursor() as cursor:
                    # SQL 업데이트 쿼리
                    query = "UPDATE t_voice SET voice_result = 1 WHERE voice_idx = %s"
                    
                    # SQL 명령 실행
                    cursor.execute(query, (data['value'], data['voice_idx']))
                    
                    # 변경 사항 커밋
                    connection.commit()
                    
                # 연결 종료
                connection.close()

            send_notification()
            return {'success':'Notification sent'}
        except Exception as e:
                return {'fail': f'오류: {e}'}
    else:
        return {'fail':'Notification no sent'}

def send_notification():
    # IFTTT로 POST 요청 보내기
    data1 = {'value': '노드조'}
    try:
        response = requests.post(ifttt_webhook_url, json=data1)
        response.raise_for_status()  # 나쁜 응답에 대해 HTTPError 발생
        logger.info("알림이 성공적으로 전송되었습니다.")
    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP 오류: {errh}")
    except requests.exceptions.RequestException as err:
        logger.error(f"요청 예외: {err}")

cursor = mysql.cursor()
@app.route("/")
def index():
    # 예제 쿼리: pet_idx가 1이고 voice_result가 'A' 또는 'B'인 데이터 가져오기
    query = "SELECT * FROM t_voice WHERE pet_idx = 1 AND voice_result IN ('A', 'B')"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        # 예제 쿼리: voice_result 값에 따라 voice_data 업데이트
        update_query = """
        UPDATE t_voice
        SET 
            voice_data = CASE 
                            WHEN voice_result = 'A' THEN '정임이 천재' 
                            WHEN voice_result = 'B' THEN '정임이 바보' 
                        END,
            result_at = CONVERT_TZ(NOW(), 'UTC', 'Asia/Seoul')
        WHERE voice_idx = %s
        """
        cursor.execute(update_query, (result[0],))  # result[0]은 voice_idx

        # 업데이트된 데이터를 HTML 파일에 전달
        return render_template("home.html", voice_data=result[2])
    else:
        return "No data found."
cursor = mysql.cursor()

@app.route("/")
def index():
    # MySQL 쿼리 실행
    query = """
    SELECT DATE(result_at) AS date, COUNT(*) AS count
    FROM t_voice
    GROUP BY DATE(result_at)
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # 결과를 JSON 형식으로 반환
    return jsonify(results)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)








