<template>
  <div>
    <header>
      <GameBanner />
    </header>
    
    <section>
      <h3>인기 있는 펀딩</h3>
      <MovieCarousel :movies="home.popularMovies"/>
    </section>

    <section>
      <!-- 취향 토너먼트 게임 진행 완료 시 -->
      <div v-if="account.user && account.user.title">
        <h2>{{ account.user.nickname }}님 취향과 비슷한 펀딩</h2>
        <MovieCarousel :movies="home.personalizedMovies"/>
      </div>
    </section>
  
  </div>
</template>

<script setup>

import GameBanner from '@/components/GameBanner.vue';
import MovieCarousel from '@/components/MovieCarousel.vue';

import { useHomeStore } from '@/stores/home';
import { useAccountStore } from '@/stores/account';
import { onMounted } from 'vue';

const home = useHomeStore()
const account = useAccountStore()

onMounted(() => {
  home.getPopularMovies()
  home.getPersonalizedMovies() 
})

</script>

<style scoped>
section {
  padding: 32px 8px;
}
</style>