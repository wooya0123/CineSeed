<template>
  <div v-if="movie">
    {{ movie }}
    <h1>영화 수정하기</h1>
    <form @submit.prevent="updateMovie">
      <header>
        <label for="image">이미지: </label>
        <input type="file" id="image" @change="handleImageUpload">
        <br>
        <label for="title">제목: </label>
        <input type="text" id="title" v-model="movie.title">
        <br>
        <label for="genre">장르: </label>
        <select id="genre" v-model="movie.genre">
        </select>
        <br>
        <p>시작 날짜: {{ movie.start_date }}</p>
        <p>종료 날짜: {{ movie.end_date }}</p>
        <br>
        <label for="is-appliable">지원자 받기</label>
        <input type="checkbox" id="is-appliable" v-model="movie.is_appliable">
      </header>

      <body>
        <label for="movie-introduction">영화 소개</label>
        <input type="textarea" id="movie-introduction" v-model="movie.movie_introduction">
        <br>
        <label for="budget-plan">예산 사용 계획</label>
        <input type="textarea" id="budget-plan" v-model="movie.budget_plan">
        <br>
        <label for="team-introduction">팀 소개</label>
        <input type="textarea" id="team-introduction" v-model="movie.team_introduction">
        <br>
        <button type="submit">수정하기</button>
      </body>
        
    </form>
  </div>
  <div v-else>
    <p>데이터를 불러오는 중입니다...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useAccountStore } from '@/stores/account';

const route = useRoute()
const router = useRouter()
const id = ref(route.params.id)
const account = useAccountStore()
const movie = ref(null)
const genres = ref(['낭만적인'])
const movieAPI = account.API_URL + '/api/v1/movie/' + `${id.value}/`

const getMovieDetail = () => {
  axios.get(`${movieAPI}`, {
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

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    movie.value.image = file
  }
}

const updateMovie = function () {
  const formData = new FormData()
  formData.append('genre', movie.value.genre_id)
  formData.append('is_appliable', movie.value.is_appliable)
  formData.append('movie_introduction', movie.value.movie_introduction)
  formData.append('budget_plan', movie.value.budget_plan)
  formData.append('team_introduction', movie.value.team_introduction)
  if (movie.value.image instanceof File) {
    formData.append('image', movie.value.image)
  }


  axios({
    method: 'put',
    url: `${movieAPI}`,
    headers: {
      'Authorization': `Token ${account.token}`,
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  })
  .then((res) => {
    console.log('수정 성공')
    router.push({ name: 'movieDetail', params : { id : movie.id}})
  })
  .catch((err) => {
    console.log('수정실패', err.response.data)
  })
}

onMounted(() => {
  getMovieDetail(id.value)
})

</script>

<style scoped>

</style>