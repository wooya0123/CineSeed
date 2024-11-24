<template>
  <div v-if="movie">
    {{ movie }}
    <h1>영화 수정하기</h1>
    <form @submit.prevent="updateMovie">
      <header>
        <label for="image">이미지: </label>
        <input type="file" id="image" @change="handleImageUpload">

        <label for="title">제목: </label>
        <input type="text" id="title" v-model="movie.title">

        <label for="genre">장르: </label>
        <input type="text" id="genre" v-model="movie.genre">

        <label for="period">펀딩 시작 날짜</label>
        <input type="text" id="period" v-model="movie.start_date">
        <label for="period">펀딩 종료 날짜</label>
        <input type="text" id="period" v-model="movie.end_date">

        <label for="is-appliable">지원자 받기</label>
        <input type="checkbox" id="is-appliable" v-model="movie.is_appliable">
      </header>

      <body>
        <label for="movie-introduction">영화 소개</label>
        <input type="textarea" id="movie-introduction" v-model="movie.movie_introduction">
        <label for="budget-plan">예산 사용 계획</label>
        <input type="textarea" id="budget-plan" v-model="movie.budget_plan">
        <label for="team-introduction">팀 소개</label>
        <input type="textarea" id="team-introduction" v-model="movie.team_introduction">
        <br>
        <button type="submit">수정하기</button>
      
      </body>
        
    </form>
  </div>
  <div v-else>
    <p>영화 데이터를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useAccountStore } from '@/stores/account';

const route = useRoute()
const id = ref(route.params.id)
const account = useAccountStore()
const movie = ref(null)

const getMovieDetail = (movieId) => {
  axios.get(`${account.API_URL}/api/v1/movie/${movieId}/`, {
    headers: {
      'Authorization': `Token ${account.token}`
    }
  })
  .then((res) => {
    movie.value = res.data
  })
  .catch((err) => {
    console.error(err)
  })
}

onMounted(() => {
  getMovieDetail(id.value)
})

</script>

<style scoped>

</style>