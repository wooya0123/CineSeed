<template>
  <div class="movie_card" @click="goToDetail">
    <img class="thumbnail" :src="thumbnailUrl" alt="movie_thumbnail">
    {{ movie.genre }}
    {{ movie.title }}
    <br>
    <img class="profile_image" :src="profileImage" alt="profile_image">
    {{ movie.user_nickname }}
    <hr>
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
.thumbnail {
  width: 100px;
}

.profile_image {
  width: 100px;
}

.movie_card {
  cursor: pointer;
}
</style>