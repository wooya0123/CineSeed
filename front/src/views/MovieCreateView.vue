<template>
  <div>
    <h1>영화 등록하기</h1>
    <form @submit.prevent="createMovie">
      <header>
        <label for="image">이미지: </label>
        <input type="file" id="image" @change="handleImageUpload">
        <br>
        <label for="title">제목: </label>
        <input type="text" id="title" v-model="movie.title">
        <br>
        <label for="genre">장르: </label>
        <select id="genre" v-model="movie.genre">
          <!-- <option v-for="genre in genres" :key="genre.id" :value="genre.id">{{ genre.name }}</option> -->
        </select>
        <br>
        <label for="start_date">시작 날짜: </label>
        <input type="date" id="start_date" v-model="movie.start_date">
        <br>
        <label for="end_date">종료 날짜: </label>
        <input type="date" id="end_date" v-model="movie.end_date">
        <br>
        <label for="is_appliable">지원자 받기</label>
        <input type="checkbox" id="is_appliable" v-model="movie.is_appliable">
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
        <button type="submit">생성하기</button>
      </body>
        
    </form>
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
const movie = ref({
  title: '',
  genre: '', 
  start_date: '',
  end_date: '',
  is_appliable: '',
  movie_introduction: '',
  budget_plan: '',
  team_introduction: '',
  image: null
})
const movieAPI = account.API_URL + '/api/v1/movie/'


const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    movie.value.image = file
  }
}

const createMovie = function () {
  const formData = new FormData()
  formData.append('title', movie.value.title)
  formData.append('genre', 1)
  formData.append('start_date', movie.value.start_date)
  formData.append('end_date', movie.value.end_date)
  formData.append('is_appliable', movie.value.is_appliable)
  formData.append('movie_introduction', movie.value.movie_introduction)
  formData.append('budget_plan', movie.value.budget_plan)
  formData.append('team_introduction', movie.value.team_introduction)
  if (movie.value.image) {
    formData.append('image', movie.value.image)
  }


  axios({
    method: 'post',
    url: `${movieAPI}`,
    headers: {
      'Authorization': `Token ${account.token}`,
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  })
  .then((res) => {
    console.log('등록 성공')
    router.push({ name: 'movies'})
  })
  .catch((err) => {
    console.log('등록 실패', err.response.data)
  })
}

onMounted(() => {
})

</script>

<style scoped>

</style>