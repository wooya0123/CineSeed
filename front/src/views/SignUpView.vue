<template>
    <div v-show="!store.isLogIn">
        <h1>회원가입</h1>
        <form @submit.prevent="signUp">
            <label for="profile_image">프로필 이미지</label><br>
            <input type="file" id="profile_image"><br>
            
            <label for="username">아이디</label><br>
            <input type="text" id="username" v-model.trim="username"><br>

            <label for="password1">비밀번호</label><br>
            <input type="password" id="password1" v-model.trim="password1"><br>

            <label for="password2">비밀번호 확인</label><br>
            <input type="password" id="password2" v-model.trim="password2"><br>

            <label for="nickname">닉네임</label><br>
            <input type="text" id="nickname" v-model.trim="nickname"><br>

            <label for="role">역할</label><br>
            <select id="role" v-model="role">
                <option value="UN">미정</option>
                <option value="DI">감독</option>
                <option value="AC">배우</option>
                <option value="ST">스태프</option>
            </select><br>

            <input type="text" id="email" placeholder="이메일" v-model="email"><br>

            <input type="text" id="instagram" placeholder="인스타그램" v-model="instagram"><br>

            <input type="text" id="etc" placeholder="기타" v-model="etc"><br>

            <label for="introduction">자기소개</label><br>
            <input type="textarea" id="introduction" v-model="introduction"><br>

            <button>회원가입</button>
        </form>
    </div>
    <div v-show="store.isLogIn">
        <SignUpComplete />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'
import SignUpComplete from '@/components/SignUpComplete.vue'

const store = useAccountStore()

const profile_image = ref(null)
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const nickname = ref(null)
const role = ref(null)
const email = ref(null)
const instagram = ref('')
const etc = ref('')
const introduction = ref('')

const signUp = function () {
    const payload = {
        username: username.value,
        password1: password1.value,
        password2: password2.value,
        nickname: nickname.value,
        role: role.value,
        email: email.value,
        instagram: instagram.value,
        etc: etc.value,
        introduction: introduction.value
    }
    store.signUp(payload)
}
</script>

<style scoped>

</style>