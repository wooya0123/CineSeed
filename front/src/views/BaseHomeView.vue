<template>
  <div>
    <header>
      <GameBanner />
    </header>
    
    <section>
      <h2>트렌드 펀딩</h2>
      <MovieCarousel :movies="home.popularMovies"/>
    </section>

    <!-- 로그인 하지 않았을 때 보이지 않는 섹션 -->
    <section v-if="home.personalizedMovies.length">
      <h2>닉네임님 취향과 비슷한 펀딩</h2>
      <MovieCarousel :movies="home.personalizedMovies"/>
    </section>
  
  </div>
</template>

<script setup>

import GameBanner from '@/components/GameBanner.vue';
import MovieCarousel from '@/components/MovieCarousel.vue';

import { useHomeStore } from '@/stores/home';
import { onMounted } from 'vue';

const home = useHomeStore()

onMounted(() => {
  home.getPopularMovies()
  home.getPersonalizedMovies()
})

</script>

<style scoped>

</style>