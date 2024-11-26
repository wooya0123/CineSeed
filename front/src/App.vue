<template>
  <nav class="top-nav bg-gray6">
    <a class="logo" @click="goHome">
        <img src="" alt="logo" width="30" height="24">
    </a>
    <div class="account-area caption">
      <span v-if="!account.isLogIn">
        <RouterLink :to="{ name : 'login' }" class="top-text nav-text:hover">
          로그인
        </RouterLink>
      </span>
      <span v-if="!account.isLogIn">
        <RouterLink :to="{ name : 'signup' }" class="top-text nav-text:hover">
          회원가입
        </RouterLink>
      </span>
      <span class="gray2" v-if="account.isLogIn && account.user">
        {{ account.user.nickname }}님의 잔액 : {{ account.user.cash }}원
      </span>
      <span v-if="account.isLogIn && account.user">
        <RouterLink :to="{ name : 'profile', params: { id: account.user.id }}" class="top-text nav-text:hover">
          마이페이지
        </RouterLink>
      </span>

      <form @submit.prevent="logOut" v-show="account.isLogIn">
        <input type="submit" value="로그아웃" class="delete-button-style delete-button-style:hover">
      </form>
    </div>
  </nav>

  <div class="menu-nav bg-gray6">
    <div class="menu-text-container">
      <RouterLink :to="{ name : 'home' }" class="menu-text menu-text:hover menu-text:focus">홈</RouterLink>
    </div>
    <div class="menu-text-container">
      <RouterLink :to="{ name : 'movies' }" class="menu-text menu-text:hover menu-text:focus">영화</RouterLink>
    </div>
    <div class="menu-text-container">
      <RouterLink :to="{ name : 'game' }" class="menu-text menu-text:hover menu-text:focus">영화 취향 분석</RouterLink>
    </div>
  </div>

  <RouterView class="container"/>
</template>

<script setup>
import { RouterView, RouterLink, useRouter } from 'vue-router'
import { useAccountStore } from './stores/account'

const account = useAccountStore()
const router = useRouter()

const logOut = function () {
  account.logOut()
}

const goHome = function () {
  router.push({ name : 'home' })
}
</script>

<style scoped>
.top-nav {
  height:48px;
  padding-left:60px;
  padding-right:60px;
  padding-top:8px;
  padding-bottom:8px;
  display:flex;
  flex-direction:row;
  justify-content:space-between;
  align-items:center;
  position:relative;
}

.account-area {
  width: fit-content;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap:10px;
}

.top-text {
  color: #F5FAFF;
  text-decoration: none;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

.top-text:hover {
  color: #FB4CA1;
  text-decoration: none;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

/* 버튼 속성 지우기 */
.delete-button-style {
  color: #F5FAFF;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.delete-button-style:hover {
  color: #FB4CA1;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
}

.menu-nav {
  height:48px;
  /* filter:drop-shadow(0px 4px 4px #f3b3d1); */
  box-shadow: 0 1px 10px #f478b2;
  padding-left:60px;
  padding-right:60px;
  display:flex;
  flex-direction:row;
  justify-content:flex-start;
  align-items:center;
  gap:24px;
}

.menu-text-container {
  display: flex;
  flex-direction: column;
  align-items: baseline;
  height: 48px;
  padding-top: 12px;
}

.menu-text {
  color: #F5FAFF;
  padding-left: 4px;
  padding-right: 4px;
  text-decoration: none;
  border-bottom: 10px;
  align-items: center;
  flex: 1;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

.menu-text:hover {
  color: #FB4CA1;
  text-decoration: none;
  align-items: center;
  flex: 1;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}

.menu-text:focus {
  color: #FB4CA1;
  text-decoration: none;
  align-items: center;
  border-bottom: 2px solid #FB4CA1;
  flex: 1;
  white-space: nowrap; /* 텍스트 줄바꿈 방지 */
}
</style>