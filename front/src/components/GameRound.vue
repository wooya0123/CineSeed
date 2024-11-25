<template>
    <div>
        <div v-if="questions && questionIndex < questions.length">
            <h2>{{ questions[questionIndex].text }}</h2>
            <button @click="selectAnswer('a')">{{  questions[questionIndex].a }}</button>
            <button @click="selectAnswer('b')">{{  questions[questionIndex].b }}</button>
        </div>
        <div v-if="movies && movieIndex < movies.length">
            <h2>두 영화 중 더 선호하는 영화를 선택해주세요</h2>
            <div>
                <label for="movie_a">{{ movies[movieIndex].title_a }}</label>
                <img @click="selectMovie" :src="movies[movieIndex].source_a" alt="영화a" id="movie_a">
            </div>
            <div>
                <label for="movie_b">{{ movies[movieIndex].title_b }}</label>
                <img @click="selectMovie" :src="movies[movieIndex].source_b" alt="영화b" id="movie_b">
            </div>
        </div>
        <div v-if="movies && movieIndex >= movies.length">
            <h2>취향 분석이 완료되었습니다.</h2>
            <h3>{{ userTitle }}</h3>
            <p @click="goHome">홈으로 가서 내 취향 맞춤 펀딩 둘러보기</p>
        </div>
    </div>
</template>

<script setup>
import { useAccountStore } from '@/stores/account'
import axios from 'axios'
import { onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const API_URL = 'http://127.0.0.1:8000'

const result = ref(null)        // ex. [ g, 1, c, 1, a, a, a, b, b ] 형태로 사용자 응답을 저장할 배열
const questions = ref(null)     // 질문 리스트
const questionIndex = ref(0)    // 현재 보고 있는 문제가 몇 번인지 저장할 변수

const movies = ref(null)        // 영화 리스트
const movieIndex = ref(0)

const router = useRouter()
const accountStore = useAccountStore()

const userTitle = ref(null)

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
        result.value = res.data.type.split('') // 문제 코드 리스트로 변환 후 저장
        
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

// 질문이 끝나면 데이터를 가져오기
const setMovieRound = function () {
    axios({
        method: 'post',
        url: `${API_URL}/api/v1/game/result/`,
        headers: {
            Authorization: `Token ${accountStore.token}`
        },
        data: {
            result: result.value
        }
    })
        .then((res) => {
            getUserId()
            movies.value = [
                {
                    title_a: res.data[0].title,
                    source_a: res.data[0].image,
                    title_b: res.data[1].title,
                    source_b: res.data[1].image,
                },
                {
                    title_a: res.data[2].title,
                    source_a: res.data[2].image,
                    title_b: res.data[3].title,
                    source_b: res.data[3].image,
                },
                {
                    title_a: res.data[4].title,
                    source_a: res.data[4].image,
                    title_b: res.data[5].title,
                    source_b: res.data[5].image,
                },
                {
                    title_a: res.data[6].title,
                    source_a: res.data[6].image,
                    title_b: res.data[7].title,
                    source_b: res.data[7].image,
                },
                {
                    title_a: res.data[8].title,
                    source_a: res.data[8].image,
                    title_b: res.data[9].title,
                    source_b: res.data[9].image,
                }
            ]

            // Optional: 상태 변경 이후 `localStorage` 강제 갱신 (필요한 경우)
            localStorage.setItem('user-info', JSON.stringify(accountStore.user))
        })
        .catch((err) => {
            console.log(err) 
            if (err.status === 401) {      
                alert('로그인한 회원만 참여 가능합니다.')
                console.log(accountStore.token.value) 
                router.push({ name : 'login'})
            }
        })
}

// 칭호 저장하기 step 1. pk 가져오기
const getUserId = function () {
    axios({
        method: 'get',
        url: `${API_URL}/accounts/user/`,
        headers: {
            Authorization: `Token ${accountStore.token}`
        },
    })
        .then((res) => {
            const id = ref(res.data.pk)
            getUserTitle(id.value)

            // Optional: 사용자 ID 변경 시 동기화
            accountStore.user = { ...accountStore.user, id }
            localStorage.setItem('user-info', JSON.stringify(accountStore.user))
        })
        .catch((err) => {
            console.error(err)
        })
}


// 칭호 저장하기 step 2. title 가져오기
const getUserTitle = function(id) {
    axios({
        method: 'get',
        url: `${API_URL}/api/v1/profile/${id}/`,
        headers: {
            Authorization: `Token ${accountStore.token}`
        }
    })
        .then((res) => {
            console.log(res.data)
            userTitle.value = res.data.title

            // Optional: 칭호 업데이트 시 동기화
            accountStore.user = { ...accountStore.user, title: res.data.title }
            localStorage.setItem('user-info', JSON.stringify(accountStore.user))
        })
        .catch((err) => {
            console.error(err)
        })
}


// `watch`로 questionIndex가 끝났는지 감지
watch(questionIndex, (newValue, oldValue) => {
    if (questions.value && newValue >= questions.value.length) {
        // userTitle.value = accountStore.profile.title
        setMovieRound()
  }
})

// 영화 선택하면 다음 영화 보여주기
const selectMovie = function () {
    movieIndex.value++
}

// 홈으로 돌아가기
const goHome = function () {
    router.push({ name: 'home' })
}
</script>

<style scoped>

</style>