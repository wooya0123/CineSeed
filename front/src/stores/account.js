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
