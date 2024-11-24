<template>
  <div v-if="movie">
    {{ movie }}
    <hr>
    <RouterLink :to="{ name: 'movies' }">목록으로</RouterLink>
    <header>
      <h2>{{ movie.title }}</h2>
      <img class="profile-image" :src="`${account.API_URL}${movie.profile_image}`" alt="">
      {{ movie.user_nickname }}
      <br>
      <img class="movie-image" :src="`${account.API_URL}${movie.image}`" alt="">

      <section>
        <p>모집금액: {{ movie.fund_amounts }}원</p>
        <p>남은 시간: </p>
        <p>후원자: {{ movie.fund_users }}명</p>
        <p>목표 금액: ??(글 작성할 때 없음)</p>
        <p>펀딩 기간: {{ movie.start_date }}~{{ movie.end_date }}</p>

        <button v-if="isLiked" @click="movieLike">좋아요 취소</button>
        <button v-else @click="movieLike">좋아요</button>
        <br>
        <span>{{ funding }}</span>
        <button @click="reset">초기화</button>
        <button @click="movieFund">후원하기</button>
        <br>
        <button @click="increaseFunding(10000)">10,000원</button>
        <button @click="increaseFunding(100000)">100,000원</button>
        <button @click="increaseFunding(1000000)">1,000,000원</button>
      </section>
    </header>

    <body>
      <section>
        <h4>영화 소개</h4>
        {{ movie.movie_introduction }}
      </section>
      <section>
        <h4>예산 사용 계획</h4>
        {{ movie.budget_plan }}
      </section>
      <section>
        <h4>팀 소개</h4>
        {{ movie.team_introduction }}
      </section>
      <hr>
      <button v-if="account.user.pk === movie.user" @click="updateMovie">수정하기</button>
      <button v-else-if="isApplied === false" @click="movieApply">크루로 지원하기</button>
      <button v-else>지원완료(비활성)</button>
    </body>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/account';

const account = useAccountStore()
const route = useRoute()
const router = useRouter()
const id = ref(route.params.id)
const movie = ref(null)
const movieAPI = account.API_URL + '/api/v1/movie/' + `${id.value}/`
const isLiked = ref(null)
const funding = ref(0)
const isApplied = ref(null)

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
    console.log('후원 성공')
    funding.value = 0
  })
}

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
    console.log(res)
    console.log('지원 성공')
    isApplied.value = res.data.is_applied
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

onMounted(() => {
  getMovieDetail()
}) 

watch(route, (newRoute) => {
  id.value = newRoute.params.id
  getMovieDetail()
})

</script>

<style scoped>
.profile-image {
  width: 10%;
}
.movie-image {
  width: 30%;
}
</style>