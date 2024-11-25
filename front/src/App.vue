<template>
  <div>
    <RouterLink :to="{ name : 'home' }">홈</RouterLink> |
    <RouterLink :to="{ name : 'movies' }">영화</RouterLink>

    <span v-if="!account.isLogIn">
      | <RouterLink :to="{ name : 'login' }">로그인</RouterLink>
    </span>
    <span v-if="!account.isLogIn">
      | <RouterLink :to="{ name : 'signup' }">회원가입</RouterLink>
    </span>
    <span v-if="account.isLogIn && account.user">
      | <RouterLink :to="{ name : 'profile', params: { id: account.user.id }}">마이페이지</RouterLink>
    </span>


    <form @submit.prevent="logOut" v-show="account.isLogIn">
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

const account = useAccountStore()

const logOut = function () {
  account.logOut()
}
</script>

<style scoped>

</style>