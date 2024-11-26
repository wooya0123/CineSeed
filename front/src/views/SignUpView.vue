<template>
    <div class="signup-body"  v-show="!isSignup">
        <div class="signup-container" v-show="!store.isLogIn">
            <h1>회원가입</h1>
            <form class="signup-form" @submit.prevent="signUp">
                <!-- <label for="profile_image">프로필 이미지</label><br>
                <input class="profile-image" type="file" id="profile_image" @change="handleFileChange"><br> -->
                
                <label for="username"></label>
                <input class="input-white" type="text" id="username" v-model.trim="username" placeholder="아이디">

                <label for="password1"></label>
                <input class="input-white" type="password" id="password1" v-model.trim="password1" placeholder="비밀번호">

                <label for="password2"></label>
                <input class="input-white" type="password" id="password2" v-model.trim="password2" placeholder="비밀번호 확인">

                <label for="nickname"></label>
                <input class="input-white" type="text" id="nickname" v-model.trim="nickname" placeholder="닉네임">

                <label for="role"></label>
                <select class="role-dropdown" id="role" v-model="role">
                    <option value="포지션을 선택해주세요" disabled selected>포지션을 선택해주세요</option>
                    <option value="미정">미정</option>
                    <option value="감독">감독</option>
                    <option value="배우">배우</option>
                    <option value="스탭">스탭</option>
                </select>

                <input class="input-white" type="text" id="email" placeholder="이메일" v-model="email">

                <p>연락처</p>
                <span class="caption">프로필 페이지에서 다른사람에게 노출이 돼요</span>

                <input class="input-white" type="text" id="instagram" placeholder="인스타그램" v-model="instagram">

                <input class="input-white" type="text" id="etc" placeholder="기타 (ex. 메일, 휴대폰 번호)" v-model="etc">
                

                <!-- <label for="introduction">자기소개</label><br>
                <input type="textarea" id="introduction" v-model="introduction"><br> -->

                <button class="signup-btn bg-primary white">회원가입</button>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/account'

const store = useAccountStore()

const profile_image = ref(null)
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const nickname = ref(null)
const role = ref("포지션을 선택해주세요")
const email = ref(null)
const instagram = ref('')
const etc = ref('')
const introduction = ref('')

const handleFileChange = (event) => {
    if (event.target.files.length > 0) {
        profile_image.value = event.target.files[0] // 선택한 파일을 설정
    } else {
        profile_image.value = null // 파일이 없으면 null로 초기화
    }
}

const signUp = function () {
    const formData = new FormData()
    if (profile_image.value) {
        formData.append('profile_image', profile_image.value)
    }
    formData.append('username', username.value)
    formData.append('password1', password1.value)
    formData.append('password2', password2.value)
    formData.append('nickname', nickname.value)
    formData.append('role', role.value)
    formData.append('email', email.value)
    formData.append('instagram', instagram.value)
    formData.append('etc', etc.value)
    formData.append('introduction', introduction.value)
    store.signUp(formData)
  }
</script>

<style scoped>
.signup-body {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 10%;
  padding: 150px;
}

.signup-container {
  width: 500px;
  padding: 50px;
  background-color: #F5FAFF;
  border-radius: 10px;
  text-align: left;
}

.signup-container h1 {
  color: #333;
  margin-top: 20%;
}

.signup-form {
  margin-top: 50px;
  margin-bottom: 20px;
}

.signup-form p {
  color: #333;
  margin: 0;
  /* margin-top: 0px;
  margin-bottom: 15px; */
}

.signup-form span {
  color: #333;
}

.role-dropdown {
  width: 100%;
  margin-bottom: 18px;
  padding: 16px;
  border: 1px solid #D0D5DA;
  border-radius: 5px;
  font-size: 20px;
}

.role-dropdown option {
  color: #999999;
  font-size:15px;
}

.signup-btn {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>