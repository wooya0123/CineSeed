<template>
    <div>
        <div v-if="questions && questionIndex < questions.length">
            <h2>{{ questions[questionIndex].text }}</h2>
            <button @click="selectAnswer('a')">{{  questions[questionIndex].a }}</button>
            <button @click="selectAnswer('b')">{{  questions[questionIndex].b }}</button>
        </div>
    </div>
    <div>
        <!-- <img src="movieSrcA" alt="영화1">
        <img src="movieSrcB" alt="영화1"> -->
    </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router';

const API_URL = 'http://127.0.0.1:8000'

const result = ref(null)        // ex. [ g, 1, c, 1, a, a, a, b, b ] 형태로 사용자 응답을 저장할 배열
const questions = ref(null)     // 질문 리스트
const questionIndex = ref(0)    // 현재 보고 있는 문제가 몇 번인지 저장할 변수

const gameStage = ref(1)
const movieSrcA = ref(null)
const movieSrcB = ref(null)

const router = useRouter()
const accountStore = useAccountStore()

// 게임을 시작할 때, 게임 질문 가져오기
 onMounted(() => {
    axios({
        method: 'get',
        url: `${API_URL}/api/v1/game/setting/`,
        headers: {
            Authorization: `Token ${accountStore.token}`
        }
    })
        .then((res) => {
            console.log(res.data)
            result.value = res.data.type.split('') // 문제 코드 리스트로 변환 후 저장
            console.log(result.value);
            
            questions.value = [
                {
                    text: res.data.question1_text,
                    a: res.data.question1_a,
                    b: res.data.question1_b,
                },
                {
                    text: res.data.question2_text,
                    a: res.data.question2_a,
                    b: res.data.question2_b,
                },
                {
                    text: res.data.question3_text,
                    a: res.data.question3_a,
                    b: res.data.question3_b,
                },
                {
                    text: res.data.question4_text,
                    a: res.data.question4_a,
                    b: res.data.question4_b,
                },
                {
                    text: res.data.question5_text,
                    a: res.data.question5_a,
                    b: res.data.question5_b,
                },
            ]
            console.log(questions.value)
            
        })
        .catch((err) => {
            console.log(err.status) 
            if (err.status === 401) {      
                alert('로그인한 회원만 참여 가능합니다.')
                console.log(accountStore.token.value) 
                router.push({ name : 'login'})
            }
        })
 })


// 문제 하나 지나갈 때마다 결과에 추가
 const selectAnswer = function (answer) {
    result.value.push(answer)
    questionIndex.value++
 } 
</script>

<style scoped>

</style>