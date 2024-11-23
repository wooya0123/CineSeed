import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useAccountStore = defineStore('account', () => {
    const API_URL = 'http://127.0.0.1:8000'
    const token = ref(null)
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
                const password = password1
                logIn({ username, password})// 회원가입 후 로그인 해주기

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
                token.value = res.data.key
                console.log('로그인 성공')        
                // 로그인 성공 후 페이지 이동
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
              token.value = null
              // 페이지 이동
            })
            .catch((err) => {
              console.log(err)
            })
    }


    return { API_URL, signUp, logIn, token, isLogIn, logOut }
})
