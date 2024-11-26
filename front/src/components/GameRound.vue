<template>
    <div class="container">
        <div v-if="questions && questionIndex < questions.length">
            <div class="question bg-white primary">
                <h3>{{ questions[questionIndex].text }}</h3>
            </div>

            <div class="answer gray6">
                <div class="answer-card-sm"
                    @mouseover="isHoveredA = true" 
                    @mouseleave="isHoveredA = false"
                >
                    <div class="answer-card-title" :class="{ 'hovered': isHoveredA }">A</div>
                    <div class="answer-card-text" @click="selectAnswer('a')">{{  questions[questionIndex].a }}</div>
                </div>
                <div class="answer-card-sm"
                    @mouseover="isHoveredB = true" 
                    @mouseleave="isHoveredB = false"
                >
                    <div class="answer-card-title" :class="{ 'hovered': isHoveredB }">B</div>
                    <div class="answer-card-text" @click="selectAnswer('b')">{{  questions[questionIndex].b }}</div>
                </div>
            </div>
        </div>

        <div v-if="movies && movieIndex < movies.length">
            <div class="question bg-white primary">
                <h3>두 영화 중 더 선호하는 영화를 선택해주세요</h3>
            </div>

            <div v-show="isLoading" class="loading-spinner"></div>
            <div v-show="!isLoading" class="answer gray6">
                <div class="answer-card-lg"
                    @mouseover="isHoveredA = true" 
                    @mouseleave="isHoveredA = false"
                >
                    <div class="answer-card-title" :class="{ 'hovered': isHoveredA }">{{ movies[movieIndex].title_a }}</div>
                    <img class="answer-card-movie" @click="selectMovie" :src="movies[movieIndex].source_a" alt="영화a" id="movie_a" @load="onImageLoadA">
                </div>
                <div class="answer-card-lg"
                    @mouseover="isHoveredB = true" 
                    @mouseleave="isHoveredB = false"
                >
                    <div class="answer-card-title" :class="{ 'hovered': isHoveredB }">{{ movies[movieIndex].title_b }}</div>
                    <img class="answer-card-movie" @click="selectMovie" :src="movies[movieIndex].source_b" alt="영화b" id="movie_b" @load="onImageLoadB">
                </div>
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

const isLoading = ref(true)
const isLoadingA = ref(true) // A 영화 이미지 로딩 상태
const isLoadingB = ref(true) // B 영화 이미지 로딩 상태

// 이미지 로딩 완료 핸들러
const onImageLoadA = () => {
  isLoadingA.value = false
  checkAllImagesLoaded()
}

const onImageLoadB = () => {
  isLoadingB.value = false
  checkAllImagesLoaded()
}

const checkAllImagesLoaded = () => {
    if (!isLoadingA.value && !isLoadingB.value) {
        isLoading.value = false
    }
}
// movies 또는 movieIndex가 변경되면 로딩 상태 초기화
watch(movieIndex, () => {
  isLoadingA.value = true;
  isLoadingB.value = true;
  isLoading.value = true;
});

const router = useRouter()
const accountStore = useAccountStore()

const userTitle = ref(null)

const isHoveredA = ref(false) // hover 상태를 추적하는 변수
const isHoveredB = ref(false) // hover 상태를 추적하는 변수

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
.question {
    width: 100%;
    max-width: 962px; /* 최대 너비 제한 */
    min-width: 516px;
    height: 15vw;
    max-height: 160px;
    min-height: 140px;
    border-radius: 20px;
    white-space: nowrap; /* 텍스트 줄바꿈 방지 */
    text-align: center;

    display: flex;
    justify-content: center;
    align-items: center;
}

.answer {
    width: 100%;
    max-width: 962px; /* 최대 너비 제한 */
    min-width: 516px;
    height: 20vw;
    max-height: 180px;
    min-height: 160px;
    padding: 0px;
    margin-top: 32px;
    display: flex;
    flex-direction: row;
    text-align: center;
    justify-content: space-between; /* 아이템 간 간격을 동일하게 배치 */
    gap: 16px;  /* 요소 간의 간격 설정 */
}

.answer-card-title {
    width: 100%;
    height: 32px;
    border-top-left-radius: 10px;  /* 왼쪽 상단 코너 */
    border-top-right-radius: 10px; /* 오른쪽 상단 코너 */
    background-color: #D0D5DA;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Pretendard-Medium';
}

.answer-card-title.hovered {
    background-color: #FB4CA1;
    cursor: pointer;
}

.answer-card-sm {
    flex: 1;
    width: 100%;
}

.answer-card-text {
    width: 100%;
    height: 80px;
    border-bottom-left-radius: 10px;  /* 왼쪽 상단 코너 */
    border-bottom-right-radius: 10px; /* 오른쪽 상단 코너 */
    background-color: #F5FAFF;
    display: flex;
    justify-content: center;
    align-items: center;
}

.answer-card-lg{
    flex: 1;
    width: 100%;
}

.answer-card-movie {
    width: 100%;
    max-height: 640px;
}

.loading-spinner {
  text-align: center;
  font-size: 16px;
  color: #F5FAFF;
}

.loading-spinner::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  border: 3px solid #F5FAFF;
  border-top: 3px solid #FB4CA1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  transform: translate(-50%, -50%);
}

@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

</style>