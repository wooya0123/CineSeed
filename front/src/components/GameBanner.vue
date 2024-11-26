<template>
  <div class="banner">
    <div class="banner-text">
      <div class="white">
        <p>당신의 영화 취향을 알아보세요!</p>
        <h2>영화 취향 토너먼트 게임</h2>
      </div>
      <button class="btn-m bg-primary" @click='playGame'>게임 시작하기</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router/dist/vue-router';
const router = useRouter()
const playGame = function () {
  router.push({name : 'game'})
}
</script>

<style scoped>
.banner {
  border-radius: 20px;
  padding: 32px;
  height: 240px;
  min-width: 574px;
  display: flex;
  flex-direction: row;
  /* background-image: url('https://i.pinimg.com/originals/06/7f/a8/067fa8ac52c9112276b1b445670ce354.gif'); 이미지 URL 입력 */
  /* background-image: url('https://i.pinimg.com/originals/0d/bb/34/0dbb3414f38ec6a65d10d88225d71cb2.gif'); */
  /* background-image: url('https://i.pinimg.com/736x/18/11/8e/18118ef0cc8d2bdabd3cab6619a900bf.jpg'); */
  background-image: url('https://i.pinimg.com/originals/b8/e7/73/b8e773dcdf3e60ba1821757ec82d0574.gif');
  background-size: cover; /* 이미지가 요소를 가득 채우도록 크기 조정 */
  background-position: center;
  background-repeat: no-repeat;
  /* height: 100vh; 화면 전체 높이 */
}

.banner-text {
  align-items: flex-start;
}

.banner-image {
  background-image: url('https://i.pinimg.com/originals/c4/9b/1d/c49b1d8bd996ecf531330156a7232288.gif');
  background-size: cover; /* 이미지가 요소를 가득 채우도록 크기 조정 */
  background-position: center; /* 이미지가 중앙에 위치하도록 설정 */
  background-repeat: no-repeat; /* 이미지 반복되지 않도록 설정 */
}

p {
  margin-bottom: 4px;
}
</style>