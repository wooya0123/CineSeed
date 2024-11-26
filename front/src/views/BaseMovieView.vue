<template>
  <div>
      
      <div class="header">
        <h1>영화 목록</h1>
        <RouterLink class="create-button" :to="{ name : 'movieCreate' }">글쓰기</RouterLink>
      </div>
      

    <div class="movie-card-container">
      <RouterLink
      v-for="movie in movies"
      :key="movie.id"
      :to="{ name : 'movieDetail', params: { id : movie.id } }"
      class="movie-card-link"
      >
      <MovieCard :movie="movie"/>
    </RouterLink>
    </div>
    
    

    <RouterView />
  </div>
</template>

<script setup>
import MovieCard from '@/components/MovieCard.vue';
import axios from 'axios';

import { onMounted, ref } from 'vue';
import { useAccountStore } from '@/stores/account';

const account = useAccountStore()
const movies = ref(null)

onMounted(() => {
  axios({
    method: 'get',
    url: `${account.API_URL}/api/v1/movie/`
  })
  .then((res) => {
    movies.value = res.data
  })
  .catch((err) => {
    console.error(err)
  })
})

</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.create-button {
  margin-left: auto; /* 링크를 오른쪽 끝으로 배치 */
  background-color: #FB4CA1;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  text-decoration: none;
  cursor: pointer;
}

.movie-card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.movie-card-link {
  flex: 1 1 calc(33.333% - 16px);
  box-sizing: border-box;
  text-decoration: none;
}
</style>