const $ = (idSelector) => document.querySelector(`#${idSelector}`);

const $SignupUsernameInput = $('signup-username');
const $SignupPasswordInput = $('signup-password');
const $SignupNameInput = $('signup-name');
const $SignupStuIdInput = $('signup-studentid');

const $TokenUsernameInput = $('token-username');
const $TokenPasswordInput = $('token-password');

const $SignupBtn = $('signup-btn');
const $CreateTokenBtn = $('create-token-btn');
const $LogInBtn = $('verify-btn');
const $BlackTokenBtn = $('black-token-btn');

const SERVER_URL = 'http://localhost:8000/user/';

$SignupBtn.onclick = async (e) => {
  e.preventDefault();
  const payload = {
    username: $SignupUsernameInput.value,
    password: $SignupPasswordInput.value,
    name: $SignupNameInput.value,
    student_id: $SignupStuIdInput.value,
  };
  const res = await fetch(`${SERVER_URL}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  if (res.status === 201) {
    alert('회원가입에 성공!');
  } else {
    alert('회원가입 실패');
  }
};

$CreateTokenBtn.onclick = async (e) => {
  e.preventDefault();
  const payload = {
    username: $TokenUsernameInput.value,
    password: $TokenPasswordInput.value,
  };
  const res = await fetch(SERVER_URL + 'token/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const body = await res.json();
  if (res.status === 201) {
    alert(`액세스 토큰: ${body.access}`);
    document.cookie = 'access_token=' + body.access;
  } else {
    alert('인증 실패');
  }
};

$LogInBtn.onclick = async (e) => {
  e.preventDefault();
  const payload = {
    Authorization: 'Bearer ' + document.getCookie('access_token')
  };
  
  const res = await fetch(SERVER_URL + 'verify/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const body = await res.json();
  if (res.status == 200) {
    alert(`${body.msg}`);
  }
  else {
    alert('Log in failed...');
  }
}
var getCookie = function (name) {
  var value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return value ? value[2] : null;
};


// function getCookie(cookie_name) {
//   var x, y;
//   var val = document.cookie.split(';');

//   for (var i = 0; i < val.length; i++) {
//     x = val[i].substr(0, val[i].indexOf('='));
//     y = val[i].substr(val[i].구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구''); // 앞과 뒤의 공백 제거하기
//     if (x == cookie_name) {도구도구도구도구도두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구구도구도구도구도구두ㅗㄱ구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구독구도구
//       return unescape(y); // unescape로 디코딩 후 값 리턴
//     }
//   }도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ
// }두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구도구두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구두ㅗㄱ두ㅗㄱ두ㅗㄱ도구도구도구도구도구도구도구