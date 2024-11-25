<template>
  <div>
    <RouterLink
      v-for="movie in movies"
      :key="movie.id"
      :to="{ name : 'movieDetail', params: { id : movie.id } }"
      >
      <MovieCard :movie="movie"/>
    </RouterLink>
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

</style>