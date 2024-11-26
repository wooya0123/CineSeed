<template>
  <div class="movie-card bg-gray5" @click="goToDetail">
    <img class="thumbnail" :src="thumbnailUrl" alt="movie_thumbnail">
    
    <div class="movie-info-container">
      <p class="movie-genre primary caption">{{ movie.genre }}</p>
      <p class="movie-title white">{{ movie.title }}</p>
    </div>
    
    <div class="profile-container">
      <img class="profile_image" :src="profileImage" alt="profile_image">
      {{ movie.user_nickname }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const goToDetail = function () {
  router.push({ name : 'movieDetail', params : { id : props.movie.id }})
}

const props = defineProps({
  movie: Object,
})

const thumbnailUrl = computed(() => {
  return `http://127.0.0.1:8000${props.movie.image}`
})

const profileImage = computed(() => {
  return `http://127.0.0.1:8000${props.movie.profile_image}`
})

</script>


<style scoped>
.movie-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  border: none;
  border-radius: 8px;
  transition: transform 0.2s;
  cursor: pointer;
}

.movie-card:hover {
  transform: translateY(-5px);
}

.thumbnail {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px 8px 0 0;
}

.movie-info-container {
  margin-bottom: 10px;
}

.movie-genre {
  margin-top: 15px;
  margin-left: 10px;
  margin-bottom: 0;
}

.movie-title{
  margin-top: 0;
  margin-left: 10px;
}

.profile-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  margin-bottom: 10px;
  margin-left: 10px;
}

.profile_image {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 8px;
}

</style>