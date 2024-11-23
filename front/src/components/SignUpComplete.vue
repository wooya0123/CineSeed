<template>
    <div>
        <h1>회원가입 성공!</h1>
        <p>앞으로 OOO에서 활동을 즐겨주세요!</p>
        <hr>
        <p v-on:click="goHome">홈으로 가기</p>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()
const goHome = function () {
    // 홈페이지로 이동
    // router.push({ name: 'home' })
}
</script>

<style scoped>

</style>