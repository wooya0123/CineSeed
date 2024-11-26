<template>
    <div class="container">
        <h2>프로필 수정</h2>
        
        <div class="introduction">
            <!-- 프로필 이미지 수정 -->
            <div class="introduction-image bg-gray5">
                <div class="image-wrapper">
                    <img class="user_image" :src="profileImagePreview || image" alt="프로필이미지" />
                    <!-- 이미지 바꾸기 버튼 -->
                    <label for="profileImage" class="btn-m bg-primary">이미지 바꾸기</label>
                    <input type="file" id="profileImage" class="file-input" @change="handleImageUpload" />
                </div>
            </div>

            <!-- 프로필 정보 수정 -->
             <div class="introduction-body">
                 <div class="introduction-form bg-gray5">
                     <!-- 닉네임 -->
                     <div class="form-group">
                         <label for="nickname">닉네임</label>
                         <input
                         type="text"
                         id="nickname"
                         v-model="form.nickname"
                         placeholder="닉네임을 입력하세요"
                         class="input-white"
                         />
                     </div>
     
                     <!-- 자기소개 -->
                     <div class="form-group">
                         <label for="introduction">자기소개</label>
                         <textarea
                             id="introduction"
                             v-model="form.introduction"
                             placeholder="자기소개를 입력하세요"
                             class="input-white"
                             style="height: 500px;"
                         ></textarea>
                     </div>
                     
                     <!-- 인스타그램 -->
                     <div class="form-group">
                         <label for="instagram">인스타그램</label>
                         <input
                             type="text"
                             id="instagram"
                             v-model="form.instagram"
                             placeholder="인스타그램 링크를 입력하세요"
                             class="input-white"
                         />
                     </div>
                     
                     <!-- 연락처 -->
                     <div class="form-group">
                         <label for="etc">연락처</label>
                         <input
                             type="text"
                             id="etc"
                             v-model="form.etc"
                             placeholder="메일 또는 URL"
                             class="input-white"
                         />
                     </div>
                 </div>
                 <!-- 저장 및 취소 버튼 -->
                 <div class="form-actions">
                 <button class="btn-lg bg-primary" @click="updateProfile">저장</button>
                 <button class="btn-lg bg-gray5" @click="cancelEdit">취소</button>
                 </div>
             </div>
        </div>

    </div>
</template>
  
  
  
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAccountStore } from '@/stores/account';

const router = useRouter();
const account = useAccountStore();

// API 경로 및 현재 사용자 ID
const profileAPI = `${account.API_URL}/api/v1/profile/update/`;
const profileOwnerId = account.user.id;

// Form 상태 관리
const form = ref({
  nickname: account.user.nickname || '',
  introduction: account.user.introduction || '',
  instagram: account.user.instagram || '',
  etc: account.user.etc || '',
});

// 이미지 관리
const image = ref(`${account.API_URL}${account.user.profile_image}` || `${account.API_URL}/media/profile_images/default_profile.png`);
const profileImage = ref(null);
const profileImagePreview = ref('');

const handleImageUpload = (event) => {
    if (event.target.files.length > 0) {
        profileImage.value = event.target.files[0] // 선택한 파일을 설정
    } else {
        profileImage.value = null // 파일이 없으면 null로 초기화
    }
}

// 프로필 업데이트
const updateProfile = function () {
  const formData = new FormData()

  formData.append('nickname', form.value.nickname);
  formData.append('introduction', form.value.introduction);
  formData.append('instagram', form.value.instagram);
  formData.append('etc', form.value.etc);

  if (profileImage.value) {
    formData.append('profile_image', profileImage.value);
  }

  axios({
    method: 'put',
    url: `${account.API_URL}/api/v1/profile/${account.user.id}/`,
    data: formData,
    headers: {
      'Authorization': `Token ${account.token}`,
      'Content-Type': 'multipart/form-data',
    }
  })
    .then((res)=> {
        alert('프로필이 성공적으로 수정되었습니다.')
        router.push({ name: 'home' })
    })
    .catch ((error) => {
        console.error('프로필 수정 실패:', error);
        alert('프로필 수정 중 오류가 발생했습니다.');
    })
};

// 취소 버튼
const cancelEdit = () => {
  router.push({ name: 'profileView', params: { id: profileOwnerId } });
};
</script>

<style scoped>
.introduction {
  display: flex;
  flex-direction: row;
  gap: 24px;
  align-items: flex-start;
}

.introduction-image {
  width: 30%;
  height: 30%;
  display: flex;
  flex-direction: column;
  border-bottom-right-radius: 20px;
  border-bottom-left-radius: 20px;
    overflow: hidden;
}

.image-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.user_image {
  border-top-left-radius: 20px;
  border-top-right-radius: 20px;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-input {
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  width: 100%;
  height: 300px;
  cursor: pointer;
}

.introduction-body {
    width: 100%;
}

.introduction-form {
  display: flex;
  flex-direction: column;
  width: 100%;
  border-radius: 20px;
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

label {
  font-weight: bold;
  margin-bottom: 8px;
}

input,
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 4px;
}

textarea {
  resize: none;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 20px;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
</style>
