<template>
  <div>
    <h1>영화 목록</h1>
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
    
    <RouterLink :to="{ name : 'movieCreate' }">글쓰기</RouterLink>

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