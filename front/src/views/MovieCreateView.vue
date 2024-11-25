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
          <option value="1">로맨스</option>
          <option value="2">음악</option>
          <option value="3">다큐멘터리 / 역사</option>
          <option value="4">드라마</option>
          <option value="5">코미디 / 가족</option>
          <option value="6">공포 / 스릴러 / 미스터리</option>
          <option value="7">SF / 판타지 / 애니메이션</option>
          <option value="8">액션 / 모험 / 범죄 / 전쟁</option>
        </select>
        <br>
        <label for="start_date">시작 날짜: </label>
        <input type="date" id="start_date" v-model="movie.start_date" :min="minStartDate" :max="maxStartDate">
        <br>
        <label for="end_date">종료 날짜: </label>
        <input type="date" id="end_date" v-model="movie.end_date" :min="minStartDate" :max="maxStartDate">
        <br>
        <label for="target_amount">목표 금액: </label>
        <input type="number" id="target_amount" v-model="movie.target_amount" step="1000">
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
  genre: 'A', 
  start_date: '',
  end_date: '',
  is_appliable: '',
  movie_introduction: '',
  budget_plan: '',
  team_introduction: '',
  image: null,
  target_amount: ''
})

const today = new Date();
const nextYear = new Date();
nextYear.setFullYear(today.getFullYear() + 1);

const minStartDate = today.toISOString().split('T')[0]
const maxStartDate = nextYear.toISOString().split('T')[0]

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
  formData.append('genre', movie.value.genre)
  formData.append('start_date', movie.value.start_date)
  formData.append('end_date', movie.value.end_date)
  formData.append('is_appliable', movie.value.is_appliable)
  formData.append('movie_introduction', movie.value.movie_introduction)
  formData.append('budget_plan', movie.value.budget_plan)
  formData.append('team_introduction', movie.value.team_introduction)
  formData.append('target_amount', movie.value.target_amount)
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