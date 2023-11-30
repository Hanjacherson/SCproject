from flask import Flask, session, render_template, redirect, request, url_for, flash, jsonify, g
from datetime import datetime
from werkzeug.utils import secure_filename
import pymysql, os

mysql = pymysql.connect(host="project-db-stu3.smhrd.com", 
                       db="Insa4_IOTB_final_4", 
                       user="Insa4_IOTB_final_4", 
                       password="aischool4", 
                       port=3307,
                       cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)
app.secret_key = "12345"

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

@app.route('/')
def index():
    # /login으로 리다이렉트
    return redirect(url_for('login'))

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


@app.route('/get_pet_info', methods=['GET'])
def get_pet_info_route():
    member_id = request.args.get('member_id')
    pet_id = request.args.get('id')

    # 여기에서 적절한 SQL 쿼리를 사용하여 펫 정보를 가져오는 로직을 작성
    # 이하 코드는 예시이며, 실제로 사용하는 테이블 및 필드명에 맞게 수정해야 합니다.
    pet_sql = "SELECT pet_idx, pet_name, created_at, pet_img FROM t_pet JOIN t_member USING (id) WHERE t_pet.id = %s"
    pet_result = DQL(pet_sql, (member_id, pet_id))

    if pet_result:
        pet_info = pet_result[0]
        return jsonify(pet_info)
    else:
        return jsonify({'error': '반려견 정보를 찾을 수 없습니다'}), 404
    


# 업로드 폴더 설정
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 기본 이미지 파일명 설정
DEFAULT_IMAGE = 'default_image.jpg'


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pet_image' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['pet_image']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.root_path, 'static', 'uploads', filename)
        file.save(upload_path)

        # 업로드 성공 시에 파일 이름을 세션에 저장
        session['uploaded_filename'] = filename

        # 세션에서 사용자 ID 가져오기
        user_id = session.get('login_user')
        pet_id = session.get('current_pet_id')  # 현재 선택된 반려동물 ID

        # 펫 정보 가져오기
        pet_info = get_pet_info(user_id)

        if user_id and pet_info:
            # 사용자 ID를 통해 해당 사용자의 반려견 정보 업데이트
            update_pet_info(user_id, pet_info['pet_name'], pet_info['created_at'], filename)  # filename이 이미지 파일명

            flash('File successfully uploaded')
            return redirect(url_for('home'))  # 업로드 완료 후 home으로 리디렉션
        else:
            flash('Invalid session data')

    return render_template('profile.html')  # 업로드 실패 시 업로드 페이지로 리디렉션

        # 세션에서 사용자 ID 가져오기
        #member_id = session.get('login_user')
        #pet_id = session.get('current_pet_id')  # 현재 선택된 반려동물 ID

        #if member_id:
            # 업로드된 이미지 파일명을 데이터베이스의 t_pet 테이블의 pet_img 필드에 업데이트합니다.
            #update_sql = "UPDATE t_pet SET pet_img = %s WHERE id = %s"
            #DML(update_sql, (filename, member_id))

            #flash('File successfully uploaded')
            #return redirect(url_for('profile'))  # 업로드 완료 후 home으로 리디렉션
        #else:
            #flash('Invalid session data')

    #return render_template('profile.html')  # 업로드 실패 시 업로드 페이지로 리디렉션


def update_pet_info(user_id, pet_name, created_at, pet_img=None):
    try:
        # 사용자가 t_pet에 이미 레코드를 가지고 있는지 확인
        check_query = "SELECT * FROM t_pet WHERE id = %s"
        result = DQL(check_query, (user_id,))

        if result:
            # 이미 레코드가 있는 경우, 업데이트
            update_query = "UPDATE t_pet SET pet_name=%s, created_at=%s, pet_img=%s WHERE id = %s"
            DML(update_query, (pet_name, created_at, pet_img, user_id))
        else:
            # 레코드가 없는 경우, 삽입
            insert_query = "INSERT INTO t_pet (pet_name, created_at, pet_img, id) VALUES (%s, %s, %s, %s)"
            DML(insert_query, (pet_name, created_at, pet_img, user_id))

        # 성공 메시지를 세션에 추가
        session['update_success_message'] = True

    except Exception as e:
        print(f"Error in update_pet_info: {str(e)}")
        # 실패 메시지를 세션에 추가
        session['update_failure_message'] = True 


@app.route('/show_pet_image/<filename>')
def show_pet_image(filename):
    # 세션에서 사용자 ID와 반려동물 ID 가져오기
    member_id = session.get('login_user')  # 로그인한 사용자 ID
    pet_id = session.get('current_pet_id')  # 현재 선택된 반려동물 ID

    if member_id and pet_id:
        # 데이터베이스에서 pet_img 필드를 검색합니다.
        pet_img_sql = "SELECT pet_img FROM t_pet JOIN t_member USING (id) WHERE t_pet.id = %s"
        pet_img_result = DQL(pet_img_sql, (member_id,))

        if pet_img_result:
            pet_img_filename = pet_img_result[0]['pet_img']
            if pet_img_filename:
                return f'<img src="{url_for("static", filename=f"uploads/{pet_img_filename}")}" alt="My Pet">'

    # 이미지가 없으면 기본 이미지를 사용합니다.
    return f'<img src="{url_for("static", filename=f"uploads/{DEFAULT_IMAGE}")}" alt="Default Pet Image">'



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


@app.route('/home/profile', methods=['GET', 'POST'])
def profile():

    uploaded_filename = session.pop('uploaded_filename', None)

    # 로그인한 사용자의 ID를 가져옵니다.
    if 'login_user' not in session:
        return redirect(url_for('login'))
    user_id = session['login_user']

    # 사용자 정보를 데이터베이스에서 가져옵니다.
    #sql = "SELECT id, email, nick, phone FROM t_member WHERE id = %s"
    sql = """
        SELECT t_member.id, email, nick, phone, created_at, pet_name
        FROM t_member
        LEFT JOIN t_pet ON t_member.id = t_pet.id
        WHERE t_member.id = %s
    """
    user_info = DQL(sql, (user_id,))

    if not user_info:
        flash('사용자 정보를 찾을 수 없습니다.')
        return redirect(url_for('home'))  # 혹은 다른 경로로 리디렉션

    # 사용자 정보를 템플릿에 전달합니다.
    user_info = user_info[0]  # 결과가 리스트 형태이므로 첫 번째 요소를 사용

    # 펫 정보를 가져옵니다.
    pet_info = get_pet_info(user_id)

    # 'created_at' 값을 템플릿으로 전달합니다.
    created_at = user_info['created_at']

    # 등록/수정 버튼이 눌렸을 때의 처리
    if request.method == 'POST':
        pet_name = request.form['dog_name']
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']

        # 날짜 구성 요소를 하나의 문자열로 결합
        created_at = f"{year}-{month}-{day}"

        print(f"Pet Name: {pet_name}")
        print(f"Created At: {created_at}")

        # 데이터베이스에 등록 또는 수정
        update_pet_info(user_id, pet_name, created_at)

        # 업데이트된 펫 정보 다시 가져오기
        pet_info = get_pet_info(user_id)

        print(f"Updated Pet Info: {pet_info}")

    return render_template('profile.html', user_id=user_info['id'], email=user_info['email'],
                           nickname=user_info['nick'], phone=user_info['phone'],  pet_info=pet_info, created_at=created_at)


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


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)








