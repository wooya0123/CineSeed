<template>
  <div v-if="account.user">
    <div class="info">
      <img class="user_image" :src="`${account.API_URL}${account.user.profile_image}`" alt="">
      <p v-if="account.user.title && account.user.title != 'null'">{{ account.user.title }}</p>
      <a v-else href="">취향 테스트를 해보세요!</a>
    </div>
    
    <div class="contact">
      <!-- 인스타 정보가 있을 경우 -->
      <a v-if="account.user.instagram" :href="account.user.instagram">인스타</a>
      <!-- etc 정보가 있을 경우 -->
      <div v-if="account.user.etc">
        <!-- etc가 주소인 경우 -->
        <span v-if="account.user.etc.includes('www')">
          <a :href="account.user.etc" target="_blank" rel="noopener noreferrer">연락처</a>
        </span>
        <!-- etc가 메일인 경우 -->
        <span v-else @click="copyToClipboard(account.user.etc)" style="cursor: pointer; color: blue;">
          연락처 (클릭하여 복사)
        </span>
      </div>
    </div>
    
    <h2>{{ nickname }} {{ account.user.role }}님</h2>
    <p>남은 잔액: {{ account.user.cash }}원</p>
    <hr>

    <section class="fund_movies">
      <h3>{{ nickname }}님이 후원한 영화</h3>
      <MovieCarousel :movies="account.user.fund_movies"/>
    </section>
    
    <section class="like_movies">
      <h3>{{ nickname }}님이 좋아요한 영화</h3>
      <MovieCarousel :movies="account.user.like_movies"/>
    </section>

    <section v-if="account.user.role === '유저'">
      <h3>혹시, 감독/배우/크루세요?</h3>
      <p>그렇다면, 회원 정보 수정으로 펀딩에 참여하거나, 펀딩을 시작해보세요!</p>
    </section>
    
    <section v-else-if="account.user.role === '감독'">
      <h3>{{ nickname }}님의 영화</h3>
      <div 
        v-for="movie in account.user.my_movie"
        :key="movie.id"
        >
        <p>{{ movie.title }}</p>
        <img class="movie_paster" :src="`${account.API_URL}${movie.image}`" alt="">
        <p>{{ movie.apply_users }}</p>
        
      </div>
    </section>
    
    <section v-else>
      <h3>{{ nickname }}님이 지원한 영화</h3>
      <MovieCarousel :movies="account.user.apply_movies"/>
    </section>
  </div>
</template>

<script setup>
import MovieCarousel from '@/components/MovieCarousel.vue';

import { useAccountStore } from '@/stores/account';

const account = useAccountStore()
const nickname = account.user.nickname

// 연락처 아이콘 클릭하면 클립보드에 복사
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    alert('클립보드에 복사되었습니다.')
  }).catch((err) => {
    console.error('클립보드 복사 실패:', err)
  })
}
</script>

<style scoped>
.user_image {
  width: 10%;
}

.movie_paster {
  width: 30%;
}
</style>