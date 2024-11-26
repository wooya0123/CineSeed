<template>
    <div v-show="!isPlaying" class="background">
        <div class="container" style="text-align: center;">
            <h1>나의 영화 취향은 ?</h1>
            <p>평소 좋아하는 영화를 바탕으로 펀딩할 영화를 추천해드릴게요 !</p>
            <button v-on:click="startGame" class="btn-lg bg-primary">게임 시작하기</button>
        </div>
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
.background {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    /* background-image: url('https://i.pinimg.com/736x/85/4a/a0/854aa031770645b00e9a053f88d24fc9.jpg'); */
    background-image: url('https://i.pinimg.com/736x/09/09/5b/09095bfebec5061afb88cd727a1504d8.jpg');
    background-size: contain;
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>