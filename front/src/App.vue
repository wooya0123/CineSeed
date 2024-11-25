<template>
  <div>
    <RouterLink :to="{ name : 'login' }">로그인</RouterLink> | 
    <RouterLink :to="{ name : 'signup' }">회원가입</RouterLink>
    <form @submit.prevent="logOut" v-show="store.isLogIn">
      <input type="submit" value="로그아웃">
    </form>
  </div>
  <div>
    <RouterLink :to="{ name : 'game' }">영화 취향 분석</RouterLink>
  </div>
  <RouterView />
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router'
import { useAccountStore } from './stores/account'

const store = useAccountStore()

const logOut = function () {
  store.logOut()
}
</script>

<style scoped>

</style>