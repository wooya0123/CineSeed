<template>
    <div class="login-body">
      <div class="login-container bg-gray1 ">
        <h1>로그인</h1>
        <form class="login-form" @submit.prevent="logIn">
            <label for="username"></label>
            <input class="input-white" type="text" id="username" v-model.trim="username" placeholder="아이디"><br>

            <label for="password"></label>
            <input class="input-white" type="password" id="password1" v-model.trim="password" placeholder="비밀번호"><br>
            <button class="login-btn btn-lg bg-primary white">로그인</button>
            <hr>
            <p v-on:click="goSignUp">아직 회원이 아니신가요? 회원가입</p>
        </form>
      </div>
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
.login-body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
}

.login-container {
  width: 500px;
  padding: 50px;
  background-color: #F5FAFF;
  border-radius: 10px;
  text-align: left;
}

.login-form {
  margin-top: 50px;
  margin-bottom: 20px;
}

.login-container h1 {
  color: #333;
  margin-top: 50px;
}

.login-container hr {
  color: #333;
  margin-bottom: 5px;
}

.login-container p {
  color: #333;
  text-align: center;
  font-size: 10px;
  cursor: pointer;
}


.login-btn {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}




</style>