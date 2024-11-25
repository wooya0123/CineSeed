import { ref, computed, watch } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
    const API_URL = 'http://127.0.0.1:8000'
    const token = ref(localStorage.getItem('user-token') || null)                       // 로그인 토큰 정보
    const user = ref(JSON.parse(localStorage.getItem('user-info') || null))             // 유저 정보 (민감성 정보 제외 필요)
    const isLogIn = ref(!!token.value) // 초기값 설정
    const router = useRouter()

    watch(token, (newToken) => {
        isLogIn.value = !!newToken
      })

    const signUp = function (formdata) {
        axios({
            method: 'post',
            url: `${API_URL}/accounts/signup/`,
            data: formdata
        })
            .then((res) => {
                console.log('회원가입 성공')
        
                // formData에서 데이터를 가져올 때 키를 문자열로 명시
                const username = formdata.get("username");
                const password = formdata.get("password1")
                // 로그인을 호출
                logIn({ username, password })
            })
            .catch((error) => {
                console.log(error)
                // 오류 응답 처리
                if (error.response && error.response.data) {
                    // 서버에서 반환된 오류 메시지를 alert로 표시
                    const errorMessages = error.response.data; 
                    
                    // 필드별 오류 메시지를 처리하여 alert로 표시
                    if (errorMessages.username) {
                        // alert(`아이디 오류: ${errorMessages.username.join(', ')}`);
                        alert('아이디 오류: 이미 존재하는 아이디입니다.')
                    }
                    if (errorMessages.nickname) {
                        alert(`닉네임 오류: ${errorMessages.nickname.join(', ')}`);
                        // alert('닉네임 오류: 이미 존재하는 닉네임입니다.')
                    }
                    if (errorMessages.email) {
                        alert(`이메일 오류: ${errorMessages.email.join(', ')}`);
                    }
                    if (errorMessages.password1) {
                        alert(`비밀번호 오류: ${errorMessages.password1.join(', ')}`);
                    }
                    if (errorMessages.password2) {
                        alert(`비밀번호 오류: ${errorMessages.password2.join(', ')}`);
                    }
                } else {
                    // 서버에서 오류 메시지가 없는 경우 일반적인 에러 메시지
                    alert('회원가입 중 오류가 발생했습니다. 다시 시도해 주세요.');
                }
            })
    }

    const logIn = function (payload) {
        const { username, password } = payload

        axios({
            method: 'post',
            url: `${API_URL}/accounts/login/`,
            data: {
                username,
                password
            }
        })
        .then((res) => {
            console.log('로그인 성공')
            token.value = res.data.key
            localStorage.setItem('user-token', token.value) // 토큰을 로컬 스토리지에 저장
                
            // 로그인 후 유저 정보 가져오기
            return axios({
                method: 'get',
                url: `${API_URL}/accounts/user/`,
                headers: {
                'Authorization': `Token ${token.value}`
                },
            })
        })
        .then((userResponse) => {
            return axios({
                method: 'get',
                url: `${API_URL}/api/v1/profile/${userResponse.data.pk}/`,
                headers: {
                    'Authorization': `Token ${token.value}`
                },
            })
        })
        .then((finalResponse) => {
            console.log(finalResponse.data)
            console.log(isLogIn)
            user.value = finalResponse.data
            localStorage.setItem('user-info', JSON.stringify(user.value))   // 로컬 스토리지에 유저 정보 저장
            router.push({ name : 'home' })
        })
         .catch((error) => {
                // 로그인 실패 시 오류 처리
                if (error.response && error.response.data) {
                    const errorMessages = error.response.data;
        
                    // 예를 들어, 로그인 오류 메시지에 대한 처리
                    if (errorMessages.non_field_errors) {
                        alert(`로그인 오류: ${errorMessages.non_field_errors.join(', ')}`);
                    }
        
                    if (errorMessages.username) {
                        alert(`아이디 오류: ${errorMessages.username.join(', ')}`);
                    }
        
                    if (errorMessages.password) {
                        alert(`비밀번호 오류: ${errorMessages.password.join(', ')}`);
                    }
                } else {
                    alert('로그인 중 오류가 발생했습니다. 다시 시도해 주세요.');
                }
            })
    }

    const logOut = function () {
        axios({
            method: 'post',
            url: `${API_URL}/accounts/logout/`,
          })
            .then((res) => {
              console.log(res.data)
              res.value = null
              token.value = null
              user.value = null

              localStorage.removeItem('user-token')     // 로컬 스토리지에서 토큰 제거
              localStorage.removeItem('user-info')      // 로컬 스토리지에서 사용자 정보 제거
              router.push({ name: 'home' })             // 홈으로 이동
            })
            .catch((err) => {
              console.log(err)
            })
    }

    // accountStore의 상태가 변경될 때 localStorage를 자동으로 갱신하도록 설정
    watch(token, (newToken) => {
        localStorage.setItem('user-token', newToken || '')
        isLogIn.value = !!newToken;
    })

    watch(user, (newUser) => {
        localStorage.setItem('user-info', JSON.stringify(newUser))
    })

    return { API_URL, token, user, isLogIn, signUp, logIn, logOut }
})