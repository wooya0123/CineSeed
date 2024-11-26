<template>
  <div v-if="profileOwner">
    <div class="introduction">
      <div class="introduction-image bg-gray5">
        <img class="user_image" :src="image" alt="프로필이미지">
        <div class="title">
          <p v-if="profileOwner.title && profileOwner.title != 'null'">{{ profileOwner.title }}</p>
          <p v-else="profileOwner.title && profileOwner.title != 'null'">취향 분석을 해보세요</p>
          <button class="btn-m bg-primary" v-if="profileOwner.title && profileOwner.title != 'null'" @click="playGame">다시 분석해보기</button>
          <button class="btn-m bg-primary" v-else @click="playGame">취향 분석해보기</button>
        </div>
      </div>
      
      <div class="introduction-body bg-gray5">
        <div class="introduction-title-container">
          <div class="introduction-title">
            <h3>{{ nickname }}님</h3>
            <div class="contact">
              <!-- 인스타 정보가 있을 경우 -->
              <a v-if="profileOwner.instagram" :href="profileOwner.instagram">인스타</a>
              <!-- etc 정보가 있을 경우 -->
              <div v-if="profileOwner.etc">
                <!-- etc가 주소인 경우 -->
                <span v-if="profileOwner.etc.includes('www')">
                  <a :href="profileOwner.etc" target="_blank" rel="noopener noreferrer">연락처</a>
                </span>
                <!-- etc가 메일인 경우 -->
                <span v-else @click="copyToClipboard(account.user.etc)" style="cursor: pointer; color: blue;">
                  연락처 (클릭하여 복사)
                </span>
              </div>
            </div>
          </div>
          <p class="edit-btn caption" @click="goEditProfile" v-if="profileOwner.id === account.user.id">수정하기</p>
        </div>
        <p v-show="!introduction" class="gray2">아직 등록된 자기소개가 없어요!</p>
        <p v-show="introduction">{{ profileOwner.introduction }}</p>
      </div>
    </div>
    
    <section class="movie-carousel">
      <h3>{{ nickname }}님이 후원한 영화</h3>
      <MovieCarousel v-show="profileOwner.fund_movies.length" :movies="profileOwner.fund_movies"/>
      <div class="info gray2 bg-gray5" v-show="!profileOwner.fund_movies.length">
        아직 후원한 영화가 없어요
      </div>
    </section>
    
    <section class="movie-carousel">
      <h3>{{ nickname }}님이 좋아요한 영화</h3>
      <MovieCarousel v-show="profileOwner.like_movies.length" :movies="profileOwner.like_movies"/>
      <div class="info gray2 bg-gray5" v-show="!profileOwner.like_movies.length">
        아직 좋아요한 영화가 없어요
      </div>
    </section>

    <section class="movie-carousel" v-if="profileOwner.role === '유저'">
      <h3>혹시, 감독/배우/크루세요?</h3>
      <p>그렇다면, 회원 정보 수정으로 펀딩에 참여하거나, 펀딩을 시작해보세요!</p>
    </section>
    
    <section class="movie-carousel" v-else-if="profileOwner.role === '감독'">
      <h3>{{ nickname }}님의 영화</h3>
      <div class="info gray2 bg-gray5" v-show="!profileOwner.my_movie.length">
        아직 등록한 영화가 없어요
      </div>
      <div 
        v-show="profileOwner.my_movie.length"
        v-for="movie in profileOwner.my_movie"
        :key="movie.id"
        >
        <p>{{ movie.title }}</p>
        <img class="movie_poster" :src="`${account.API_URL}${movie.image}`" alt="">
        <p>{{ movie.apply_users }}</p>
      </div>
    </section>
    
    <section class="movie-carousel" v-else>
      <h3>{{ nickname }}님이 지원한 영화</h3>
      <MovieCarousel v-show="profileOwner.apply_movies.length" :movies="profileOwner.apply_movies"/>
      <div class="info gray2 bg-gray5" v-show="!profileOwner.apply_movies.length">
        아직 지원한 영화가 없어요
      </div>
    </section>
  </div>
</template>

<script setup>
import MovieCarousel from '@/components/MovieCarousel.vue';

import { useAccountStore } from '@/stores/account';
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router/dist/vue-router';

const router = useRouter()
const playGame = function () {
  router.push({name : 'game'})
}

const route = useRoute()
const account = useAccountStore()
const profileOwnerId = ref(route.params.id)
const profileOwner = ref(null)

const nickname = ref(null)

// 연락처 아이콘 클릭하면 클립보드에 복사
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    alert('클립보드에 복사되었습니다.')
  }).catch((err) => {
    console.error('클립보드 복사 실패:', err)
  })
}

const image = ref(null)
const introduction = ref(true)
const profileAPI = account.API_URL + '/api/v1/profile/' // 프로필 데이터 가져올 주소

onMounted(() => {
  // 이 프로필 주인 찾기
  axios({
    method: 'get',
    url: `${profileAPI}${profileOwnerId.value}/`,
    headers: {
      'Authorization': `Token ${account.token}`,
    },
  })
    .then((res) => {
      profileOwner.value = res.data
      console.log(profileOwner.value);
    })
    .catch((err) => {
      console.log('프로필 불러오기 실패', err)
    })
})

watch(profileOwner,
  (newVal) => {
    // 등록된 이미지가 없다면 기본 이미지 보여주기
    if (!profileOwner.value.profile_image) {
          image.value = account.API_URL + '/media/profile_images/default_profile.png'
    } else {
      image.value = account.API_URL + profileOwner.value.profile_image
    }

    // 자기소개가 있는지 체크
    if (!profileOwner.value.introduction) {
      introduction.value = false
    } else {
      introduction.value = true
    }

    // 닉네임 칭호 붙일지 말지 체크
    if (profileOwner.value.role != '미정') {
      nickname.value = profileOwner.value.nickname + ' ' + profileOwner.value.role
    } else {
      nickname.value = profileOwner.value.nickname
    }
})

const goEditProfile = function () {
  router.push({ name : 'profileEdit' })
}
</script>

<style scoped>
.introduction {
  display: flex;
  flex-direction: row;
  gap: 24px;
}

.introduction-image {
  width: 30%;
  height: fit-content;
  display: flex;
  flex-direction: column;
  border-bottom-right-radius: 20px;
  border-bottom-left-radius: 20px;
}

.introduction-title {
  display: flex;
  flex-direction: row;
}

.user_image {
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  width: 100%;
}

.title {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-content: center;
  text-align: center;
}

.introduction-body {
  display: flex;
  flex-direction: column;
  padding: 24px 32px;
  width: 100%;
  border-radius: 20px;
}


.movie_poster {
  width: 30%;
}

.movie-carousel {
  margin-top: 32px;
}

.info {
  margin-top: 16px;
  height: 160px;
  border-radius: 16px;
  padding: 16px;
}

.introduction-title-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.edit-btn {
  color: #9BA0A5;
  text-decoration-line: underline;
}

.edit-btn:hover {
  color: #FB4CA1;
  cursor: pointer;
}
</style>