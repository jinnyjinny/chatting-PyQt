## 번역 기능이 탑재된 GUI 환경의 채팅 프로그래밍

### 실행화면 
- 서버, 클라이언트 채팅 <br>
<img width="540" src="https://user-images.githubusercontent.com/49601361/103331362-f6c50400-4aa8-11eb-83b4-04437368b0d2.png"><br>
<br>

- 서버 실행 로그 <br>
<img width="540" src="https://user-images.githubusercontent.com/49601361/103331406-2542df00-4aa9-11eb-8c0f-83e3129a1a4f.png"><br>
<br>

- 채팅방 지움 버튼 실행 <br>
<img width="540" src="https://user-images.githubusercontent.com/49601361/103331409-2b38c000-4aa9-11eb-9f04-cf5bc87209c2.png"><br>
<br>

- 번역 창 띄우기 <br>
<img width="540" src="https://user-images.githubusercontent.com/49601361/103331417-31c73780-4aa9-11eb-9b19-77c19d62e9a8.png"><br>
<br>

- 번역 결과 <br>
<img width="200" src="https://user-images.githubusercontent.com/49601361/103331424-34c22800-4aa9-11eb-9e2e-c27429e301bb.png"><br>
<br>

## PyQt <br>
 파이썬에서 데스크탑 프로그램 혹은 GUI 프로그램을 만들기 위해서 여러 GUI Framework (혹은 Toolkit) 들을 사용할 수 있다. 
 
## 2. 클래스 
### 2.1 Server
#### (1) 클라이언트 접속
start함수에서 ip, port를 바인드한다. 클라이언트가 접속할 때마다 listen함수에서 새로운 연결을 반복적으로 생성한다. 클라이언트가 접속할 때까지 무한 대기하다가 클라이언트가 접속하면 accept 함수를 통해 대기를 탈출한다. 클라이언트가 접속할  때마다 listen함수에서 스레드를 생성하는데 그 스레드에 의해 receive함수가 실행된다.  

#### (2) 클라이언트 삭제
선택한 하나의 클라이언트를 제거하기 위해 removeClient 함수를 사용한다. 서버에 할당된 주소 값, 클라이언트 리스트 값을 삭제하고 해당 클라이언트의 스레드가 죽어있기 때문에 스레드를 삭제시켜 준다. 삭제된 후 남아있는 클라이언트 정보들은 resourceInfo 함수를 호출시켜서 출력한다. 모든 클라이언트를 제거하기 위해서  removeAllClient 함수를 동작시키면 되는데, 이는 스레드 활동 유무에 상관없이 모든 주소 값, 클라이언트 리스트 값, 스레드들을 한번에 삭제시킨다.       

#### (3) 받은 메시지 보기, 메시지 전송
클라이언트로부터 받은 메세지를 차례로 send 함수에서 encoding하여 처리한다.
   
#### (4) 메세지 번역
serverTranslate 클래스에서 번역된 메세지를 받는 역할을 한다. 번역 과정은 2.2과 2.5에서 자세히 다룬다. 

### 2.2 ServerWindow		
#### (1) 클라이언트 접속
pyqt를 사용하여 채팅 서버 윈도우를 제작했다. Server를 임포트하여 ServerSocket 클래스를 객체화하여 재사용한다. 서버ip, port를 입력받는 항목은 9행2열로 구성하였다. 해당 항목에 소켓의 호스트 이름을 받아 표시하고 ServerSocket 객체에 포함된 ip, port를 끌어와 표시해준다. 서버 실행 버튼을 누르면 toggleButton 함수가 호출되어 소켓과 접속을 시작한다. 

#### (2) 메세지 삭제
채팅방 지움 버튼을 누르면  clearbtn 변수에 할당된 clearMsg 함수가 호출되어 clear메소드를 사용하여 메세지를 삭제한다.

#### (3) 받은 메시지 보기, 메시지 전송
보내기 버튼을 누르면 sendbtn 변수에 할당된 줄 편집기 객체가 호출된다. 차례로 sendMsg 함수가 호출되어 메세지를 서버로 보내도록 하는 과정을 거친다. 처음 호출된sendMsg 함수는 서버가 통신되는지 여부를 보고, 연결이 된다면 입력된 텍스트를 updateMsg함수를 호출하여 줄 편집기 안에 보여준다. 

####(4) 메세지 번역 
ServerTranslate의 TranslateWindow 클래스를 translateWin객체로 만들어 호출한다. 번역하기 버튼을 누르면action함수가 실행되어 새 창(번역기)을 show메소드를 사용하여 띄운다. 문장을 입력하면 translateWin 객체에 들어있는 google translator api가 작동한다. 


### 2.3 Client
connectServer함수에서 ip, port를 받아 연결한다. 연결 성공여부를 묻고, 연결에 성공한다면 Tread함수를 통해 스레드를 생성하여 실행시킨다. 메세지를 받고receive 함수를 사용하여1024의 길이만큼 메세지를 받을 수 있게 할당한다. utf-8로 인코딩하여 메세지를 문자열로 처리하고 받은 메세지를 출력한다. 클라이언트의 접속을 끊기 위해 Signal객체의 disconnect_signal.connect를 끌어와 사용하였다. 

### 2.4 ClientWindow
#### (1) 서버 접속 
Client를 임포트하여ClientSocket 클래스를 객체화하여 재사용한다. 서버ip, port를 입력받는 항목은 ClientSocket객체에 포함된 ip, port를 끌어와 표시해준다. ip를 입력하는데 용이하도록 setInputMask메소드를 사용하여 공간을 지정해준다. 접속 버튼을 누르면 connectClicked 함수가 호출되어 소켓과 접속을 시작한다. 

#### (2) 메세지 삭제 
채팅방 지움 버튼을 누르면  clearbtn 변수에 할당된 clearMsg 함수가 호출되어 clear메소드를 사용하여 메세지를 삭제한다.

#### (3) 받은 메시지 보기, 메시지 전송 
보내기 버튼을 누르면 sendbtn 변수에 할당된 줄 편집기 객체가 호출된다. 차례로 sendMsg 함수가 호출되어 메세지를 서버로 보내도록 하는 과정을 거친다. 처음 호출된sendMsg 함수는 서버가 통신되는지 여부를 보고, 연결이 된다면 입력된 텍스트를 updateMsg함수를 호출하여 줄 편집기 안에 보여준다. 

#### (4) 메세지 번역 
ClientTranslate의 TranslateWindow 클래스를 translateWin객체로 만들어 호출한다. 번역하기 버튼을 누르면action함수가 실행되어 새 창(번역기)을 show메소드를 사용하여 띄운다. 문장을 입력하면 translateWin 객체에 들어있는 google translator api가 작동한다. 

  
### 2.5 ServerTranslate + ClientTranslate
메세지를 번역하기 위해 google translator api를 사용한다. google translator api는 google에서 제공하는 유료로 key를 따로 설정하여 동작하는 방식과, 무료로 작동하는 방식이 있다. 해당 api는 무료로 작동하는 api를 사용했다. ‘한국어’, ‘영어’ 두개의 라벨과 한국어를 입력하는 줄 편집기, 영어가 출력되는 텍스트 편집기, 번역하기 버튼을 만들었다. 번역하기 버튼을 클릭하면 self.translate_kor 메서드를 호출시킨다. translate_kor 함수는 한국어를 영어로 번역하여 텍스트 편집기에 보여주는 기능을 한다. 하지만 한 줄을 번역하고 나면 프로그램이 종료된다는 문제점이 있다. 연속된 채팅에도 종료되지 않도록 개선 예정이다. 


