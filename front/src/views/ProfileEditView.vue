<template>
    <input type="text" v-show="!introduction" class="gray2">아직 등록된 자기소개가 없어요!</input>
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