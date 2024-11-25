<template>
  <div>
    <h1>영화 취향 토너먼트 게임</h1>
    <h3>당신의 영화 취향을 알아보세요!</h3>
    <button @click='playGame'>게임 시작하기</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router/dist/vue-router';
const router = useRouter()
const playGame = function () {
  router.push({name : 'game'})
}
</script>

<style scoped>

</style>