import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAccountStore = defineStore('account', () => {
    const API_URL = 'http://127.0.0.1:8000'
    
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
                // 회원가입 후 로그인 해주기
            })
            .catch((error) => {
                console.error('Error:', error.response || error.message || error);         
            })
    }
    return { API_URL, signUp }
})
