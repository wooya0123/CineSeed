<template>
  <div v-if="account.profile">
    <div class="info">
      <img class="profile_image" :src="`${account.API_URL}${account.profile.profile_image}`" alt="">
      <p v-if="account.profile.title && account.profile.title != 'null'">{{ account.profile.title }}</p>
      <a v-else href="">취향 테스트를 해보세요!</a>
    </div>
    
    <div class="contact">
      <!-- 인스타 정보가 있을 경우 -->
      <a v-if="account.profile.instagram" :href="account.profile.instagram">인스타</a>
      <!-- etc 정보가 있을 경우 -->
      <div v-if="account.profile.etc">
        <!-- etc가 주소인 경우 -->
        <span v-if="account.profile.etc.includes('www')">
          <a :href="account.profile.etc" target="_blank" rel="noopener noreferrer">연락처</a>
        </span>
        <!-- etc가 메일인 경우 -->
        <span v-else @click="copyToClipboard(account.profile.etc)" style="cursor: pointer; color: blue;">
          연락처 (클릭하여 복사)
        </span>
      </div>
    </div>
    
    <h2>{{ nickname }} {{ account.profile.role }}님</h2>
    <p>남은 잔액: {{ account.profile.cash }}원</p>
    <hr>

    <section class="fund_movies">
      <h3>{{ nickname }}님이 후원한 영화</h3>
      <MovieCarousel :movies="account.profile.fund_movies"/>
    </section>
    
    <section class="like_movies">
      <h3>{{ nickname }}님이 좋아요한 영화</h3>
      <MovieCarousel :movies="account.profile.like_movies"/>
    </section>

    <section v-if="account.profile.role === '유저'">
      <h3>혹시, 감독/배우/크루세요?</h3>
      <p>그렇다면, 회원 정보 수정으로 펀딩에 참여하거나, 펀딩을 시작해보세요!</p>
    </section>
    
    <section v-else-if="account.profile.role === '감독'">
      <h3>{{ nickname }}님의 영화</h3>
      
    </section>
    
    <section v-else>
      <h3>{{ nickname }}님이 지원한 영화</h3>
      <MovieCarousel :movies="account.profile.apply_movies"/>
    </section>
    

    <hr>
    {{ account.profile}}
  </div>
</template>

<script setup>
import MovieCarousel from '@/components/MovieCarousel.vue';

import { useAccountStore } from '@/stores/account';
import { onMounted } from 'vue';

const account = useAccountStore()
const nickname = account.user.nickname

onMounted(() => {
  console.log(account.profile)
  account.myPage()
})

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
.profile_image {
  width: 10%;
}
</style>