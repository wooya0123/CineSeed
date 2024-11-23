<template>
    <div>
        <h1>로그인</h1>
        <form @submit.prevent="logIn">
            <label for="username">아이디</label><br>
            <input type="text" id="username" v-model.trim="username"><br>

            <label for="password">비밀번호</label><br>
            <input type="password" id="password1" v-model.trim="password"><br>
            <p>비밀번호 생성 조건</p>

            <button>로그인</button>
            <hr>
            <p v-on:click="goSignUp">아직 회원이 아니신가요? 회원가입</p>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'
import { useRouter } from 'vue-router';

const store = useAccountStore()
const router = useRouter()

const username = ref(null)
const password = ref(null)

const logIn = function () {
    const payload = {
        username: username.value,
        password: password.value,
    }
    store.logIn(payload)
}

const goSignUp = function () {
    router.push({ name: 'signup' })
}
</script>

<style scoped>

</style>