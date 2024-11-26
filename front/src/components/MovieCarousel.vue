<template>
  <div class="carousel-wrapper">
    <!-- 왼쪽 네비게이션 버튼 -->
    <button class="custom-prev" @click="prevSlide">‹</button>
    <Carousel class="movie-carousel" v-bind="config">
      <Slide v-for="movie in movies" :key="movie.id">
        <MovieCard
          :movie="movie"
          class="size"
        />
      </Slide>
      <template #addons>
        <Navigation />
      </template>
    </Carousel>
  </div>
</template>

<script setup>
import MovieCard from '@/components/MovieCard.vue';
import { Carousel, Slide, Navigation } from 'vue3-carousel';
import "vue3-carousel/dist/carousel.css";


const props = defineProps({
  movies: Array,
})

// Carousel configuration
const config = {
  itemsToShow: 4,
  itemsToScroll: 4,
  snapAlign: 'start',
  gap: 24,
};
</script>

<style scoped>
.size {
  width: 100%;
}
</style>