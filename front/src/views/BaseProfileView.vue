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
              <a v-if="profileOwner.instagram" :href="profileOwner.instagram"><i class="bi bi-instagram"></i></a>
              <!-- etc 정보가 있을 경우 -->
              <div v-if="profileOwner.etc">
                <!-- etc가 주소인 경우 -->
                <span v-if="profileOwner.etc.includes('www')">
                  <a :href="profileOwner.etc" target="_blank" rel="noopener noreferrer"><i class="bi bi-link"></i></a>
                </span>
                <!-- etc가 메일인 경우 -->
                <span v-else @click="copyToClipboard(account.user.etc)" style="cursor: pointer; color: blue;">
                  <i class="bi bi-envelope"></i>
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
      <h2>{{ nickname }}님이 후원한 영화</h2>
      <MovieCarousel v-show="profileOwner.fund_movies.length" :movies="profileOwner.fund_movies"/>
      <div class="info gray2 bg-gray5" v-show="!profileOwner.fund_movies.length">
        아직 후원한 영화가 없어요
      </div>
    </section>
    
    <section class="movie-carousel">
      <h2>{{ nickname }}님이 좋아요한 영화</h2>
      <MovieCarousel v-show="profileOwner.like_movies.length" :movies="profileOwner.like_movies"/>
      <div class="info gray2 bg-gray5" v-show="!profileOwner.like_movies.length">
        아직 좋아요한 영화가 없어요
      </div>
    </section>

    <section class="movie-carousel" v-if="profileOwner.role === '유저'">
      <h2>혹시, 감독/배우/크루세요?</h2>
      <p>그렇다면, 회원 정보 수정으로 펀딩에 참여하거나, 펀딩을 시작해보세요!</p>
    </section>
    
    <section class="movie-carousel" v-else-if="profileOwner.role === '감독'">
      <div class="carousel-heading">
        <h2 style="flex: 1;">{{ nickname }}님의 영화</h2>
        <button class="btn-m bg-primary" v-if="profileOwner.id === account.user.id" @click="checkApplication">지원서 보기</button>
      </div>
      <div class="info gray2 bg-gray5" v-show="!profileOwner.my_movie.length">
        아직 등록한 영화가 없어요
      </div>
      <div 
        v-if="profileOwner.my_movie.length"
        >
        <MovieCarousel :movies="profileOwner.my_movie"/>
      </div>
    </section>
    
    <section class="movie-carousel" v-else>
      <h3>{{ nickname }}님이 지원한 영화</h3>
      <MovieCarousel v-show="profileOwner.apply_movies.length" :movies="profileOwner.apply_movies"/>
      <div class="info gray2 bg-gray5" v-show="!profileOwner.apply_movies.length">
        아직 지원한 영화가 없어요
      </div>
    </section>

    <!-- 모달 컴포넌트 -->
    <ApplicationModal
      v-if="isModalVisible"
      :ApplicationData="selectedApplicationData"
      @close="isModalVisible = false"
    />
  </div>
</template>

<script setup>
import MovieCarousel from '@/components/MovieCarousel.vue';
import ApplicationModal from '@/components/ApplicationModal.vue';

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
const profileAPI = account.API_URL + '/api/v1/profile/' // 프로필 데이터 가져올 주소


const loadProfile = () => {
  axios({
    method: 'get',
    url: `${profileAPI}${profileOwnerId.value}/`,
    headers: {
      Authorization: `Token ${account.token}`,
    },
  })
  .then((res) => {
    profileOwner.value = res.data;
  })
  .catch((err) => {
    console.log('프로필 불러오기 실패', err);
  });
};

const nickname = ref(null)
// 연락처 아이콘 클릭하면 클립보드에 복사
const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text).then(() => {
    alert('메일 주소가 클립보드에 복사되었습니다.')
  }).catch((err) => {
    console.error('클립보드 복사 실패:', err)
  })
}

const image = ref(null)
const introduction = ref(true)

onMounted(() => {
  loadProfile()
})

// 라우트 파라미터 변경 감지
watch(
  () => route.params.id,
  (newId) => {
    profileOwnerId.value = newId;
    loadProfile(); // 새 ID에 대해 데이터를 다시 가져옴
    isModalVisible.value = false
  }
);

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


const isModalVisible = ref(false); // 모달 표시 여부
const selectedApplicationData = ref(null); // 전달할 데이터

// 모달 표시 함수
const checkApplication = () => {
  // apply_users가 비어 있지 않은 데이터만 변환
  selectedApplicationData.value = profileOwner.value.my_movie
    .filter((movie) => movie.apply_users.length > 0) // 지원자가 있는 영화만 필터링
    .map((movie) => ({
      movieTitle: movie.title,
      applicants: movie.apply_users,
    }));
  isModalVisible.value = true; // 모달 표시
};
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

.contact {
  padding: 0px 12px;
  display: flex;
  flex-direction: row;
  gap: 8px;
  justify-content: center;
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

i {
  color: #FB4CA1;
}

.carousel-heading {
  display: flex;
  flex-direction: row;
  margin-bottom: 8px;
}
</style>