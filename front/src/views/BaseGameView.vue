<template>
    <div v-show="!isPlaying">
        <h1>영화 취향 테스트</h1>
        <p>게임 설명</p>
        <button v-on:click="startGame">게임 시작하기</button>
    </div>
    <div v-if="isPlaying">
        <GameRound />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import GameRound from '@/components/GameRound.vue'

const isPlaying = ref(false)

const startGame = function () {
    isPlaying.value = true
    console.log(isPlaying.value)    
}
</script>

<style scoped>

</style>