


> D모델링 주소 

URL : https://aquerytool.com/aquerymain/index/?rurl=e5e60963-ef28-461d-bad4-dd091cca2581&
Password : 8j81cg

> 소수점 처리 

  12397.04 ... DECIMAL(7,2) = NUMERIC(7,2) --> 오라클 NUMER(7,2) 

> 데이터 객체 : VO(Value Object)=DTO(Data Transfer Object)

// 회원 
public class MemerDTO {

    // 아이디 
    private String id;

    // 비밀번호 
    private String pw;

    // 이메일 
    private String email;

    // 성명(닉네임) 
    private String nick;

    // 전화번호 
    private String phone;

    // 가입일자 
    private Timestamp joinedAt;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getPw() {
        return pw;
    }

    public void setPw(String pw) {
        this.pw = pw;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getNick() {
        return nick;
    }

    public void setNick(String nick) {
        this.nick = nick;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public Timestamp getJoinedAt() {
        return joinedAt;
    }

    public void setJoinedAt(Timestamp joinedAt) {
        this.joinedAt = joinedAt;
    }

    // tMember 모델 복사
    public void CopyData(tMember param)
    {
        this.id = param.getId();
        this.pw = param.getPw();
        this.email = param.getEmail();
        this.nick = param.getNick();
        this.phone = param.getPhone();
        this.joinedAt = param.getJoinedAt();
    }
}

> 회원 비밀번호 암호화 :

select * from t_member limit 10;

-- 비밀번호 암호화 : AES / MD5 / SHA / SHA2 

SELECT MD5('1234');        # 32글자 81dc9bdb52d04dc20036dbd8313ed055
SELECT SHA('1234');        # 40글자 7110eda4d09e062aa5e4a390b0a572ac0d2c0220
SELECT SHA2('1234', 224);  # 56글자 99fb2f48c6af4761f904fc85f95eb56190e5d40b1f44ec3a9c1fa319
SELECT SHA2('1234', 256);  # 64 글자 03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4
SELECT SHA2('1234', 384);  # 96글자 504f008c8fcf8b2ed5dfcde752fc5464ab8ba064215d9c5b5fc486af3d9ab8c81b14785180d2ad7cee1ab792ad44798c
SELECT SHA2('1234', 512);  # 128글자 d404559f602eab6fd602ac7680dacbfaadd13630335e951f097af3900e9de176b6db28512f2e000b9d04fba5133e8b1c6e8df59db3a8ab9d60be4b97cc9e81db


INSERT INTO t_member (id, pw, email, nick, phone, joined_at) 
VALUES ('id 1', SHA2('pw 1', 512), 'email 1', 'nick 1', 'phone 1', NOW());




SELECT SHA3('1234', 256);  # SHA3는 MySQL 8.0.30에서 지원됨. 
SELECT VERSION();          # 8.0.26



SELECT LENGTH('d404559f602eab6fd602ac7680dacbfaadd13630335e951f097af3900e9de176b6db28512f2e000b9d04fba5133e8b1c6e8df59db3a8ab9d60be4b97cc9e81db');
SELECT LENGTH('03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

SELECT * FROM t_member ORDER BY joined_at DESC LIMIT 15;


-- 자바에서 insert 처리 
-- INSERT INTO t_member VALUES(?, SHA2(?, 512), ?, ?...);

-- 자바에서 login 처리 

SELECT COUNT(*) FROM t_member 
WHERE id = u_id AND pw = SHA2('u_pw', 512);

SELECT * FROM t_member ORDER BY joined_at DESC LIMIT 5;

login = SELECT COUNT(*) FROM t_member 
WHERE id = 'id 1' AND pw = SHA2('pw 1', 512);
if login > then '로그인 성공' else '로그인 실패'


>> 프로젝트는 어떻게 할 것인가?

개소리 음성분석 : 개소리 음성을 분석하여 이상징후 발생 시 주인에게 알려주는 서비스

(python) 
음성분석 라이브러리 : librosa, music21 
음성분석 기초자료 찾기 : https://www.youtube.com/watch?v=IE6lue0qusQ

* 음성분석 알고리듬   : Mel-spectrogram + MFCCs 결합한 복합적인 방법 ---> (Step 1)
z5r
* [LSTM]   Mel-spectrogram    + MFCCs(Step 1) ... 60.5%, 
* [BiLSTM] Mel-spectrogram    + MFCCs(Step 2) ... 75.8% (Hyperparameter 10가지, 최적화하기)
* [BiLSTM +A] Mel-spectrogram + MFCCs(Step 3) ... 95.6% (시각화:Matplotlig, Seaborn) --F1 Score, ....Confusion Matrix..

LSTM(Long-Short Term Memory) --> (1) BiDirection LSTM -> BiLSTM (2) EfficientNet B0/B1/B2/B3...


---------------------------------------------------------------------------------
(최종프로젝트 개성공단 SQL)

-- 테이블 순서는 관계를 고려하여 한 번에 실행해도 에러가 발생하지 않게 정렬되었습니다.

-- t_member Table Create SQL
-- 테이블 생성 SQL - t_member
use Insa4_IOTB_final_4;

CREATE TABLE t_member
(
    `id`         VARCHAR(30)    NOT NULL    COMMENT '아이디', 
    `pw`         VARCHAR(30)    NOT NULL    COMMENT '비밀번호', 
    `email`      VARCHAR(40)    NOT NULL    COMMENT '이메일', 
    `nick`       VARCHAR(30)    NOT NULL    COMMENT '성명(닉네임)', 
    `phone`      VARCHAR(20)    NOT NULL    COMMENT '전화번호', 
    `joined_at`  DATETIME       NOT NULL    COMMENT '가입일자', 
     PRIMARY KEY (id)
);

-- 테이블 Comment 설정 SQL - t_member
ALTER TABLE t_member COMMENT '회원';


-- t_pet Table Create SQL
-- 테이블 생성 SQL - t_pet
CREATE TABLE t_pet
(
    `pet_idx`     INT UNSIGNED     NOT NULL    AUTO_INCREMENT COMMENT '반려동물 순번', 
    `pet_name`    VARCHAR(50)      NOT NULL    COMMENT '반려동물 이름', 
    `pet_weight`  NUMERIC(4,1)     NOT NULL    COMMENT '반려동물 체중', 
    `created_at`  DATE             NOT NULL    COMMENT '반려동물 태어난날', 
    `id`          VARCHAR(30)      NOT NULL    COMMENT '소유자 아이디', 
    `pet_img`     VARCHAR(1000)    NOT NULL    COMMENT '반려동물 사진', 
     PRIMARY KEY (pet_idx)
);

-- 테이블 Comment 설정 SQL - t_pet
ALTER TABLE t_pet COMMENT '반려동물';

-- Foreign Key 설정 SQL - t_pet(id) -> t_member(id)
ALTER TABLE t_pet
    ADD CONSTRAINT FK_t_pet_id_t_member_id FOREIGN KEY (id)
        REFERENCES t_member (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - t_pet(id)
-- ALTER TABLE t_pet
-- DROP FOREIGN KEY FK_t_pet_id_t_member_id;


-- t_voice Table Create SQL
-- 테이블 생성 SQL - t_voice
CREATE TABLE t_voice
(
    `voice_idx`   INT UNSIGNED     NOT NULL    AUTO_INCREMENT COMMENT '소리 순번', 
    `pet_idx`     INT UNSIGNED     NOT NULL    COMMENT '반려동물 순번', 
    `voice_data`  VARCHAR(1000)    NOT NULL    COMMENT '음성 데이터', 
     PRIMARY KEY (voice_idx)
);

-- 테이블 Comment 설정 SQL - t_voice
ALTER TABLE t_voice COMMENT '소리 데이터';

-- Foreign Key 설정 SQL - t_voice(pet_idx) -> t_pet(pet_idx)
ALTER TABLE t_voice
    ADD CONSTRAINT FK_t_voice_pet_idx_t_pet_pet_idx FOREIGN KEY (pet_idx)
        REFERENCES t_pet (pet_idx) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - t_voice(pet_idx)
-- ALTER TABLE t_voice
-- DROP FOREIGN KEY FK_t_voice_pet_idx_t_pet_pet_idx;


-- t_anomaly Table Create SQL
-- 테이블 생성 SQL - t_anomaly
CREATE TABLE t_anomaly
(
    `anomaly_idx`     INT UNSIGNED    NOT NULL    AUTO_INCREMENT COMMENT '이상징후 순번', 
    `voice_idx`       INT UNSIGNED    NOT NULL    COMMENT '소리 순번', 
    `anomaly_result`  TEXT            NOT NULL    COMMENT '이상징후 내용', 
    `created_at`      DATETIME        NOT NULL    COMMENT '발생 시간', 
     PRIMARY KEY (anomaly_idx)
);

-- 테이블 Comment 설정 SQL - t_anomaly
ALTER TABLE t_anomaly COMMENT '이상 징후';

-- Foreign Key 설정 SQL - t_anomaly(voice_idx) -> t_voice(voice_idx)
ALTER TABLE t_anomaly
    ADD CONSTRAINT FK_t_anomaly_voice_idx_t_voice_voice_idx FOREIGN KEY (voice_idx)
        REFERENCES t_voice (voice_idx) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - t_anomaly(voice_idx)
-- ALTER TABLE t_anomaly
-- DROP FOREIGN KEY FK_t_anomaly_voice_idx_t_voice_voice_idx;


-- t_accessory Table Create SQL
-- 테이블 생성 SQL - t_accessory
CREATE TABLE t_accessory
(
    `pet_idx`        INT UNSIGNED    NOT NULL    COMMENT '반려동물 순번', 
    `battery_level`  VARCHAR(50)     NULL        COMMENT '배터리 잔량', 
     PRIMARY KEY (pet_idx)
);

-- 테이블 Comment 설정 SQL - t_accessory
ALTER TABLE t_accessory COMMENT '악세서리';

-- Foreign Key 설정 SQL - t_accessory(pet_idx) -> t_pet(pet_idx)
ALTER TABLE t_accessory
    ADD CONSTRAINT FK_t_accessory_pet_idx_t_pet_pet_idx FOREIGN KEY (pet_idx)
        REFERENCES t_pet (pet_idx) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - t_accessory(pet_idx)
-- ALTER TABLE t_accessory
-- DROP FOREIGN KEY FK_t_accessory_pet_idx_t_pet_pet_idx;


-- t_notification Table Create SQL
-- 테이블 생성 SQL - t_notification
CREATE TABLE t_notification
(
    `noti_idx`     INT UNSIGNED     NOT NULL    AUTO_INCREMENT COMMENT '알림 순번', 
    `id`           VARCHAR(30)      NOT NULL    COMMENT '사용자 아이디', 
    `anomaly_idx`  INT UNSIGNED     NOT NULL    COMMENT '이상징후 순번', 
    `msg`          VARCHAR(1000)    NOT NULL    COMMENT '메시지 내용', 
    `sended_at`    DATETIME         NOT NULL    COMMENT '전송 시간', 
     PRIMARY KEY (noti_idx)
);

-- 테이블 Comment 설정 SQL - t_notification
ALTER TABLE t_notification COMMENT '알림 서비스';

-- Foreign Key 설정 SQL - t_notification(anomaly_idx) -> t_anomaly(anomaly_idx)
ALTER TABLE t_notification
    ADD CONSTRAINT FK_t_notification_anomaly_idx_t_anomaly_anomaly_idx FOREIGN KEY (anomaly_idx)
        REFERENCES t_anomaly (anomaly_idx) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - t_notification(anomaly_idx)
-- ALTER TABLE t_notification
-- DROP FOREIGN KEY FK_t_notification_anomaly_idx_t_anomaly_anomaly_idx;

-- Foreign Key 설정 SQL - t_notification(id) -> t_member(id)
ALTER TABLE t_notification
    ADD CONSTRAINT FK_t_notification_id_t_member_id FOREIGN KEY (id)
        REFERENCES t_member (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Foreign Key 삭제 SQL - t_notification(id)
-- ALTER TABLE t_notification
-- DROP FOREIGN KEY FK_t_notification_id_t_member_id;




15:49:05	INSERT INTO t_pet (pet_name, pet_weight, created_at, id, pet_img) VALUES ('pet_name 10', 10, NOW(), 'id 010', 'pet_img 10')	1 row(s) affected, 1 warning(s): 1292 Incorrect date value: '2023-11-17 06:49:05' for column 'created_at' at row 1	0.063 sec
