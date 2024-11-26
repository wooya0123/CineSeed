<template>
  <div v-if="movie">
    <RouterLink class="back-button" :to="{ name: 'movies' }">목록으로</RouterLink>

      <p class="movie-genre primary">{{ movie.genre }}</p>
      
      <h2 class="movie-title">{{ movie.title }}</h2>
      <div>
        <img @click="goToProfile" class="profile-image" :src="`${account.API_URL}${movie.profile_image}`" alt="">
        <span class="profile-name">{{ movie.user_nickname }}</span>
      </div>
      

    <div class="movie-detail-container">
      <img class="movie-image" :src="`${account.API_URL}${movie.image}`" alt="영화 이미지">
      
      <section class="movie-info">
        <div class="funding-status">
          <p class="funing-label">모집금액</p>
          <div class="funding-amounts">
            <p class="funding-content">{{ movie.fund_amounts }}원</p>
            <span class="primary">{{ percent }}% 달성!</span>
          </div>
          
        </div>
        <div class="funding-status">
          <p class="funing-label">남은 기간</p>
          <p class="funding-content">{{ daysUntilEndDate(movie.end_date) }}일</p>
        </div>
        <div class="funding-status">
          <p class="funing-label">후원자</p>
          <p class="funding-content">{{ movie.fund_users }}명</p>
        </div>
        <hr>
        <div class="funding-info">
          <span>목표 금액 | </span>
          <span class="target_amount">{{ movie.target_amount }}원</span>
        </div>
        <div class="funding-info">
          <span>펀딩 기간 | </span>
          <span class="funding-period">{{ movie.start_date }}~{{ movie.end_date }}</span>
        </div>
        
        <div class="like-funding">
          <button class="like-button bg-gray6" v-if="isLiked" @click="movieLike">
            <img src="@/components/Icons/heart_filled.svg" alt="좋아요 취소">
          </button>
          <button class="like-button bg-gray6" v-else @click="movieLike">
            <img src="@/components/Icons/heart.svg" alt="좋아요">
          </button>
          <button class="funding-button bg-primary white" @click="movieFund">{{ funding }}원 후원하기</button>
        
        </div>
        
        <div class="button-container">
          <button @click="increaseFunding(10000)">10,000원</button>
          <button @click="increaseFunding(100000)">100,000원</button>
          <button @click="increaseFunding(1000000)">1,000,000원</button>
          <button @click="reset">초기화</button>
        </div>
      </section>
    </div>

    <body>
      <section class="movie-info">
        <h4>영화 소개</h4>
        <hr>
        <p>{{ movie.movie_introduction }}</p>
      </section>
      <section class="movie-info" v-if="movie.budget_plan">
        <h4>예산 사용 계획</h4>
        <hr>
        <p>{{ movie.budget_plan }}</p>
      </section>
      <section class="movie-info">
        <h4>팀 소개</h4>
        <hr>
        <p>{{ movie.team_introduction }}</p>
      </section>
      <hr>
      <div class="detail-button" v-show="account.isLogIn">
        <!-- <button class="apply-button bg-primary white" v-if="account.user.id === movie.user" @click="updateMovie">수정하기</button> -->
        <button class="apply-button bg-primary white" v-if="!movie.apply_users.includes(account.user.id)" @click="movieApply">크루로 지원하기</button>
        <button class="apply-button bg-gray1 gray3" v-else>지원완료(비활성)</button>
      </div>
    </body>
  </div>
</template>

<script setup>


import { ref, onMounted, watch, computed } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/account';

const account = useAccountStore()
const route = useRoute()
const router = useRouter()
const id = ref(route.params.id)
const movie = ref(null)

const isLiked = ref(null)
const funding = ref(0)
const isApplied = ref(false)
const movieAPI = account.API_URL + '/api/v1/movie/' + `${id.value}/`

const percent = computed(() => {
  if (movie.value && movie.value.target_amount > 0) {
    return Math.round((movie.value.fund_amounts / movie.value.target_amount) * 100);
  }
  return 0;
});

const goToProfile = function () {
  router.push({ name : 'profile', params : { id : movie.user }})
}

const daysUntilEndDate = (endDate) => {
  const today = new Date();
  const end = new Date(endDate);
  const timeDiff = end - today;
  return Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
}

// 좋아요
const movieLike = function () {
  axios({
    method: 'post',
    url: `${movieAPI}like/`,
    headers: {
      'Authorization': `Token ${account.token}`
    }
  })
  .then((res) => {
    console.log(res)
    console.log('좋아요 성공')
    isLiked.value = res.data.is_liked
  })
  .catch((err) => {
    console.error(err)
  })
}

// 후원 금액 증가
const increaseFunding = function (amount) {
  funding.value += amount
}

// 후원 금액 초기화
const reset = function () {
  funding.value = 0
}

// 후원하기
const movieFund = function () {
  axios({
    method: 'post',
    url: `${movieAPI}fund/`,
    headers: {
      'Authorization': `Token ${account.token}`
    },
    data: {
      cash: funding.value
    }
  })
  .then((res) => {
    alert('후원해주셔서 감사합니다!')
    funding.value = 0
    window.location.reload()
  })
  .catch((err) => {
    console.log(err)
    if (err.response.status == 400) {
      alert('잔액이 부족합니다!')
      window.location.reload()
    } else {
      console.log(err)
    }
})}

// 지원하기
const movieApply = function () {
  axios({
    method: 'post',
    url: `${movieAPI}application/`,
    headers: {
      'Authorization': `Token ${account.token}`
    },
  })
  .then((res) => {
    alert('지원해주셔서 감사합니다!')
    isApplied.value = res.data.is_applied
    window.location.reload()
  })
}

// 글 수정하기
const updateMovie = function () {
  router.push({ name: 'movieEdit', params: { id: id.value }})
}


// 조회
const getMovieDetail = function () {
  axios({
    mehtod: 'get',
    url: `${movieAPI}`
  })
  .then((res) => {
    movie.value = res.data

  })
  .catch((err) => {
    console.error(err)
  })
}

// 영화 데이터 mount 전에 불러오기
onMounted(() => {
  getMovieDetail()
}) 

watch(route, (newRoute) => {
  id.value = newRoute.params.id
  getMovieDetail()
})

</script>

<style scoped>
.back-button {
  display: inline-block;
  background-color: #FB4CA1;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  text-decoration: none;
  cursor: pointer;
  margin-bottom: 20px;
}

.back-button:hover {
  background-color: #E63946;
}

.movie-genre {
  margin-top: 20px;
  margin-bottom: 0;
}

.profile-image {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 100%;
  cursor: pointer
}

.profile-name {
  font-size: 15px;
  margin: 0 10px;
}

.movie-detail-container {
  display: flex;
  gap: 40px;
  margin: 20px 0;
}

.movie-image {
  width: 50%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 8px;
}

.funding-status {
  margin-bottom: 30px;
}

.funding-amounts {
  display: flex;
  align-items: center;
}

.funing-label { 
  font-size: 10px;
  margin: 0;
}

.funding-content {
  font-size: 50px;
  margin-right: 20px;
}

.funding-info {
  margin: 20px 0;
}

.funding-period {
  margin-left: 40px;
}

.target_amount {
  margin-left: 40px;
}

.like-button {
  border: none;
  width: 25px; /* 버튼의 너비 고정 */
  height: 25px; /* 버튼의 높이 고정 */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0; /* 패딩 제거 */
  margin-left: auto;
  cursor: pointer; /* 커서 포인터 설정 */
}

.like-button img {
  width: 100%; /* 아이콘 크기 고정 */
  height: 100%; /* 아이콘 크기 고정 */
}

.funding-button {
  width: 80%;
  height: 40px;
  margin-left: auto;
}

.like-funding {
  display: flex;
  align-items: center;
}

.button-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px; /* 버튼 사이의 간격 */
  margin-top: 5px;
}

.button-container button {
  flex: 1 1 calc(50% - 10px); /* 버튼의 크기를 동일하게 설정하고, 간격을 고려하여 너비 설정 */
  height: 40px;
  background-color: #23282D;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.button-container button:hover {
  background-color: #FB4CA1; /* 마우스가 올라왔을 때 배경색 핑크색 */
}

.movie-info {
  margin-bottom: 30px;
}


.detail-button {
  width: 100%; /* 버튼의 너비를 로 설정 */
  display: flex;
  justify-content: center; /* 버튼을 가운데 정렬 */
  margin-top: 20px; /* 상단 여백 추가 */
}

.apply-button {
  width: 50%; /* 버튼의 너비를 100%로 설정 */
  height: 50px; /* 버튼의 높이 설정 */
  background-color: #FB4CA1; /* 버튼 배경색 설정 */
  color: white; /* 버튼 텍스트 색상 설정 */
  border: none; /* 버튼 테두리 제거 */
  border-radius: 5px; /* 버튼 모서리 둥글게 설정 */
  cursor: pointer; /* 커서 포인터 설정 */
  font-size: 16px; /* 버튼 텍스트 크기 설정 */
  text-align: center; /* 버튼 텍스트 가운데 정렬 */
  margin: 20px 0;
}

.apply-button.bg-gray1 {
  background-color: #9BA0A5; /* 비활성화된 버튼 배경색 설정 */
  color: #4B5055; /* 비활성화된 버튼 텍스트 색상 설정 */
  pointer-events: none;
}

</style>