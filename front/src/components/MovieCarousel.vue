<template>
  <div>
    <MovieCard 
      v-for="movie in movies"
      :key="movie.id"
      :movie="movie"
    />
  </div>
</template>

<script setup>

import MovieCard from '@/components/MovieCard.vue';

const props = defineProps({
  movies: Array,
})

</script>

<style scoped>

</style>