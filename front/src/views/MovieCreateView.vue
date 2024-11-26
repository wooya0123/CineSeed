<template>
  <div>
    <h1>영화 등록하기</h1>
    <form class="movie-container bg-gray5" @submit.prevent="createMovie">
      <label class="input-black-label" for="title">영화 제목</label>
      <p>영화의 제목을 입력해주세요.</p>
      <input class="input-black bg-gray4" type="text" id="title" v-model="movie.title" placeholder="제목">
      <hr>
      <label class="input-black-label" for="genre">영화 장르</label>
      <p>기획한 영화의 성격과 가장 일치하는 장르를 골라주세요. <br>선택한 장르를 선호하는 사용자에게 감독님의 영화가 추천됩니다.</p>
      <select class="genre-dropdown bg-gray4 white" id="genre" v-model="movie.genre">
        <option value="장르를 선택해주세요" disabled selected>장르를 선택해주세요</option>
        <option value="1">로맨스</option>
        <option value="2">음악</option>
        <option value="3">다큐멘터리 / 역사</option>
        <option value="4">드라마</option>
        <option value="5">코미디 / 가족</option>
        <option value="6">공포 / 스릴러 / 미스터리</option>
        <option value="7">SF / 판타지 / 애니메이션</option>
        <option value="8">액션 / 모험 / 범죄 / 전쟁</option>
      </select>

      <hr>

      <label for="image">대표 이미지</label>
      <p style="margin: 8px 0;">후원자들이 영화의 내용을 쉽게 확인하고 영화의 분위기를 느낄 수 있는 이미지를 등록해주세요.</p>
      <div class="image-upload-container">
          <input class="input-image bg-gray4 white" type="text" id="image-path" v-model="movie.image_path" readonly>
          <label for="image" class="custom-file-upload bg-primary">파일 선택</label>
          <input type="file" id="image" @change="handleImageUpload">
        </div>

        <hr>

        <label class="input-black-label" for="movie-introduction">영화 소개</label>
        <textarea class="textarea-input-black" id="movie-introduction" v-model="movie.movie_introduction" placeholder="영화에 대해서 알려주세요."></textarea>
        
        <hr>

        <label class="input-black-label" for="budget-plan">예산 사용 계획</label>
        <textarea class="textarea-input-black" id="budget-plan" v-model="movie.budget_plan" placeholder="후원 받은 금액을 어떻게 사용할 것인지 적어주세요."></textarea>

        <hr>

        <label class="input-black-label" for="team-introduction">팀 소개</label>
        <p>혹시 아직 팀원이 필요하다면, 구하고 있는 포지션을 상세히 적어주세요!</p>
        <textarea class="textarea-input-black" id="team-introduction" v-model="movie.team_introduction" placeholder="프로젝트를 함께하는 팀에 대한 소개를 작성해주세요."></textarea>
        
        <hr>

        <div class="checkbox-container">
          <label class="input-black-label" for="is_appliable">지원서 받기</label>
          <input type="checkbox" id="is_appliable" v-model="movie.is_appliable">
        </div>
        
        <p style="margin-bottom: 10px">스탭, 배우의 지원서를 받을 수 있어요!<br>아직 팀원이 필요하다면 지원서 받기를 체크해주세요</p>
        
        <hr>

        <label class="input-black-label" for="target_amount">목표 금액</label> 
        <input class="input-black bg-gray4" type="number" id="target_amount" v-model="movie.target_amount" step="1000" placeholder="1000원 단위로 입력해주세요">

        <hr>

          <h5>펀딩 기간</h5>
          <p>펀딩 기간을 설정해주세요. 최대 1년까지 설정 가능합니다.</p>
          <div class="funding-period">
            <div class="date-input-start gray2">
              <label for="start_date">시작 날짜</label> 
              <input class="date-start bg-gray4 white" type="date" id="start_date" v-model="movie.start_date" :min="minStartDate" :max="maxStartDate">
            </div>
            <div class="date-input-end gray2">
              <label for="end_date">종료 날짜</label>
              <input class="date-end bg-gray4 white" type="date" id="end_date" v-model="movie.end_date" :min="minStartDate" :max="maxStartDate">
            </div>
          </div>
          
          <button class="create-btn bg-primary white" style="margin-top: 30px;" type="submit">등록하기</button>
    </form>
    

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useAccountStore } from '@/stores/account';

const route = useRoute()
const router = useRouter()
const id = ref(route.params.id)
const account = useAccountStore()
const movie = ref({
  title: '',
  genre: '장르를 선택해주세요', 
  start_date: '',
  end_date: '',
  is_appliable: '',
  movie_introduction: '',
  budget_plan: '',
  team_introduction: '',
  image: null,
  image_path: '',
  target_amount: ''
})

const today = new Date();
const nextYear = new Date();
nextYear.setFullYear(today.getFullYear() + 1);

const minStartDate = today.toISOString().split('T')[0]
const maxStartDate = nextYear.toISOString().split('T')[0]

const movieAPI = account.API_URL + '/api/v1/movie/'


const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    movie.value.image = file
    movie.value.image_path = event.target.files[0].name
  }
}

const createMovie = function () {
  const formData = new FormData()
  formData.append('title', movie.value.title)
  formData.append('genre', movie.value.genre)
  formData.append('start_date', movie.value.start_date)
  formData.append('end_date', movie.value.end_date)
  formData.append('is_appliable', movie.value.is_appliable)
  formData.append('movie_introduction', movie.value.movie_introduction)
  formData.append('budget_plan', movie.value.budget_plan)
  formData.append('team_introduction', movie.value.team_introduction)
  formData.append('target_amount', movie.value.target_amount)
  if (movie.value.image) {
    formData.append('image', movie.value.image)
  }


  axios({
    method: 'post',
    url: `${movieAPI}`,
    headers: {
      'Authorization': `Token ${account.token}`,
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  })
  .then((res) => {
    console.log('등록 성공')
    router.push({ name: 'movies'})
  })
  .catch((err) => {
    console.log('등록 실패', err.response.data)
  })
}

onMounted(() => {
})

</script>

<style scoped>
.movie-container {
  width: 100%;
  border-radius: 20px;
  padding: 30px;
  margin: 3% auto;
}

.movie-container p {
  font-size: 12px;
  margin: 0;
}

.textarea-input-black {
  background-color: #4B5055;
  color: #F5FAFF;
  width: 100%;
  margin: 10px 0;
  padding: 10px 15px;
  height: 200px;
  border: none;
  border-radius: 5px;
  box-sizing: border-box;
  vertical-align: top;
  overflow: auto;
  resize: none;
}

.textarea-input-black::placeholder {
  color: #9BA0A5;
}

.checkbox-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

#is_appliable {
  width: 25px;
  height: 25px;
  background-color: #4B5055; /* Sets the background color to gray */
  appearance: none; /* Removes default styling */
  -webkit-appearance: none; /* Removes default styling for Safari */
  cursor: pointer;
  border-radius: 5px;
}

#is_appliable:checked::before {
  content: '✔'; /* Adds a checkmark */
  color: #F5FAFF; /* Sets the checkmark color to white */
  display: block;
  text-align: center;
  line-height: 30px; /* Centers the checkmark vertically */
}

#is_appliable:checked {
  background-color: #FB4CA1; /* Keeps the background color gray when checked */
}

.genre-dropdown {
  width: 100%;
  margin: 20px 0;
  padding: 15px;
  border: #4B5055;
  border-radius: 5px;
  font-size: 17px;
}

.genre-dropdown option {
  color: #F5FAFF;
  font-size:15px;
}

.image-upload-container {
  display: flex;
  align-items: center;
}

.input-image {
  flex-grow: 1;
  margin-right: 20px;
  margin-top: 10px;
  margin-bottom: 10px;
  border: none;
  height: 45px;
  border-radius: 5px;
  padding: 10px 20px
}

input[type="file"] {
  display: none; /* 기본 파일 입력 요소 숨기기 */
}

.custom-file-upload {
  color: #F5FAFF;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  margin-left: auto;
}

.funding-period {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.date-input-start {
  flex: 1;
  margin-right: 10px;
  display: flex;
  flex-direction: column;
  border-radius: 5px;
}

.date-input-end {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 5px;
}

.date-start {
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  margin-top: 10px;
}

.date-end {
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  margin-top: 10px;
  color: ;
}

.create-btn {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

</style>