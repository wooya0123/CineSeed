<template>
  <div>
    <header>
      <GameBanner />
    </header>
    
    <section>
      <h2>트렌드 펀딩</h2>
      <MovieCarousel :movies="home.popularMovies"/>
    </section>

    <!-- 로그인 했을 때 보이는 섹션 -->
    <section v-if="account.isLogIn">
      <h2>{{ account.user.nickname }}님 취향과 비슷한 펀딩</h2>
      <MovieCarousel :movies="home.personalizedMovies"/>
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

</style>