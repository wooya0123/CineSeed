import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
    const API_URL = 'http://127.0.0.1:8000'
    const token = ref(localStorage.getItem('user-token'))                       // 로그인 토큰 정보
    const user = ref(JSON.parse(localStorage.getItem('user-info')))             // 유저 정보 (민감성 정보 제외 필요)
    const profile = ref(JSON.parse(localStorage.getItem('user-profile')))       // 마이페이지용 유저 정보 (민감성 정보 제외 필요)

    const isLogIn = computed(() => {
        if (token.value === null) {
            return false
        } else {
            return true
        }
    })
    
    const router = useRouter()

    const signUp = function (payload) {
        const { username, password1, password2, nickname, role, email, instagram, etc, introduction } = payload

        axios({
            method: 'post',
            url: `${API_URL}/accounts/signup/`,
            data: {
                username,
                password1,
                password2,
                nickname,
                role,
                email,
                instagram,
                etc,
                introduction
            }
        })
            .then((res) => {
                console.log('회원가입 성공')
                router.push({ name: 'login' })   // 회원가입 후 로그인 페이지로 이동
            })
            .catch((error) => {
                console.error('Error:', error.response || error.message || error)   
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
                user.value = userResponse.data
                localStorage.setItem('user-info', JSON.stringify(user.value))   // 유저 정보를 로컬 스토리지에 저장
                router.push({ name: 'home' })   // 로그인 성공 후 홈으로 이동
            })
            .catch((error) => {
                console.error('Error:', error.response || error.message || error)     
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
              profile.value = null

              localStorage.removeItem('user-token')     // 로컬 스토리지에서 토큰 제거
              localStorage.removeItem('user-info')      // 로컬 스토리지에서 사용자 정보 제거
              localStorage.removeItem('user-profile')   // 로컬 스토리지에서 사용자 정보 제거

              router.push({ name: 'home' })     // 홈으로 이동
            })
            .catch((err) => {
              console.log(err)
            })
    }

    const myPage = function () {    
        axios({
            method: 'get',
            url: `${API_URL}/api/v1/profile/${user.value.pk}/`,
            headers: {
                'Authorization': `Token ${token.value}`
            },
        })
            .then((res) => {
                console.log(res.data)
                profile.value = res.data
                localStorage.setItem('user-profile', JSON.stringify(profile.value))
            })
            .catch((err) => {
                console.error('Error:', error.response || error.message || error)
            })
    }

    return { API_URL, token, user, profile, isLogIn, signUp, logIn, logOut, myPage }
})
